import pygame
from simulation.entity import Entity

class Layer(object):
    def __init__(self, surface: pygame.Surface, backgroundColour = pygame.Color(0, 0, 0, 0), canRender = True):
        self.canRender = canRender
        self.__entities = {}
        self.surface = surface
        self.backgroundColour = backgroundColour

    def getEntity(self, name: str):
        if name in self.__entities.keys():
            return self.__entities[name]
        else:
            return None

    def addEntity(self, name: str, entity: Entity):
        if name not in self.__entities.keys():
            self.__entities[name] = entity
        else:
            raise KeyError("An entity already exists with the name {}.".format(name))

    def removeEntity(self, name: str):
        if name in self.__entities.keys():
            self.__entities.pop(name, None)

    def update(self, delta_t):
        for entity in self.__entities.values():
            entity.update(delta_t)

    def render(self, surfaceOveride: pygame.Surface = None):
        if self.canRender:
            self.surface.fill(self.backgroundColour)

            for entity in self.__entities.values():
                if surfaceOveride is None:
                    entity.render(self.surface)
                else:
                    entity.render(surfaceOveride)