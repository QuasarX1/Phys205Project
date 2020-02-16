import pygame
import numpy as np
from simulation.layer import Layer
from simulation.entity import Entity

pygame.init()

def runExampleSim():
    class TestEntity(Entity):
        def __init__(self, startLoc = 0, startVelocity = 100, startColour = pygame.Color(100, 100, 100)):
            super().__init__(pygame.Rect(0, 0, 50, 50), startColour)
            self.maxVelocity = np.abs(startVelocity)
            self.velocity = startVelocity
            self.xLocation = startLoc
        def update(self, delta_t):
            self.xLocation = delta_t * self.velocity + self.xLocation
            self.setRect(pygame.Rect(self.xLocation, 0, 50, 50))

            if self.getRect().x > 450:
                self.setRect(pygame.Rect(450, 0, 50, 50))
                self.velocity = -self.maxVelocity
            elif self.getRect().x < 0:
                self.setRect(pygame.Rect(0, 0, 50, 50))
                self.velocity = self.maxVelocity

    sim = Simulation()
    sim.addLayer("test_overlay", Layer(pygame.Surface((500, 500), pygame.SRCALPHA)))

    sim.getLayer("defult").addEntity("test", TestEntity())
    sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity(450, -100, pygame.Color(255, 0, 0, 175)))

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