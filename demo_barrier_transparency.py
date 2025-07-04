import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_transparency import transparency_vectorized
from physical_constants import PhysicalConstants as consts

# =========================
# Adjustable Parameters
# =========================
EFFECTIVE_MASS = 0.041 * consts.m0
WELL_WIDTH = 3e-9
BARRIER_WIDTH = 10e-9
FERMI_LEVEL_EMITTER = (0.16 + 0.1) * consts.e_c
FERMI_LEVEL_COLLECTOR = 0.1 * consts.e_c
GROUND_STATE = 0.28 * consts.e_c
EXCITED_STATE = 0.6 * consts.e_c
STATE_SHIFT = 0.0 * consts.e_c
N_2D = 1e16
TEMPERATURE = 300

# =========================
# Classes
# =========================
class Region:
    def __init__(self, effective_mass, potential_energy, width):
        self.effective_mass = effective_mass
        self.potential_energy = potential_energy
        self.width = width

class Emitter:
    def __init__(self, reg_1, barrier, reg_3, fermi_level):
        self.reg_1 = reg_1
        self.barrier = barrier
        self.reg_3 = reg_3
        self.fermi_level = fermi_level

class Collector:
    def __init__(self, reg_1, barrier, reg_3, fermi_level):
        self.reg_1 = reg_1
        self.barrier = barrier
        self.reg_3 = reg_3
        self.fermi_level = fermi_level

class Well:
    def __init__(self, effective_mass, width, n_2D):
        self.effective_mass = effective_mass
        self.ground_state = GROUND_STATE
        self.excited_state = EXCITED_STATE
        self.state_shift = STATE_SHIFT
        self.width = width
        self.n_2D = n_2D

class Model:
    temperature = TEMPERATURE  # Default temperature in Kelvin
    def __init__(self, emitter, collector, well):
        self.emitter = emitter
        self.collector = collector
        self.well = well

# =========================
# Setup for zero bias (non-biased RTD)
# =========================
# Set all potentials to zero for non-biased case
zero_potential = 0.0

em_reg1 = Region(EFFECTIVE_MASS, zero_potential, 0)
em_barrier = Region(EFFECTIVE_MASS, 1.2 * consts.e_c, BARRIER_WIDTH)
well_region = Region(EFFECTIVE_MASS, zero_potential, 0)  # Shared region

emitter = Emitter(em_reg1, em_barrier, well_region, FERMI_LEVEL_EMITTER)
col_reg1 = well_region  # Shared region
col_barrier = Region(EFFECTIVE_MASS, zero_potential, BARRIER_WIDTH)
col_reg3 = Region(EFFECTIVE_MASS, zero_potential, 0)
collector = Collector(col_reg1, col_barrier, col_reg3, FERMI_LEVEL_COLLECTOR)
well = Well(EFFECTIVE_MASS, WELL_WIDTH, N_2D)
model = Model(emitter, collector, well)

# =========================
# Transparency Calculation
# =========================
energy_vec = np.linspace(0, 10, 5000) * consts.e_c  # 0 to 1.2 eV in Joules
transparency = transparency_vectorized(energy_vec, model.emitter)

# =========================
# Plot
# =========================
plt.figure(figsize=(6, 4))
plt.plot(energy_vec / consts.e_c, transparency)
plt.xlabel('Energy (eV)')
plt.ylabel('Transparency')
plt.title('Barrier Transparency vs Energy (Non-biased RTD)')
plt.yscale('log')
plt.grid(True)
plt.show()