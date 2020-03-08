import pygame
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
                   tempriture = 100,
                   mass = 10000000000000000000,#1.9891 * 10**30,#500000,
                   initial_velocity = pygame.Vector3(0, 0, 0),
                   location = pygame.Vector3(-200, 0, 0))
simulation_layer.addEntity("target_star", target_star)

test_star = Star(radius = 10,
                 tempriture = 100,
                 mass = 10000,#1.9891 * 10**30,#500000,
                   initial_velocity = pygame.Vector3(0, 0, -30),
                 location = pygame.Vector3(200, 0, 0))
simulation_layer.addEntity("test_star", test_star)

target_star.bindEntity_by_name("test_star", simulation_layer)
test_star.bindEntity_by_name("target_star", simulation_layer)

#TODO: add a planet

simulation.run()