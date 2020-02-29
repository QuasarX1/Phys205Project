import pygame
from simulation.entities.moveable import Moveable

class FreeBody(Moveable):
    def __init__(self, mass, moment_of_inertia,
                 initial_velocity = 0, initial_angular_velocity = 0,
                 acceleration = 0, initial_angular_acceleration = 0,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 **kwargs):
        super().__init__(location, facing, vertical, **kwargs)