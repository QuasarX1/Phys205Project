import numpy as np
from simulation.physics_engine.constants import c as speed_of_light, h as planksConstant, k as boltzmann_constant

def peak_wavelength(surface_temperature):
    '''
    Calculates the peak wavelength from the surface temperature of the star, this should be used if the light emitted from the star is considered to be monochromatic
    '''
    return speed_of_light / (surface_temperature * 5.879 * 10**10)#TODO: is this Wiens constant?? if so needs to be put in the constants file

def radiance(wavelength, surface_temperature):
    """
    Calculates the luminosity of a specific wavelength emitted from a star, not the total luminosity

    Paramiters:
        float wavelength -> The wavelength in meters
        float surface_temperature -> The blackbody's temperature in kelvin
    """
    return 2 * planksConstant * speed_of_light / wavelength**5 / (np.exp(planksConstant / wavelength * surface_temperature * boltzmann_constant) - 1)

def total_luminosity(peak_wavelength, star_radius):
    '''
    Calculates the total luminosity of a star from the star's radius and the peak wavelength
    '''
    return (4 * np.pi * (star_radius**2) * (5.67 * 10**-8) * ((0.0029 / peak_wavelength)**4))


