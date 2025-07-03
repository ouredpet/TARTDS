import numpy as np
from physical_constants import PhysicalConstants as consts

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

def current_throug_barrier_func(model, energy_state):
    Ne = 1 # number of electrons availible from the contact (changed this, now dummy)
    N_2D = 1 # Number of electrons in the QW (change this, now dummy)
    rate = attempt_rate_func(model, energy_state)
    energy_vector = np.linspace(0, 0.3*consts.e_c, 5000)  # Create a vector of energies from 0 to the given energy_state
    transparency = model.barrier.transparency(energy_vector, model)
    gamma = 0.0001*consts.e_c  # Broadening parameter (in Joules), can be adjusted based on the system
    split = 3
    dE = 0.001 * consts.e_c  # Energy step for broadening, can be adjusted based on the system
    broadening = np.zeros_like(energy_vector, dtype=float)
    for i in range(split):
        broadening += (gamma / np.pi) / ((energy_vector - energy_state + dE*i - dE*(split/2 - 1/2))**2 + gamma**2)
    broadening /= split  # Average the broadening over the splits
    # current = Ne * N_2D * rate * np.trapz(transparency * broadening, energy_vector)
    current = Ne * N_2D * rate * transparency * broadening
    return current, energy_vector, broadening

