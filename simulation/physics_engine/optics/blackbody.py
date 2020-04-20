import numpy as np

from simulation.physics_engine.constants import c as speed_of_light, h as planksConstant, k as boltzmann_constant, sb as stefan_boltzmann_constant, w as weins_constant

def peak_wavelength(surface_temperature):
    '''
    Calculates the peak wavelength from the surface temperature of the star, this should be used if the light emitted from the star is considered to be monochromatic
    '''
    return (weins_constant / surface_temperature)

def radiance(wavelength, surface_temperature):
    """
    Calculates the intensity of a specific wavelength emitted from a star, not the total luminosity

    Paramiters:
        float wavelength -> The wavelength in meters
        float surface_temperature -> The blackbody's temperature in kelvin
    """
    return 2 * planksConstant * speed_of_light**2 / (wavelength**5 * (np.exp(planksConstant * speed_of_light / (wavelength * boltzmann_constant * surface_temperature)) - 1))

def total_luminosity(peak_wavelength, star_radius):
    '''
    Calculates the total luminosity of a star from the star's radius and the peak wavelength
    '''
    return (4 * np.pi * (star_radius**2) * (5.67 * 10**-8) * ((0.0029 / peak_wavelength)**4))


def luminosity_from_temp(star_radius, surface_temperature):
    '''
    Calculates total luminosity of a star from the surface temperature and radius of the star
    '''
    return (4 * np.pi * star_radius**2 * stefan_boltzmann_constant * surface_temperature**4)


