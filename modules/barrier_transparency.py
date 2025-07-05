import numpy as np
from physical_constants import PhysicalConstants as consts
from modules.non_parabolic_mass import non_parabolic_mass

def calc_k(mass, potential, energy):
    return np.sqrt(2 * mass * (energy - potential) / consts.hbar**2)

def transparency_vectorized(energy_vec, model):
    energy_vec = energy_vec.astype(complex)
    m1 = non_parabolic_mass(model.reg_1.effective_mass, energy_vec, model.reg_1.potential_energy, model.reg_1.band_gap_energy)
    m2 = non_parabolic_mass(model.barrier.effective_mass, energy_vec, model.barrier.potential_energy, model.barrier.band_gap_energy)
    m3 = non_parabolic_mass(model.reg_3.effective_mass, energy_vec, model.reg_3.potential_energy, model.reg_3.band_gap_energy)
    v1 = model.reg_1.potential_energy
    v2 = model.barrier.potential_energy
    v3 = model.reg_3.potential_energy
    width = model.barrier.width

    k1 = calc_k(m1, v1, energy_vec)
    k2 = calc_k(m2, v2, energy_vec)
    k3 = calc_k(m3, v3, energy_vec)

    numerator = 2 * k1 *k2*m2*m3
    denominator = k2*m2*(k3*m1 + k1*m3) * np.cos(k2*width) - 1j*(k1*k3*m2**2 + k2**2*m1*m3) * np.sin(k2*width)

    with np.errstate(divide='ignore', invalid='ignore'):
        t_amp = numerator / denominator
        transparency = (k3 * m1) / (k1 * m3) * np.abs(t_amp)**2

    # Without effective mass dependence
    # numerator = 4 * k1 * k2
    # denominator = (k1 + k2)**2 * np.exp(-1j*k2*width) - (k1- k2)**2 * np.exp(1j*k2*width)
    # with np.errstate(divide='ignore', invalid='ignore'):
    #     t_amp = numerator / denominator
    #     transparency = np.abs(t_amp)**2

    # Ensure transparency is real-valued
    transparency = np.real(transparency)
    transparency = np.nan_to_num(transparency, nan=0.0)

    return transparency