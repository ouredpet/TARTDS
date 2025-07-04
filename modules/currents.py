from modules.barrier_current import current_through_barrier_func
from physical_constants import PhysicalConstants as consts

def emitter_currents(model):
    j_e_in_ground = current_through_barrier_func(model, model.emitter, in_out = 'in')


    j_e_in_ground = 0.0
    j_e_out_ground = 0.0
    j_e_in_excited = 0.0
    j_e_out_excited = 0.0
    return j_e_in_ground, j_e_out_ground, j_e_in_excited, j_e_out_excited