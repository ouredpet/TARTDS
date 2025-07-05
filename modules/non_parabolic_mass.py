def non_parabolic_mass(mass, energy, potential, band_gap_energy):
    """
    Calculate the non-parabolic effective mass based on the energy.
    
    Parameters
    ----------
    mass : float
        The effective mass of the region (in kg).
    energy : float or np.ndarray
        The energy (in Joules).
    
    Returns
    -------
    float or np.ndarray
        The non-parabolic effective mass (in kg).
    """
    return mass * (1 + (energy - potential) / band_gap_energy)