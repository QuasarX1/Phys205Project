import pygame
from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Star(FreeBody, Sphere):
    def __init__(self, radius, mass, temperature, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        self.__temperature = temperature
        colour = pygame.Color(R, G, B)#TODO: calculate the colour from Temp

        super().__init__(mass = mass, moment_of_inertia = 0, radius = radius, location = location, facing = facing, vertical = vertical, colour = colour, **kwargs)
        #TODO: change moment of inertia
    
    def getTemperature(self):
        return self.__temperature

    def setTemperature(self, new_temperature: float):
        self.__temperature = new_temperature

    #def setColour(self, wavelength):
    #    return:
    #        if wavelength > 700:
    #            R = 1
    #            G = 0
    #            B = 0
    #        elif 640 < wavelength =< 700:
    #            R = 1
    #            G = ((700 - wavelength) / 60)
    #            B = 0
    #        elif 580 < wavelength =< 640:
    #            R = ((wavelength - 580) / 60)
    #            G = 1
    #            B = 0
    #        elif 520 < wavelength =< 580:
    #            R = 0
    #            G = 1
    #            B = ((580 - wavelength) / 60)
    #        elif 460 < wavelength =< 520:
    #            R = 0
    #            G = ((wavelength - 460) / 60)
    #            B = 1
    #        elif 400 < wavelength =< 460:
    #            R = ((460 - wavelength) / 60)
    #            G = 0
    #            B = 1

def setColour(self, wavelength):
    maxColouredWavelength = max(Rintensity, Gintensity, Bintesnity)
    return:
        R = 255 * Rintensity / maxColouredWavelength
        G = 255 * Gintensity / maxColouredWavelength
        B = 255 * Bintensity / maxColouredWavelength


    def update(self, delta_t):#TODO: star updates here? or in free body?
        self.manual_update_FreeBody(delta_t)