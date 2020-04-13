import pygame
import numpy as np
from simulation.physics_engine.optics.blackbody import radiance as blackbody_luminosity

def blackbody_visable_colour(temperature):
    '''
    Uses six known RGB values and their relative wavelengths to map out an average Red, Green and Blue intensities

    This is done by using the star's temperature and the respective wavelength of each colour to get an colour intensity. 
    Then, by using their respective RGB values, which are noted to the right of each line, are summed up and divided by the total relative value
    '''
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