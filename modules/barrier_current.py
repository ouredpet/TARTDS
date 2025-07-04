import numpy as np
from physical_constants import PhysicalConstants as consts
from modules.barrier_transparency import transparency_vectorized as transparency_func

def attempt_rate_func(model, energy_state):
    """
    Estimate the rate at which a particle with a given energy collides with one wall of a quantum well.

    This function uses a classical analogy: for a particle of mass `model.well.effective_mass` and energy `energy_state`
    confined in a 1D well of width `model.well.width`, the rate is calculated as the particle's velocity divided by twice the well width.
    This gives the number of times per second the particle would "hit" one wall.

    Parameters
    ----------
    model : object
        An object with a `well` attribute that has `effective_mass` and `width` attributes.
    energy_state : float
        The energy of the particle (in Joules).

    Returns
    -------
    float
        The estimated collision rate with one wall (in 1/s).
    """
    velocity = np.sqrt(2 * energy_state / model.well.effective_mass)
    rate = velocity / (2 * model.well.width)
    return rate

def current_through_barrier_func(model, barrier_model, in_out = 'in', broadening_type="lorentzian"):
    """
    Calculate the current through a quantum barrier for a given energy state.

    Parameters
    ----------
    model : object
        Contains emitter, collector, and well properties.
    barrier_model : object
        Used for transparency calculation.
    broadening_type : str, optional
        Type of energy broadening: "lorentzian" or "gaussian". Default is "lorentzian".

    Returns
    -------
    tuple
        (current, energy_vector, broadening)
    """

    energy_state = model.well.ground_state + model.well.state_shift  # Ground state energy minus the state shift 

    # Energy sweep for current calculation
    energy_vector = np.linspace(-0.1 * consts.e_c, 0.1 * consts.e_c, 100000) + energy_state
    transparency = transparency_func(energy_vector, barrier_model)
    rate = attempt_rate_func(model, model.well.ground_state)

    # Broadening
    gamma = 0.00001 * consts.e_c
    split = 1
    dE = 0.0001 * consts.e_c
    broadening = np.zeros_like(energy_vector)
    for i in range(split):
        shift = dE * i - 1/2 * dE * (split - 1)
        if broadening_type == "lorentzian":
            broadening += (gamma / np.pi) / ((energy_vector - energy_state + shift) ** 2 + gamma ** 2)
        elif broadening_type == "gaussian":
            broadening += (1 / (gamma * np.sqrt(2 * np.pi))) * np.exp(-((energy_vector - energy_state + shift) ** 2) / (2 * gamma ** 2))
        else:
            raise ValueError("broadening_type must be 'lorentzian' or 'gaussian'")
    broadening /= split

    # 2D density of states and Fermi-Dirac occupation
    m_eff = model.emitter.reg_1.effective_mass
    fermi = model.emitter.fermi_level
    T = model.temperature
    if in_out == 'in':
        n_available = (
            m_eff / (np.pi * consts.hbar ** 2)
            * consts.k_B * T
            * np.log(1 + np.exp((fermi - energy_vector) / (consts.k_B * T)))
        )
    elif in_out == 'out':
        n_available = model.well.n_2D

    # Current calculation
    d_current = n_available * rate * transparency * broadening
    current = consts.e_c * np.trapz(d_current, energy_vector)
    print(np.trapz(rate * transparency * broadening, energy_vector)/1e12)
    return current, energy_vector


