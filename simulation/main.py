import pygame
import numpy as np
from simulation.layer import Layer
from simulation.entities.entity import Entity, Entity3D
from simulation.entities.renderable import Renderable_Simple2DRect
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
            elif self.getRect().x <= 25:
                self.setLocation(pygame.Vector3(25, 25, 25))
                self.setFacing(self.getFacing() * -1)

    class TestEntity2(Renderable_3DWireframe):
        def __init__(self, side_length = 50, centre_start: pygame.Vector3 = pygame.Vector3(25, 25, 25), facing_start = pygame.Vector3(1, 0, 0), startSpeed = 100, start_colour: pygame.Color = pygame.Color(100, 100, 100)):
            super().__init__(side_length, centre_start, facing_start, start_colour)
            self.speed = startSpeed#np.abs(startSpeed)# Using np.abs returns an int32 not an int - causes an array to be produced when multyplying by a vector

        def update(self, delta_t):
            self.setCentre(delta_t * self.speed * self.getFacing() + self.getCentre())

            if self.getCentre().x > 475:
                self.setCentre(pygame.Vector3(470, 25, 25))
                self.setFacing(-1 * self.getFacing())
            elif self.getCentre().x < 25:
                self.setCentre(pygame.Vector3(25, 25, 25))
                self.setFacing(-1 * self.getFacing())

    sim = Simulation()
    sim.addLayer("test_overlay", Layer(pygame.Surface((500, 500), pygame.SRCALPHA)))

    sim.getLayer("defult").addEntity("test", TestEntity1())
    #sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity1(450, -100, pygame.Color(255, 0, 0, 175)))
    sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity2(centre_start = pygame.Vector3(475, 25, 25), facing_start = pygame.Vector3(-1, 0, 0), start_colour = pygame.Color(255, 0, 0, 175)))

    sim.run()

#def runExampleSim():
#    class TestEntity1(Renderable_Simple2DRect):
#        def __init__(self, startLoc = 0, startVelocity = 100, startColour = pygame.Color(100, 100, 100)):
#            super().__init__(pygame.Rect(0, 0, 50, 50), startColour)
#            self.maxVelocity = np.abs(startVelocity)
#            self.velocity = startVelocity
#            self.xLocation = startLoc
#            
#        def update(self, delta_t):
#            self.xLocation = delta_t * self.velocity + self.xLocation
#            self.setRect(pygame.Rect(self.xLocation, 0, 50, 50))

#            if self.getRect().x > 450:
#                self.setRect(pygame.Rect(450, 0, 50, 50))
#                self.velocity = -self.maxVelocity
#            elif self.getRect().x < 0:
#                self.setRect(pygame.Rect(0, 0, 50, 50))
#                self.velocity = self.maxVelocity

#    class TestEntity2(Entity3D):
#        def __init__(self, side_length = 50, centre_start: pygame.Vector3 = pygame.Vector3(25, 25, 25), facing_start = pygame.Vector3(1, 0, 0), startSpeed = 100, start_colour: pygame.Color = pygame.Color(100, 100, 100)):
#            super().__init__(side_length, centre_start, facing_start, start_colour)
#            self.speed = startSpeed#np.abs(startSpeed)# Using np.abs returns an int32 not an int - causes an array to be produced when multyplying by a vector

#        def update(self, delta_t):
#            self.setCentre(delta_t * self.speed * self.getFacing() + self.getCentre())

#            if self.getCentre().x > 475:
#                self.setCentre(pygame.Vector3(470, 25, 25))
#                self.setFacing(-1 * self.getFacing())
#            elif self.getCentre().x < 25:
#                self.setCentre(pygame.Vector3(25, 25, 25))
#                self.setFacing(-1 * self.getFacing())

#    sim = Simulation()
#    sim.addLayer("test_overlay", Layer(pygame.Surface((500, 500), pygame.SRCALPHA)))

#    sim.getLayer("defult").addEntity("test", TestEntity1())
#    #sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity1(450, -100, pygame.Color(255, 0, 0, 175)))
#    sim.getLayer("test_overlay").addEntity("test_overlay_object", TestEntity2(centre_start = pygame.Vector3(475, 25, 25), facing_start = pygame.Vector3(-1, 0, 0), start_colour = pygame.Color(255, 0, 0, 175)))

#    sim.run()

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