import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_current import current_through_barrier_func
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
    def __init__(self, effective_mass, width, n_2D):
        self.effective_mass = effective_mass
        self.ground_state = 0.1 * consts.e_c  # Example value
        self.excited_state = 0.6 * consts.e_c  # Example value
        self.state_shift = 0.0 * consts.e_c  # Example value
        self.width = width
        self.n_2D = n_2D

class Model:
    temperature = 300  # Default temperature in Kelvin
    def __init__(self, emitter, collector, well):
        self.emitter = emitter
        self.collector = collector
        self.well = well

# Initial bias values for region potentials
applied_bias = 0
n_2D = 1e16  # Example value
init_potentials = bias_calc(applied_bias, n_2D)

# Define regions using initial potentials
em_reg1 = Region(effective_mass=consts.m0, potential_energy=init_potentials["em_reg1"], width=0)
em_barrier = Region(effective_mass=consts.m0, potential_energy=init_potentials["em_barrier"], width=5e-9)
well_region = Region(effective_mass=consts.m0, potential_energy=init_potentials["well_region"], width=0)  # Shared region

emitter = Emitter(em_reg1, em_barrier, well_region, fermi_level=0.1*consts.e_c)

col_reg1 = well_region  # Shared region
col_barrier = Region(effective_mass=consts.m0, potential_energy=init_potentials["col_barrier"], width=5e-9)
col_reg3 = Region(effective_mass=consts.m0, potential_energy=init_potentials["col_reg3"], width=0)

collector = Collector(col_reg1, col_barrier, col_reg3, fermi_level=0.1*consts.e_c)

well = Well(effective_mass=consts.m0, width=10e-9, n_2D=n_2D)
model = Model(emitter, collector, well)

# Sweep energy_state (in Joules)
currents, energy_vector = current_through_barrier_func(model, model.emitter, in_out='in')

applied_bias_values = np.linspace(-0.5, 0.5, 10)  # Example sweep

class Result:
    def __init__(self, bias, energy_vector, currents):
        self.bias = bias
        self.energy_vector = energy_vector
        self.currents = currents

results = []

for applied_bias in applied_bias_values:
    potentials = bias_calc(applied_bias, n_2D)
    em_reg1.potential_energy = potentials["em_reg1"]
    em_barrier.potential_energy = potentials["em_barrier"]
    well_region.potential_energy = potentials["well_region"]
    well.state_shift = potentials["state_shift"] 
    col_barrier.potential_energy = potentials["col_barrier"]
    col_reg3.potential_energy = potentials["col_reg3"]
    currents, energy_vector = current_through_barrier_func(model, model.emitter, in_out='in', broadening_type="gaussian")
    # currents, energy_vector = current_through_barrier_func(model, model.emitter, in_out='out', broadening_type="gaussian")
    results.append(Result(applied_bias, energy_vector, currents))

# Plot all results for current
fig, ax = plt.subplots(figsize=(6, 4))
for result in results:
    ax.plot(result.energy_vector / consts.e_c, result.currents, label=f'V={result.bias:.2f} V')
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Energy')
ax.set_yscale('log')
ax.grid(True)
ax.legend()

# Plot all results for broadening
# fig, ax = plt.subplots(figsize=(6, 4))
# for result in results:
#     ax.plot(result.energy_vector / consts.e_c, result.broadening, label=f'V={result.bias:.2f} V')
# ax.set_xlabel('Energy (eV)')
# ax.set_ylabel('Broadening (arb. units)')
# ax.set_title('Broadening vs Energy')
# ax.set_yscale('log')
# ax.grid(True)
# ax.legend()

plt.show()