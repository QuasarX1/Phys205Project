import pygame
from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Star(Sphere, FreeBody):
    def __init__(self, radius, mass, tempriture, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        self.__mass = mass
        self.__tempriture = tempriture
        colour = None#TODO: calculate the colour from Temp
        super().__init__(radius, location, facing, vertical, colour, **kwargs)
    
    def getMass(self):
        return self.__mass

    def setMass(self, new_mass: float):
        self.__mass = new_mass
    
    def getTempriture(self):
        return self.__tempriture

    def setTempriture(self, new_tempriture: float):
        self.__tempriture = new_tempriture