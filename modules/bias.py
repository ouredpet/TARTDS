from physical_constants import PhysicalConstants as consts

def bias_calc(applied_bias, n_2D):
    """
    Dummy bias_calc function.
    Returns initial potential energies for each region as a dictionary.
    """
    return {
        "em_reg1": 0,
        "em_barrier": 0.3 * consts.e_c,
        "well_region": 0,
        "col_barrier": 0.3 * consts.e_c,
        "col_reg3": 0,
    }