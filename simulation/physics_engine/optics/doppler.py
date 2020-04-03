import numpy as np
from simulation.physics_engine.constants import c as speed_of_light

def redshift_doppler(velocity_perpendicular):
    '''
    Calculates redshift factor from the perpendicular velocity
    '''
    return np.sqrt(1 + (velocity_perpendicular / speed_of_light) / (1 - (velocity_perpendicular / speed_of_light) - 1))

def wavelength_doppler(redshift_factor, apparent_wavelength):
    '''
    Calculates the true wavelength, from the redshift factor and the apparent wavelength
    '''
    return (apparent_wavelength / redshift_factor)