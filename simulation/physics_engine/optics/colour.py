import pygame
from simulation.physics_engine.optics.blackbody import radiance as blackbody_luminosity

def blackbody_visable_colour(temperature):
    redIntensity = blackbody_luminosity(700 * 10**-9, temperature)
    greenIntensity = blackbody_luminosity(520 * 10**-9, temperature)
    blueIntensity = blackbody_luminosity(460 * 10**-9, temperature)

    maxColouredWavelength = max((redIntensity, greenIntensity, blueIntensity))

    return pygame.Color(int(255 * redIntensity / maxColouredWavelength),
                        int(255 * greenIntensity / maxColouredWavelength),
                        int(255 * blueIntensity / maxColouredWavelength))