import pygame
from simulation.entities.renderable import Renderable_3DWireframe, Renderable_3DSolid

class UnitCube_Wireframe(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs) -> Renderable_3DWireframe:
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
            vertical,
            scale,
            colour,
            **kwargs)



class TriangularPyrimid_Wireframe(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs) -> Renderable_3DWireframe:
        super().__init__(
            [pygame.Vector3(0, 2/3, 0),# top
            #pygame.Vector3(2/3, 0, 0),# front
            pygame.Vector3(5/3, 0, 0),# front
            pygame.Vector3(0.5, 0, -1/3),# back left
            pygame.Vector3(-0.5, 0, -1/3)],# back right
            
            [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],

            location,
            facing,
            vertical,
            scale,
            colour,
            **kwargs)



class Sphere(Renderable_3DSolid):
    def __init__(self, radius, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        vertices = None
        edges = None
        super().__init__(vertices, edges, location, facing, vertical, radius, colour, **kwargs)
    
    def getRadius(self):
        return self.getScaleFactor()

    def setRadius(self, new_radius: float):
        self.setScaleFactor(new_radius)