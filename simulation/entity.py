import pygame

class Entity(object):
    def __init__(self, start_rect: pygame.Rect, start_colour: pygame.Color):
        self.__rect = start_rect
        self.__colour = start_colour

    def getRect(self) -> pygame.Rect:
        return self.__rect

    def setRect(self, newRect: pygame.Rect):
        self.__rect = newRect

    def getColour(self) -> pygame.Color:
        return self.__colour

    def update(self, delta_t):
        raise NotImplementedError("This method must be overridden in an inheriting class.")

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.getColour(), self.getRect())