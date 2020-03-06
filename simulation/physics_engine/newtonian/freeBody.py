import pygame
from simulation.entities.moveable import Moveable

class FreeBody(Moveable):
    def __init__(self, mass, moment_of_inertia,
                 initial_velocity = 0, initial_angular_velocity = 0,
                 acceleration = 0, initial_angular_acceleration = 0,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 **kwargs):
        self.__mass = mass
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def getMass(self):
        return self.__mass

    def setMass(self, new_mass: float):
        self.__mass = new_mass