import numpy as np

def flux_sphere(luminosity, distance):
    '''
    Calculates flux from the luminosity of the star and the distance the star is from the planet
    '''
    return luminosity / (4 * np.pi * distance**2)

def flux_inverse_square(flux_B, distance_a, distance_b):
    '''
    Converts the flux from one distance, to a flux of the same star, at a different distance
    '''
    return flux_B * (distance_b / distance_a)**2

def luminosity_boltzmann(surface_area, surface_temperature):
    '''
    Calculates total Luminosity from the surface temperature of the star and its surface area
    '''
    return 5.6704 * 10**-8 * surface_area * surface_temperature

def luminosity_flux_density(flux_density, illuminated_area):
    '''
    Calculates Luminosity from flux density and the luminated area 
    '''
    return flux_density * illuminated_area

def luminosity_sphere(flux, star_radius):
    '''
    Calculates Luminosity from Flux and the radius of the star
    '''
    return flux * 4 * np.pi * star_radius**2