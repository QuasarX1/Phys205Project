import pygame
import numpy as np

class Entity(object):
    def update(self, delta_t):
        raise NotImplementedError("This method must be overridden in an inheriting class.")



#class Entity2D(Entity):
#    def __init__(self, start_rect: pygame.Rect, start_colour: pygame.Color):
#        self.__rect = start_rect
#        self.__colour = start_colour

#    def getRect(self) -> pygame.Rect:
#        return self.__rect

#    def setRect(self, newRect: pygame.Rect):
#        self.__rect = newRect

#    def getColour(self) -> pygame.Color:
#        return self.__colour

#    def render(self, surface: pygame.Surface):
#        pygame.draw.rect(surface, self.getColour(), self.getRect())



#class Entity3D(Entity):
#    def __init__(self, side_length = 2, centre_start: pygame.Vector3 = pygame.Vector3(1, 1, 1), facing_start: pygame.Vector3 = pygame.Vector3(1, 0, 0), start_colour: pygame.Color = pygame.Color(255, 255, 255)):
#        self.__facing: pygame.Vector3 = facing_start

#        self.__centre: pygame.Vector3 = centre_start

#        #self.__vertices: list = [pygame.Vector3(0, 0, 0),
#        #                       pygame.Vector3(1, 0, 0),
#        #                       pygame.Vector3(0, 1, 0),
#        #                       pygame.Vector3(0, 0, 1),
#        #                       pygame.Vector3(1, 1, 0),
#        #                       pygame.Vector3(0, 1, 1),
#        #                       pygame.Vector3(1, 0, 1),
#        #                       pygame.Vector3(1, 1, 1)]

#        self.__vertices: list = [pygame.Vector3(-0.5 * side_length, -0.5 * side_length, -0.5 * side_length),
#                               pygame.Vector3(0.5 * side_length, -0.5 * side_length, -0.5 * side_length),
#                               pygame.Vector3(-0.5 * side_length, 0.5 * side_length, -0.5 * side_length),
#                               pygame.Vector3(-0.5 * side_length, -0.5 * side_length, 0.5 * side_length),
#                               pygame.Vector3(0.5 * side_length, 0.5 * side_length, -0.5 * side_length),
#                               pygame.Vector3(-0.5 * side_length, 0.5 * side_length, 0.5 * side_length),
#                               pygame.Vector3(0.5 * side_length, -0.5 * side_length, 0.5 * side_length),
#                               pygame.Vector3(0.5 * side_length, 0.5 * side_length, 0.5 * side_length)]

#        self.__edges: list = [(0, 1),
#                            (0, 2),
#                            (0, 3),
#                            (1, 4),
#                            (1, 6),
#                            (2, 4),
#                            (2, 5),
#                            (3, 5),
#                            (3, 6),
#                            (4, 7),
#                            (6, 7),
#                            (5, 7)]



#        self.__colour = start_colour

#    def getCentre(self):
#        return self.__centre

#    def setCentre(self, new_centre: pygame.Vector3):
#        self.__centre = new_centre

#    def getFacing(self):
#        return self.__facing

#    def setFacing(self, new_direction: pygame.Vector3):
#        self.__facing = new_direction

#    def getColour(self) -> pygame.Color:
#        return self.__colour

#    def update(self, delta_t):
#        raise NotImplementedError("This method must be overridden in an inheriting class.")

#    def render(self, surface: pygame.Surface):
#        for edge in self.__edges:
#            startPosition = self.__centre + self.__vertices[edge[0]]
#            endPosition = self.__centre + self.__vertices[edge[1]]

#            pygame.draw.line(surface,
#                             self.__colour,
#                             (startPosition.x, startPosition.y),
#                             (endPosition.x, endPosition.y))