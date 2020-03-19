import numpy as np

def flux_sphere(luminosity, distance):
    '''
    Calculates flux from the luminosity of the star and the distance the star is from the planet
    '''
    return luminosity / (4 * np.pi * (distance**2))

def flux_inverse_square(flux_B, distance_a, distance_b):
    '''
    Converts the flux from one distance, to a flux of the same star, at a different distance
    '''
    return flux_b * ((distance_b / distance_a)**2)

def luminosity_boltzmann(surface_area, surface_temperature):
    '''
    Calculates total Luminosity from the surface temperature of the star and its surface area
    '''
    return (5.6704 * 10**-8) * surface_area * surface_temperature

def luminosity_flux_density(flux_density, illuminated_area):
    '''
    Calculates Luminosity from flux density and the luminated area 
    '''
    return flux_density * illuminated_area

def luminosity_sphere(flux, star_radius):
    '''
    Calculates Luminosity from Flux and the radius of the star
    '''
    return flux * 4 * np.pi * (star_radius**2)

def redshift_doppler(velocity_perpendicular):
    '''
    Calculates redshift factor from the perpendicular velocity
    '''
    return np.sqrt(1 + (velocity_perpendicular / (3*10**8)) / (1 - (velocity_perpendicular / (3*10**8)) - 1))

def wavelength_doppler(redshift_factor, apparent_wavelength):
    '''
    Calculates the true wavelength, from the redshift factor and the apparent wavelength
    '''
    return (apparent_wavelength / redshift_factor)

def peak_wavelength_surface_temp(surface_temperature):
    return ((3 * 10**8) / (surface*temperature * 5.879 * 10**10)

'''
Calculates the peak wavelength from the surface temperature of the star, this should be used if the light emitted from the star is considered to be monochromatic
'''

def radiance_wavelength_temperature(peak_wavelength, surface_temperature):
    return ((2 * 6.63 * (10**-34) / (peak_wavelength)) * (1/(np.exp(6.63 * 10**-34 / (1.38 * 10**-23) * surface_temperature))))

'''
Calculates the radience (or effective intensity) of the peak wavelength of a star, from the peak wavelength and the surface temperature, likely shouldn't be needed unless light emission is calculated as an array
'''

def luminosity_peak_wavelength(peak_wavelength, star_radius):
    return (4 * np.pi * (star_radius**2) * (5.67 * 10**-8) * ((0.0029 / peak_wavelength)**4))
'''
Calculates luminosity of the star from the star's radius and the peak wavelength of emitted light
'''


# Not sure whether to implement a code for how the star appears light wise, but i will make a code regardless:
# 
#
#
#
#