import pygame
import numpy as np
from simulation.entities.moveable import Moveable

class Camera(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(0, 0, 1), dimentions: pygame.Vector2 = pygame.Vector2(500, 500), field_of_vision: float = np.pi / 2):
        super().__init__(location, facing)
        self.__width: float = dimentions.x
        self.__height: float = dimentions.y
        self.__fov: float = field_of_vision
        self.__focus_distance: float = float(self.__width / 2 / np.tan(self.__fov / 2))

    def getFov(self) -> float:
        return self.__fov

    def setFov(self, new_field_of_vision: float):
        self.__fov = new_field_of_vision
        self.__focus_distance = float(self.__width / 2 / np.tan(self.__fov / 2))

    def getWidth(self) -> float:
        return self.__width

    def setWidth(self, new_width: float):
        self.__width = new_width
        self.__focus_distance = float(self.__width / 2 / np.tan(self.__fov / 2))

    def getHeight(self) -> float:
        return self.__height

    def setHeight(self, new_height: float):
        self.__height = new_height

    def calculatePerspective(self, location: pygame.Vector3):
        result = location * self.__focus_distance / (location.z - (self.getLocation() - (self.__focus_distance * self.getFacing())).z)
        return pygame.Vector2(result.x, result.y)