import pygame
from simulation.layer import Layer
from simulation.entity import Entity

pygame.init()

def runExampleSim():
    class TestEntity(Entity):
        def __init__(self):
            super().__init__(pygame.Rect(0, 0, 50, 50), pygame.Color(100, 100, 100))
            self.velocity = 400
        def update(self, delta_t):
            self.setRect(self.getRect().move(delta_t * self.velocity, 0))
            if self.getRect().x > 400:
                self.setRect(pygame.Rect(400, 0, 50, 50))
                self.velocity = -400
            elif self.getRect().x < 0:
                self.setRect(pygame.Rect(0, 0, 50, 50))
                self.velocity = 400

    sim = Simulation()
    sim.getLayer("defult").addEntity("test", TestEntity())
    sim.run()

class Simulation(object):
    def __init__(self, render = True):
        self.canRender = render
        self.__layers = {"defult": Layer()}
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
                layer.render(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update(self.clock.tick(500) / 1000)

            self.render()

            if self.render:
                pygame.display.flip()
                #pygame.display.update()
                self.screen.fill((0, 0, 0))