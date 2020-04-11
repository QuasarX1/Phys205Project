import pygame
import numpy as np
from simulation.entities.renderable import Renderable_2D, Renderable_2DLine, Renderable_3DWireframe, Renderable_3DSolid

class UnitCube_Wireframe(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs) -> Renderable_3DWireframe:
        vertices = [pygame.Vector3(-0.5, -0.5, -0.5),
                    pygame.Vector3(0.5, -0.5, -0.5),
                    pygame.Vector3(-0.5, 0.5, -0.5),
                    pygame.Vector3(-0.5, -0.5, 0.5),
                    pygame.Vector3(0.5, 0.5, -0.5),
                    pygame.Vector3(-0.5, 0.5, 0.5),
                    pygame.Vector3(0.5, -0.5, 0.5),
                    pygame.Vector3(0.5, 0.5, 0.5)]

        edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 6), (2, 4), (2, 5), (3, 5), (3, 6), (4, 7), (6, 7), (5, 7)]
        
        super().__init__(
            vertices = vertices,
            edges = edges,
            location = location,
            facing = facing,
            vertical = vertical,
            scale = scale,
            colour = colour,
            **kwargs)

    def render(self, *args, **kwargs):
        super().render(*args, **kwargs)



class TriangularPyrimid_Wireframe(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs) -> Renderable_3DWireframe:
        vertices = [pygame.Vector3(0, 2/3, 0),# top
                    pygame.Vector3(2/3, 0, 0),# front
                    #pygame.Vector3(5/3, 0, 0),# front
                    pygame.Vector3(0.5, 0, -1/3),# back left
                    pygame.Vector3(-0.5, 0, -1/3)]# back right

        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

        super().__init__(
            vertices = vertices, edges = edges,
            location = location,
            facing = facing,
            vertical = vertical,
            scale = scale,
            colour = colour,
            **kwargs)

    def update(self, delta_t, simulation):
        pass



class Sphere(Renderable_3DSolid):
    def __init__(self, radius, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        planes = 12
        angles = 12
        
        vertices = [pygame.Vector3(0.0, -1.0, 0.0)]
        for y in np.linspace(-1.0, 1.0, planes)[1:-1]:#TODO: alter step
            planeRadius = 1 - y**2
            for phi in np.linspace(0, 2 * np.pi, angles, endpoint = False):#TODO: alter step in radians
                vertices.append(pygame.Vector3(np.cos(phi) * planeRadius, y, np.sin(phi) * planeRadius))
        vertices.append(pygame.Vector3(0.0, 1.0, 0.0))

        edges = []
        for i in range(1, angles + 1):
            edges.append((0, i))

        for index in range(1, len(vertices) - 1 - angles):
            edges.append((index, angles * (index // angles) + index % angles + 1))
            edges.append((index, index + angles))

        for i in range(angles):
            index += 1
            edges.append((index, angles * (index // angles) + index % angles + 1))

        numOfVertices = len(vertices)
        lastVertex = numOfVertices - 1
        for i in range(numOfVertices - 1 - angles, numOfVertices - 1):
            edges.append((i, lastVertex))

        super().__init__(vertices = vertices, edges = edges, location = location, facing = facing, vertical = vertical, scale = radius, colour = colour, **kwargs)
    
    def getRadius(self):
        return self.getScaleFactor()

    def setRadius(self, new_radius: float):
        self.setScaleFactor(new_radius)

    def update(self, delta_t, simulation):
        pass



class Croshair(Renderable_2D):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0.5, 0.5, 0), scale = 0.05, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(location = location, facing = pygame.Vector3(1, 0, 0), vertical = pygame.Vector3(0, 1, 0), **kwargs)
        self.__lines = [Renderable_2DLine(scale, pygame.Vector3(0, 0, 0) + location, pygame.Vector3(1, 0, 0) + location, point1_is_midpoint = True, colour = colour), Renderable_2DLine(scale, pygame.Vector3(0, 0, 0) + location, pygame.Vector3(0, 1, 0) + location, point1_is_midpoint = True, colour = colour)]

    def setLocation(self, new_location):
        self.__lines[0].move(new_location - self.getLocation())
        self.__lines[1].move(new_location - self.getLocation())
        super().setLocation(new_location)

    def render(self, surface: pygame.Surface):
        self.__lines[0].render(surface)
        self.__lines[1].render(surface)

    def update(self, delta_t, simulation):
        pass



class Croshair_3D(Renderable_3DWireframe):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0.5, 0.5, 0), facing: pygame.Vector3 = pygame.Vector3(0, 0, 1), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 0.05, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs) -> Renderable_3DWireframe:
        vertices = [pygame.Vector3(0, 0, 0),# Centre
                    pygame.Vector3(1, 0, 0),# x
                    pygame.Vector3(0, 1, 0),# y
                    pygame.Vector3(0, 0, 1)]# z

        edges = [(0, 1), (0, 2), (0, 3)]

        super().__init__(
            vertices = vertices, edges = edges,
            location = location,
            facing = facing,
            vertical = vertical,
            scale = scale,
            colour = colour,
            **kwargs)

    def update(self, delta_t, simulation):
        pass