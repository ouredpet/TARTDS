import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_current import current_throug_barrier_func
from modules.barrier_transparency import transparency_vectorized
from physical_constants import PhysicalConstants as consts
from modules.bias import bias_calc

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
    def __init__(self, effective_mass, width):
        self.effective_mass = effective_mass
        self.width = width

class Model:
    temperature = 300  # Default temperature in Kelvin
    def __init__(self, emitter, collector, well):
        self.emitter = emitter
        self.collector = collector
        self.well = well

# Define regions
em_reg1 = Region(effective_mass=consts.m0, potential_energy=0, width=0)
em_barrier = Region(effective_mass=consts.m0, potential_energy=0.3*consts.e_c, width=5e-9)
well_region = Region(effective_mass=consts.m0, potential_energy=0, width=0)  # Shared region

emitter = Emitter(em_reg1, em_barrier, well_region, fermi_level=0.1*consts.e_c)

col_reg1 = well_region  # Shared region
col_barrier = Region(effective_mass=consts.m0, potential_energy=0.3*consts.e_c, width=5e-9)
col_reg3 = Region(effective_mass=consts.m0, potential_energy=0, width=0)

collector = Collector(col_reg1, col_barrier, col_reg3, fermi_level=0.1*consts.e_c)

well = Well(effective_mass=consts.m0, width=10e-9)
model = Model(emitter, collector, well)

# Sweep energy_state (in Joules)
energy_states = 0.1 * consts.e_c
currents, energy_vector, broadening = current_throug_barrier_func(model, model.emitter, energy_states)

applied_bias_values = np.linspace(0, 0.5, 10)  # Example sweep
n_2D = 1e12  # Example value

results = []

for applied_bias in applied_bias_values:
    potentials = bias_calc(applied_bias, n_2D)
    em_reg1.potential_energy = potentials["em_reg1"]
    em_barrier.potential_energy = potentials["em_barrier"]
    well_region.potential_energy = potentials["well_region"]
    col_barrier.potential_energy = potentials["col_barrier"]
    col_reg3.potential_energy = potentials["col_reg3"]
    currents, energy_vector, broadening = current_throug_barrier_func(model, model.emitter, energy_states)
    results.append((applied_bias, currents, broadening))

# Plot
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energy_vector / consts.e_c, currents)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Energy')
ax.set_yscale('log')
ax.grid(True)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energy_vector / consts.e_c, broadening)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Energy')
ax.set_yscale('log')
ax.grid(True)

plt.show()