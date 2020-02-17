import pygame
import numpy as np
from simulation.layer import Layer
from simulation.entities.entity import Entity
from simulation.entities.renderable import Renderable_Simple2DRect
from simulation.entities.prefabs import UnitCube_Wireframe
from simulation.graphics.transformations import vector_to_array, array_to_vector, rotationMatrix, applyTransformation

pygame.init()

def runExampleSim():
    class TestEntity1(Renderable_Simple2DRect):
        def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), width = 50, height = 50, colour = pygame.Color(100, 100, 100), speed = 100):
            super().__init__(location, facing, width, height, colour)
            self.speed = speed

        def update(self, delta_t):
            self.move_forewards(delta_t * self.speed)

            if self.getLocation().x >= 475:
                self.setLocation(pygame.Vector3(475, 25, 25))
                self.setFacing(self.getFacing() * -1)
            elif self.getLocation().x <= 25:
                self.setLocation(pygame.Vector3(25, 25, 25))
                self.setFacing(self.getFacing() * -1)

    class TestEntity2(UnitCube_Wireframe):
        def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), scale = 50, colour = pygame.Color(100, 100, 100), speed = 100):
            super().__init__(location, facing, scale, colour)
            self.speed = speed#np.abs(startSpeed)# Using np.abs returns an int32 not an int - causes an array to be produced when multyplying by a vector

        def update(self, delta_t):
            self.move_forewards(delta_t * self.speed)

            if self.getLocation().x >= 475:
                self.setLocation(pygame.Vector3(475, 25, 25))
                self.setFacing(self.getFacing() * -1)
            elif self.getLocation().x <= 25:
                self.setLocation(pygame.Vector3(25, 25, 25))
                self.setFacing(self.getFacing() * -1)

    sim = Simulation()
    sim.addLayer("test_overlay", Layer(pygame.Surface((500, 500), pygame.SRCALPHA)))

    sim.getLayer("defult").addEntity("test", TestEntity1())
    sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity2(pygame.Vector3(475, 25, 25), pygame.Vector3(-1, 0, 0), colour = pygame.Color(255, 0, 0, 175)))

    sim.run()

class Simulation(object):
    def __init__(self, render = True):
        self.canRender = render
        self.__layers = {"defult": Layer(pygame.Surface((500, 500), pygame.SRCALPHA))}
        self.clock = pygame.time.Clock()

        if self.canRender: self.screen: pygame.Surface = pygame.display.set_mode((500, 500))
        else: self.screen = None

    def getLayer(self, name: str) -> Layer:
        if name in self.__layers.keys():
            return self.__layers[name]
        else:
            return None

    def addLayer(self, name: str, layer: Layer):
        if name not in self.__layers.keys():
            self.__layers[name] = layer
        else:
            raise KeyError("A layer already exists with the name {}.".format(name))

    def removeLayer(self, name: str):
        if name in self.__layers.keys():
            self.__layers.pop(name, None)

    def update(self, delta_t):
        for layer in self.__layers.values():
            layer.update(delta_t)

    def render(self):
        if self.canRender:
            for layer in self.__layers.values():
                layer.render()
                self.screen.blit(layer.surface, (0, 0))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update(self.clock.tick(60) / 1000)

            self.render()

            if self.render:
                pygame.display.flip()
                #pygame.display.update()
                self.screen.fill((0, 0, 0))