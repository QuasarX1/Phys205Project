import pygame
from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Planet(FreeBody, Sphere):
    def __init__(self, radius, mass, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        
        super().__init__(mass = mass, moment_of_inertia = 0, radius = radius, location = location, facing = facing, vertical = vertical, colour = colour, **kwargs)
        #TODO: change moment of inertia

    def update(self, delta_t):#TODO: star updates here? or in free body?
        self.manual_update_FreeBody(delta_t)