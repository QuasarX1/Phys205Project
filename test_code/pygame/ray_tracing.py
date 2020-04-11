import pygame
import numpy as np

pygame.display.init()

window = pygame.display.set_mode((500, 500))

cube = [pygame.Vector3(0, 0, 0),
        pygame.Vector3(1, 0, 0),
        pygame.Vector3(0, 0, 1),
        pygame.Vector3(1, 0, 1),
        pygame.Vector3(0, 1, 0),
        pygame.Vector3(1, 1, 0),
        pygame.Vector3(0, 1, 1),
        pygame.Vector3(1, 1, 1)]

edges = [(0,1),
         (0,2),
         (1,3),
         (2,3),
         (0,4),
         (1,5),
         (2,6),
         (3,7),
         (4,5),
         (4,6),
         (5,7),
         (6,7)]

class Line(object):
    def __init__(self, p1, p2):
        self.dl_by_dx = np.sqrt(1 + ((p2.y - p1.y) / (p2.x - p1.x))**2 + ((p2.z - p1.z) / (p2.x - p1.x))**2)
        self.dl_by_dy = np.sqrt(1 + ((p2.x - p1.x) / (p2.y - p1.y))**2 + ((p2.z - p1.z) / (p2.y - p1.y))**2)
        self.dl_by_dz = np.sqrt(1 + ((p2.x - p1.x) / (p2.z - p1.z))**2 + ((p2.y - p1.y) / (p2.z - p1.z))**2)

class Ray(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.projectionVector = pygame.Vector2(self.dl_by_dz / self.dl_by_dx, self.dl_by_dz / self.dl_by_dy)

    def projection(self, delta_z):
        return delta_z * self.projectionVector

screenRadius = 1000
focusLocation = pygame.Vector3(-250, -250, -screenRadius)
projectedCube = []
for point in cube:
    p2 = point * 100
    ray = Ray(focusLocation, p2)
    projectedCube.append(ray.projection(screenRadius))


for edge in edges:
    p1_image = projectedCube[edge[0]]
    p2_image = projectedCube[edge[1]]
    pygame.draw.line(window,
                     pygame.Color(255, 255, 255),
                     (p1_image.x, p1_image.y),
                     (p2_image.x, p2_image.y))

pygame.display.flip()

input()