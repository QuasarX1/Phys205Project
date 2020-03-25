import pygame

def blackbody_visable_colour(tempriture):
    redIntensity = 1
    greenIntensity = 1
    blueIntensity = 1

    maxColouredWavelength = max((redIntensity, greenIntensity, blueIntensity))

    return pygame.Color(int(255 * redIntensity / maxColouredWavelength),
                        int(255 * greenIntensity / maxColouredWavelength),
                        int(255 * blueIntensity / maxColouredWavelength))