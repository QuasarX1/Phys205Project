import pygame
import numpy as np
from simulation.physics_engine.optics.blackbody import radiance as blackbody_luminosity

def blackbody_visable_colour(temperature):
    #return pygame.Color(255, 255, 255)#TODO: REMOVE THIS!!!!!!!!!!!!!
    redIntensity = blackbody_luminosity(700 * 10**-9, temperature) #    [255,0,0] 
    orangeIntensity = blackbody_luminosity(640 * 10**-9, temperature) # [255,165,0]
    yellowIntensity = blackbody_luminosity(580 * 10**-9, temperature) #   [255,255,0]
    greenIntensity = blackbody_luminosity(520 * 10**-9, temperature) #  [0,128,0]
    blueIntensity = blackbody_luminosity(460 * 10**-9, temperature) #   [0,0,255]
    purpleIntensity = blackbody_luminosity(400 * 10**-9, temperature) # [128,0,128]

    redColour = (redIntensity + orangeIntensity + yellowIntensity + ((128/255) * purpleIntensity)) / 893
    greenColour = ((128/255) * greenIntensity + (165/255) * orangeIntensity + yellowIntensity) / 548
    blueColour = (blueIntensity + (128/255) * purpleIntensity) / 483

    maxColouredWavelength = max((redColour, greenColour, blueColour))

    return pygame.Color(int(255 * redColour / maxColouredWavelength),
                        int(255 * greenColour / maxColouredWavelength),
                        int(255 * blueColour / maxColouredWavelength))