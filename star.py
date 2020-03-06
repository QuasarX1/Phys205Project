import pygame
from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Star(FreeBody, Sphere):
    def __init__(self, radius, mass, tempriture, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        self.__tempriture = tempriture
        colour = pygame.Color(255, 255, 0)#TODO: calculate the colour from Temp

        super().__init__(mass = mass, moment_of_inertia = 0, radius = radius, location = location, facing = facing, vertical = vertical, colour = colour, **kwargs)
        #TODO: change moment of inertia
    
    def getTempriture(self):
        return self.__tempriture

    def setTempriture(self, new_tempriture: float):
        self.__tempriture = new_tempriture

    #def update(self, delta_t):#TODO: star updates here? or in free body?
        #pass