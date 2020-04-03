import pygame
from simulation.physics_engine.optics.blackbody import luminosity as blackbody_luminosity

def blackbody_visable_colour(tempriture):
    return pygame.Color(255, 255, 255)#TODO: Remove this!!!!!!!!!
    redIntensity = blackbody_luminosity(700 * 10**-9, tempriture)
    greenIntensity = blackbody_luminosity(520 * 10**-9, tempriture)
    blueIntensity = blackbody_luminosity(460 * 10**-9, tempriture)

    maxColouredWavelength = max((redIntensity, greenIntensity, blueIntensity))

    return pygame.Color(int(255 * redIntensity / maxColouredWavelength),
                        int(255 * greenIntensity / maxColouredWavelength),
                        int(255 * blueIntensity / maxColouredWavelength))