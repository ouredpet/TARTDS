import numpy as np
import matplotlib.pyplot as plt
from modules.barrier_transparency import transparency_vectorized
from physical_constants import PhysicalConstants as consts

# Define simple Region and Model classes for testing
class Region:
    def __init__(self, effective_mass, potential_energy, width):
        self.effective_mass = effective_mass
        self.potential_energy = potential_energy
        self.width = width

class Model:
    def __init__(self, reg_1, reg_2, reg_3):
        self.reg_1 = reg_1
        self.reg_2 = reg_2
        self.reg_3 = reg_3

# Example parameters
reg1 = Region(effective_mass=consts.m0, potential_energy=0, width=0)
reg2 = Region(effective_mass=consts.m0, potential_energy=0.3*consts.e_c, width=5e-9)
reg3 = Region(effective_mass=consts.m0, potential_energy=0, width=0)
model = Model(reg1, reg2, reg3)

# Energy vector (in Joules)
energies = np.linspace(0.0, 0.5, 5000) * consts.e_c

# Calculate transparency
T = transparency_vectorized(energies, model)

# Plot using ax
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energies / consts.e_c, T)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Transparency')
ax.set_title('Barrier Transparency vs Energy')
ax.set_yscale('log')
ax.grid(True)

plt.show()