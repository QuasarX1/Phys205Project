import pygame
from simulation.entities.moveable import Moveable

class Renderable_Simple2DRect(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 width: float = 10, height: float = 10, colour: pygame.Color = pygame.Color(255, 255, 255)):
        super().__init__(location, facing)
        self.__width = width
        self.__height = height
        self.__colour = colour

        self.__rect_casche = None
        self.__generateRect()

    @staticmethod
    def createFromRect(rect: pygame.Rect, facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), colour: pygame.Color = pygame.Color(255, 255, 255)):
        entity = Renderable_Simple2DRect(facing = facing, colour = colour)
        entity.setRect(rect)
        return entity

    def __generateRect(self):
        loc = self.getLocation()
        self.__rect_casche = pygame.Rect(loc.x - self.__width / 2, loc.y - self.__height / 2, self.__width, self.__height)

    def move(self, displacement_vector: pygame.Vector3):
        super().move(displacement_vector)
        self.__generateRect()

    def getWidth(self):
        self.__width

    def setWidth(self, new_width: float):
        self.__width = new_width
        self.__generateRect()

    def getHeight(self):
        return self.__height

    def setHeight(self, new_height: float):
        self.__height = new_height
        self.__generateRect()
        
    def getRect(self) -> pygame.Rect:
        return self.__rect_casche

    def setRect(self, new_rect: pygame.Rect):
        self.__rect_casche = new_rect
        self.__width = new_rect.width
        self.__height = new_rect.height
        self.setLocation(pygame.Vector3(new_rect.x + new_rect.width / 2, new_rect.y + new_rect.height / 2, self.getLocation().z))

    def getColour(self) -> pygame.Color:
        return self.__colour

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.__colour, self.__rect_casche)



class Renderable_3DWireframe(Moveable):
    pass



class Renderable_3DSolid(Moveable):
    pass