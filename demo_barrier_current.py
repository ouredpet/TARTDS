import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_current import current_through_barrier_func
from modules.barrier_transparency import transparency_vectorized
from physical_constants import PhysicalConstants as consts
from modules.bias import bias_calc

# =========================
# Adjustable Parameters
# =========================
EFFECTIVE_MASS_INGAAS = 0.041 * consts.m0
EFFECTIVE_MASS_ALAS = 0.12 * consts.m0
WELL_WIDTH = 3.6e-9
BARRIER_WIDTH = 1.4e-9
FERMI_LEVEL_EMITTER = (0.16 + 0.1) * consts.e_c
FERMI_LEVEL_COLLECTOR = 0.16 * consts.e_c
GROUND_STATE = 0.25 * consts.e_c
EXCITED_STATE = 0.6 * consts.e_c
STATE_SHIFT = 0.0 * consts.e_c
N_2D = 1.0e16
TEMPERATURE = 300
APPLIED_BIAS_START = 0.0
APPLIED_BIAS_STOP = 3.0
APPLIED_BIAS_POINTS = 100

# Bandgap energies (in eV)
BANDGAP_INGAAS = 0.74      # In0.53Ga0.47As, lattice-matched to InP
BANDGAP_ALINGAAS = 0.84
BANDGAP_ALAS = 2.16        # Bulk AlAs, indirect gap

# =========================
# Classes
# =========================
class Region:
    def __init__(self, effective_mass, potential_energy, width, band_gap_energy):
        self.effective_mass = effective_mass
        self.potential_energy = potential_energy
        self.width = width
        self.band_gap_energy = band_gap_energy

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
    def __init__(self, effective_mass, width, n_2D, band_gap_energy):
        self.effective_mass = effective_mass
        self.ground_state = GROUND_STATE
        self.excited_state = EXCITED_STATE
        self.state_shift = STATE_SHIFT
        self.width = width
        self.n_2D = n_2D
        self.band_gap_energy = band_gap_energy

class Model:
    temperature = TEMPERATURE  # Default temperature in Kelvin
    def __init__(self, emitter, collector, well):
        self.emitter = emitter
        self.collector = collector
        self.well = well

# =========================
# Setup
# =========================
applied_bias = APPLIED_BIAS_START
init_potentials = bias_calc(applied_bias, N_2D)

em_reg1 = Region(
    EFFECTIVE_MASS_INGAAS,
    init_potentials["em_reg1"],
    0,
    band_gap_energy=BANDGAP_ALINGAAS * consts.e_c 
)
em_barrier = Region(
    EFFECTIVE_MASS_ALAS,
    init_potentials["em_barrier"],
    BARRIER_WIDTH,
    band_gap_energy=BANDGAP_ALAS * consts.e_c
)
well_region = Region(
    EFFECTIVE_MASS_INGAAS,
    init_potentials["well_region"],
    0,
    band_gap_energy=BANDGAP_INGAAS * consts.e_c
)

emitter = Emitter(em_reg1, em_barrier, well_region, FERMI_LEVEL_EMITTER)

col_reg1 = well_region  # Shared region
col_barrier = Region(
    EFFECTIVE_MASS_ALAS,
    init_potentials["col_barrier"],
    BARRIER_WIDTH,
    band_gap_energy=BANDGAP_ALAS * consts.e_c
)
col_reg3 = Region(
    EFFECTIVE_MASS_INGAAS,
    init_potentials["col_reg3"],
    0,
    band_gap_energy=BANDGAP_INGAAS * consts.e_c
)

collector = Collector(col_reg1, col_barrier, col_reg3, FERMI_LEVEL_COLLECTOR)

well = Well(EFFECTIVE_MASS_INGAAS, WELL_WIDTH, N_2D, BANDGAP_INGAAS * consts.e_c)
model = Model(emitter, collector, well)

# =========================
# Simulation
# =========================
applied_bias_values = np.linspace(APPLIED_BIAS_START, APPLIED_BIAS_STOP, APPLIED_BIAS_POINTS)
currents_vs_bias = []
col_currents_vs_bias = []

for applied_bias in applied_bias_values:
    potentials = bias_calc(applied_bias, N_2D)
    em_reg1.potential_energy = potentials["em_reg1"]
    em_barrier.potential_energy = potentials["em_barrier"]
    well_region.potential_energy = potentials["well_region"]
    well.state_shift = potentials["state_shift"] 
    col_barrier.potential_energy = potentials["col_barrier"]
    col_reg3.potential_energy = potentials["col_reg3"]
    current_in, energy_vector = current_through_barrier_func(model, model.emitter, in_out='in', broadening_type="lorentzian")
    current_out, energy_vector = current_through_barrier_func(model, model.emitter, in_out='out', broadening_type="lorentzian")
    current = current_in - current_out
    # current = current_in 
    col_current_out, energy_vector = current_through_barrier_func(model, model.collector, in_out='out', broadening_type="lorentzian")
    currents_vs_bias.append(current)
    col_currents_vs_bias.append(col_current_out)

# =========================
# Plot
# =========================
currents_vs_bias = np.array(currents_vs_bias)
col_currents_vs_bias = np.array(col_currents_vs_bias)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(applied_bias_values, currents_vs_bias * 1e3 / 1e12, marker='o', label='Emitter')
ax.plot(applied_bias_values, col_currents_vs_bias * 1e3 / 1e12, marker='o', label='Collector')
ax.set_xlabel('Applied Bias (V)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Applied Bias')
ax.grid(True)
plt.legend()
plt.show()