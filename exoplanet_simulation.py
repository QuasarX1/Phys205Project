import pygame
import simulation as sim
from star import Star

simulation = sim.Simulation()

simulation.getCamera().setLocation(pygame.Vector3(0, 0, -200))

HUD = sim.layer.Layer_2D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("HUD", HUD)

simulation_layer = sim.layer.Layer_3D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("simulation_layer", simulation_layer)


simulation_layer.addEntity("target_star", Star(radius = 100,
                                               tempriture = 100,
                                               mass = 500000,
                                               location = pygame.Vector3(0, 0, 0)))

#TODO: add a planet

simulation.run()