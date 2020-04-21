import pygame

from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody
from simulation.physics_engine.optics.colour import blackbody_visable_colour

class Star(FreeBody, Sphere):
    def __init__(self, radius, mass, temperature, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        self.__temperature = temperature
        colour = blackbody_visable_colour(temperature)#pygame.Color(255, 255, 0)#TODO: calculate the colour from Temp

        super().__init__(mass = mass, moment_of_inertia = 0, radius = radius, location = location, facing = facing, vertical = vertical, colour = colour, **kwargs)
        #TODO: change moment of inertia
    
    def getTemperature(self):
        return self.__temperature

    def setTemperature(self, new_temperature: float):
        self.__temperature = new_temperature

    def update(self, delta_t, simulation):#TODO: star updates here? or in free body?
        self.setColour(blackbody_visable_colour(self.__temperature))
        self.manual_update_FreeBody(delta_t, simulation)

    def bindStarSystemEntity(self, entity):
        for boundEntity in self.getBoundEntities():
            boundEntity.bindEntity(entity)
            entity.bindEntity(boundEntity)

        self.bindEntity(entity)
        entity.bindEntity(self)