import pygame
from simulation.entities.entity import Entity
from simulation.entities.renderable import Renderable_2D, Renderable_3D
from simulation.graphics.camera import Camera

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
        raise NotImplementedError("This method must be overridden in an inheriting class.")

    def removeEntity(self, name: str):
        if name in self.__entities.keys():
            self.__entities.pop(name, None)

    def update(self, delta_t):
        for entity in self.__entities.values():
            entity.update(delta_t)

    def render(self, surfaceOveride: pygame.Surface = None):
        raise NotImplementedError("This method must be overridden in an inheriting class.")

class Layer_2D(Layer):
    def __init__(self, surface: pygame.Surface, backgroundColour = pygame.Color(0, 0, 0, 0), canRender = True):
        super().__init__(surface, backgroundColour, canRender)

    def addEntity(self, name: str, entity: Renderable_2D):
        if not issubclass(type(entity), Renderable_2D):
            raise TypeError("The entities added to a 2D layer must be 2D renderables.")

        if name not in self._Layer__entities.keys():
            self._Layer__entities[name] = entity
        else:
            raise KeyError("An entity already exists with the name {}.".format(name))

    def render(self, surfaceOveride: pygame.Surface = None):
        if self.canRender:
            self.surface.fill(self.backgroundColour)

            for entity in self._Layer__entities.values():
                if surfaceOveride is None:
                    entity.render(self.surface)
                else:
                    entity.render(surfaceOveride)

class Layer_3D(Layer):
    def __init__(self, surface: pygame.Surface, backgroundColour = pygame.Color(0, 0, 0, 0), canRender = True):
        super().__init__(surface, backgroundColour, canRender)

    def addEntity(self, name: str, entity: Renderable_3D):
        if not issubclass(type(entity), Renderable_3D):
            raise TypeError("The entities added to a 3D layer must be 3D renderables.")

        if name not in self._Layer__entities.keys():
            self._Layer__entities[name] = entity
        else:
            raise KeyError("An entity already exists with the name {}.".format(name))

    def render(self, camera: Camera, surfaceOveride: pygame.Surface = None):
        if self.canRender:
            self.surface.fill(self.backgroundColour)

            for entity in self._Layer__entities.values():
                if surfaceOveride is None:
                    entity.render(self.surface, camera)
                else:
                    entity.render(surfaceOveride, camera)