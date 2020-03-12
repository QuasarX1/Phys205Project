import pygame
from matplotlib import pyplot as plt
import simulation as sim
from star import Star

simulation = sim.Simulation()

#simulation.getCamera().setLocation(pygame.Vector3(0, 200, 0))
#simulation.getCamera().setFacing(pygame.Vector3(0, -1, 0))
#simulation.getCamera().setVertical(pygame.Vector3(0, 0, 1))

simulation.getCamera().setLocation(pygame.Vector3(0, 0, -200))

HUD = sim.layer.Layer_2D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("HUD", HUD)

simulation_layer = sim.layer.Layer_3D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("simulation_layer", simulation_layer)

target_star = Star(radius = 100,
                   temperature = 100,
                   mass = 10000000000000000000,#1.9891 * 10**30,#500000,
                   initial_velocity = pygame.Vector3(0, 0, 0),
                   location = pygame.Vector3(-200, 0, 0))
simulation_layer.addEntity("target_star", target_star)

test_star = Star(radius = 10,
                 temperature = 100,
                 mass = 10000,#1.9891 * 10**30,#500000,
                 initial_velocity = pygame.Vector3(0, 0, 80),
                 location = pygame.Vector3(400, 0, 0))
simulation_layer.addEntity("test_star", test_star)

target_star.bindEntity_by_name("test_star", simulation_layer)
test_star.bindEntity_by_name("target_star", simulation_layer)

#TODO: add a planet

class PositionLog(object):
    def __init__(self, entity):
        self.x = [test_star.getLocation().x]
        self.z = [test_star.getLocation().z]
        self.t = [0]

        self.entity = entity

    def logPositions(self, sim, delta_t):
        self.x.append(self.entity.getLocation().x)
        self.z.append(self.entity.getLocation().z)
        self.t.append(self.t[-1] + delta_t)

        if len(self.t) > 100:
            sim.pause()

            plt.plot(self.x, self.t)
            plt.plot(self.z, self.t)
            plt.show()

            plt.plot(self.x, self.z)
            plt.show()

            self.x = [self.entity.getLocation().x]
            self.z = [self.entity.getLocation().z]
            self.t = [0]

            #input("Press enter to run next chunk... ")
            sim.resume()

logger = PositionLog(test_star)

simulation.onItterationEnd = logger.logPositions

simulation.run()