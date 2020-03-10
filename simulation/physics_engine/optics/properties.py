import numpy as np

def flux_sphere(luminosity, distance):
    return luminosity / (4 * np.pi * (distance**2))

def flux_inverse_square(flux_B, distance_a, distance_b):
    return flux_b * ((distance_b / distance_a)**2)

def luminosity_boltzmann(surface_area, surface_temperature):
    return (5.6704 * 10**-8) * surface_area * surface_temperature

def luminosity_flux_density(flux_density, illuminated_area):
    return flux_density * illuminated_area

def luminosity_sphere(flux, star_radius):
    return flux * 4 * np.pi * (star_radius**2)

def redshift_doppler(velocity_perpendicular):
    return np.sqrt(1 + (velocity_perpendicular / (3*10**8)) / 1 - (velocity_perpendicular / (3*10**8))) - 1

def wavelength_doppler(redshift_factor, apparent_wavelength):
    return (redshift_factor * apparent_wavelength)

def peak_wavelength_surface_temp(surface_temperature):
    return ((3 * 10**8) / (surface*temperature * 5.879 * 10**10)



#TODO: add function to calculate luminosity in a given wavelength given a temp of a black body