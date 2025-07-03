import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_current import current_throug_barrier_func
from modules.barrier_transparency import transparency_vectorized
from physical_constants import PhysicalConstants as consts

# Define simple Region, Barrier, and Model classes for testing
class Region:
    def __init__(self, effective_mass, potential_energy, width):
        self.effective_mass = effective_mass
        self.potential_energy = potential_energy
        self.width = width

class Barrier:
    def transparency(self, energy_vector, model):
        return transparency_vectorized(energy_vector, model)

class Well:
    def __init__(self, effective_mass, width):
        self.effective_mass = effective_mass
        self.width = width

class Model:
    def __init__(self, reg_1, reg_2, reg_3, well, barrier):
        self.reg_1 = reg_1
        self.reg_2 = reg_2
        self.reg_3 = reg_3
        self.well = well
        self.barrier = barrier

# Example parameters (same as in demo_barrier_transparency.py)
reg1 = Region(effective_mass=consts.m0, potential_energy=0, width=0)
reg2 = Region(effective_mass=consts.m0, potential_energy=0.3*consts.e_c, width=5e-9)
reg3 = Region(effective_mass=consts.m0, potential_energy=0, width=0)
well = Well(effective_mass=consts.m0, width=10e-9)
barrier = Barrier()
model = Model(reg1, reg2, reg3, well, barrier)

# Sweep energy_state (in Joules)
energy_states = 0.1 * consts.e_c
currents, energy_vector, broadening = current_throug_barrier_func(model, energy_states)

# Plot
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energy_vector / consts.e_c, currents)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Energy')
ax.set_yscale('log')
ax.grid(True)

# Plot
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energy_vector / consts.e_c, broadening)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Current (arb. units)')
ax.set_title('Current Through Barrier vs Energy')
ax.set_yscale('log')
ax.grid(True)

plt.show()