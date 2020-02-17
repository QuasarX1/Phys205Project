import pygame
from simulation.entities.renderable import Renderable_3DWireframe

class UnitCube_Wireframe(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255)) -> Renderable_3DWireframe:
        super().__init__(
            [pygame.Vector3(-0.5, -0.5, -0.5),
            pygame.Vector3(0.5, -0.5, -0.5),
            pygame.Vector3(-0.5, 0.5, -0.5),
            pygame.Vector3(-0.5, -0.5, 0.5),
            pygame.Vector3(0.5, 0.5, -0.5),
            pygame.Vector3(-0.5, 0.5, 0.5),
            pygame.Vector3(0.5, -0.5, 0.5),
            pygame.Vector3(0.5, 0.5, 0.5)],
            
            [(0, 1), (0, 2), (0, 3), (1, 4), (1, 6), (2, 4), (2, 5), (3, 5), (3, 6), (4, 7), (6, 7), (5, 7)],

            location,
            facing,
            scale,
            colour)