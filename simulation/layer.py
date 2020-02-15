import pygame
from simulation.entity import Entity

class Layer(object):
    def __init__(self, canRender = True):
        self.canRender = canRender
        self.__entities = {}

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

    def render(self, screen: pygame.Surface):
        if self.canRender:
            for entity in self.__entities.values():
                entity.render(screen)