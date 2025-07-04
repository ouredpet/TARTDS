import numpy as np
from physical_constants import PhysicalConstants as consts

def calc_k(mass, potential, energy):
    return np.sqrt(2 * mass * (energy - potential) / consts.hbar**2)

def transparency_vectorized(energy_vec, model):
    energy_vec = energy_vec.astype(complex)
    m1 = model.reg_1.effective_mass
    m2 = model.barrier.effective_mass
    m3 = model.reg_3.effective_mass
    v1 = model.reg_1.potential_energy
    v2 = model.barrier.potential_energy
    v3 = model.reg_3.potential_energy
    width = model.barrier.width

    k1 = calc_k(m1, v1, energy_vec)
    k2 = calc_k(m2, v2, energy_vec)
    k3 = calc_k(m3, v3, energy_vec)

    exp_k2_width = np.exp(1j * k2 * width)
    exp_minus_k2_width = np.exp(-1j * k2 * width)
    exp_minus_k1_width = np.exp(-1j * k1 * width)

    numerator = 2 * k1 * k2 * m2**2 * exp_minus_k1_width
    denominator = ((k1 * m2 + k2 * m1) * (k3 * m2 + k2 * m3) * exp_k2_width
                   - (k1 * m2 - k2 * m1) * (k3 * m2 - k2 * m3) * exp_minus_k2_width)

    with np.errstate(divide='ignore', invalid='ignore'):
        t_amp = numerator / denominator
        transparency = np.real((k3 * m1) / (k1 * m3) * np.abs(t_amp)**2)

    # Set transparency to zero where k1 is zero (or very close to zero)
    tol = 1e-14
    mask = np.abs(k1) < tol
    transparency[mask] = 0.0

    # Ensure transparency is real-valued
    transparency = np.real(transparency)

    return transparency