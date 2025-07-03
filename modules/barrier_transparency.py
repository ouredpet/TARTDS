import numpy as np
from physical_constants import PhysicalConstants as consts

def calc_k(mass, potential, energy):
    return np.sqrt(2 * mass * (energy - potential) / consts.hbar**2)

def interface_matrix(m1, k1, m2, k2):
    # Transfer matrix at interface between regions with (m1, k1) and (m2, k2)
    a = 0.5 * (1 + (m2 * k1) / (m1 * k2))
    b = 0.5 * (1 - (m2 * k1) / (m1 * k2))
    return np.array([[a, b], [b, a]])

def propagation_matrix(k, width):
    # Propagation matrix through a region, vectorized for arrays
    phi = k * width
    shape = phi.shape
    P = np.zeros((2, 2) + shape, dtype=complex)
    P[0, 0, ...] = np.exp(1j * phi)
    P[1, 1, ...] = np.exp(-1j * phi)
    return P

def transparency_vectorized(energy_vec, model):
    energy_vec = energy_vec.astype(complex)
    m1, m2, m3 = model.reg_1.effective_mass, model.reg_2.effective_mass, model.reg_3.effective_mass
    v1, v2, v3 = model.reg_1.potential_energy, model.reg_2.potential_energy, model.reg_3.potential_energy
    w1, w2, w3 = model.reg_1.width, model.reg_2.width, model.reg_3.width

    k1 = calc_k(m1, v1, energy_vec)
    k2 = calc_k(m2, v2, energy_vec)
    k3 = calc_k(m3, v3, energy_vec)

    with np.errstate(divide='ignore', invalid='ignore'):

        T12 = interface_matrix(m1, k1, m2, k2)
        P2 = propagation_matrix(k2, w2)
        T23 = interface_matrix(m2, k2, m3, k3)

        M = np.einsum('ij...,jk...,kl...->il...', T12, P2, T23)
        t = 1 / M[0, 0]
        transparency = (np.abs(t)**2) * (np.real(k3 / m3) / np.real(k1 / m1))

    # Set transparency to zero where k1 or k3 are (close to) zero
    tol = 1e-14
    mask = (np.real(k1) < tol) | (np.real(k3) < tol)
    transparency[mask] = 0.0

    return transparency