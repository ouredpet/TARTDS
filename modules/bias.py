from physical_constants import PhysicalConstants as consts

def bias_calc(applied_bias, n_2D):
    """
    Dummy bias_calc function.
    Returns initial potential energies for each region as a dictionary.
    """
    return {
        "em_reg1": 0.1 * consts.e_c,
        "em_barrier": 1.2 * consts.e_c - applied_bias/20 * consts.e_c,  # Example calculation
        "well_region": -2 * applied_bias/20 * consts.e_c,  # Example calculation
        "state_shift": -2 * applied_bias/20 * consts.e_c,  # Example calculation
        "col_barrier": 1.2 * consts.e_c - 3 * applied_bias/20 * consts.e_c,  # Example calculation
        "col_reg3": - 4 * applied_bias/20 * consts.e_c # Example calculation,
    }