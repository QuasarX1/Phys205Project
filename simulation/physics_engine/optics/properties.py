import numpy as np

def flux_sphere(luminosity, distance):
    flux = luminosity/(4*np.pi*(distance**2))

def flux_inverse_square(flux_B, distance_a, distance_b):
    flux = flux_b*((distance_b/distance_a)**2)

def luminosity_boltzmann(surface_area, surface_temperature):
    luminosity = (5.6704*10**-8)*surface_area*surface_temperature

def luminosity_flux_density(flux_density, illuminated_area):
    luminosity = flux_density*illuminated_area

def luminosity_sphere(flux, star_radius):
    luminosity = flux*4*np.pi*(star_radius**2)

def redshift_doppler(velocity_perpendicular):
    redshift_factor = np.sqrt(1+(velocity_perpendicular/(3*10**8))/1-(velocity_perpendicular/(3*10**8))) - 1

def wavelength_doppler(redshift_factor, apparent_wavelength):
    true_wavelength = (redshift_factor*apparent_wavelength)


