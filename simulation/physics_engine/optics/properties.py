import numpy as np

def flux_sphere(luminosity, distance):
    return luminosity / (4 * np.pi * (distance**2))

'''
Calculates flux from the luminosity of the star and the distance the star is from the planet
'''

def flux_inverse_square(flux_B, distance_a, distance_b):
    return flux_b * ((distance_b / distance_a)**2)

'''
Converts the flux from one distance, to a flux of the same star, at a different distance
'''

def luminosity_boltzmann(surface_area, surface_temperature):
    return (5.6704 * 10**-8) * surface_area * surface_temperature

'''
Calculates total Luminosity from the surface temperature of the star and its surface area
'''

def luminosity_flux_density(flux_density, illuminated_area):
    return flux_density * illuminated_area

'''
Calculates Luminosity from flux density and the luminated area 
'''

def luminosity_sphere(flux, star_radius):
    return flux * 4 * np.pi * (star_radius**2)
'''
Calculates Luminosity from Flux and the radius of the star
'''

def redshift_doppler(velocity_perpendicular):
    return np.sqrt(1 + (velocity_perpendicular / (3*10**8)) / (1 - (velocity_perpendicular / (3*10**8)) - 1))

'''
Calculates redshift factor from the perpendicular velocity
'''

def wavelength_doppler(redshift_factor, apparent_wavelength):
    return (apparent_wavelength / redshift_factor)

'''
Calculates the true wavelength, from the redshift factor and the apparent wavelength
'''

def peak_wavelength_surface_temp(surface_temperature):
    return ((3 * 10**8) / (surface*temperature * 5.879 * 10**10)

'''
Calculates the peak wavelength from the surface temperature of the star
'''

def radiance_wavelength_temperature(peak_wavelength, surface_temperature):
    return ((2 * 6.63 * (10**-34) / (peak_wavelength)) * (1/(np.exp(6.63 * 10**-34 / (1.38 * 10**-23) * surface_temperature))))

'''
Calculates the radience (or effective intensity) of the peak wavelength of a star, from the peak wavelength and the surface temperature
'''

#TODO: add function to calculate luminosity in a given wavelength given a temp of a black body