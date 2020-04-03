import numpy as np
from simulation.physics_engine.constants import c as speed_of_light, h as planksConstant, k as boltzmann_constant

def peak_wavelength(surface_temperature):
    '''
    Calculates the peak wavelength from the surface temperature of the star, this should be used if the light emitted from the star is considered to be monochromatic
    '''
    return speed_of_light / (surface_temperature * 5.879 * 10**10)#TODO: is this Wiens constant?? if so needs to be put in the constants file

def luminosity(wavelength, surface_temperature):
    """
    Calculates the luminosity of radiation emitted by a blackbody of a given temperature in a given wavelength.

    Paramiters:
        float wavelength -> The wavelength in meters
        float surface_temperature -> The blackbody's temperature in kelvin
    """
    return 2 * planksConstant * speed_of_light / wavelength**3 / (np.exp(planksConstant / wavelength * surface_temperature * boltzmann_constant) - 1)





#TODO: what do the functions below do??? Could do with a more in depth description plus physics equasion in the comment for each

def peak_luminosity(surface_temperature):
    '''
    Calculates the radience (or effective intensity) of the peak wavelength of a star, from the peak wavelength and the surface temperature, likely shouldn't be needed unless light emission is calculated as an array
    '''
    peak_wavelength = peak_wavelength_surface_temp(surface_temperature)

    #TODO: should this be the same as the "luminosity" function above?
    # if so one or the other needs to be corrected and this line replaced with a function call instead
    return (2 * planksConstant / peak_wavelength) * np.exp(planksConstant / boltzmann_constant * surface_temperature)

def luminosity_peak_wavelength(peak_wavelength, star_radius):
    '''
    Calculates luminosity of the star from the star's radius and the peak wavelength of emitted light
    '''
    return (4 * np.pi * (star_radius**2) * (5.67 * 10**-8) * ((0.0029 / peak_wavelength)**4))
