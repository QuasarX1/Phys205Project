import pygame
import numpy as np
from simulation.entities.entity import Entity

class Moveable(Entity):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0)):
        self.__centre: pygame.Vector3 = location
        self.__facing: pygame.Vector3 = facing

    def getLocation(self) -> pygame.Vector3:
        return self.__centre

    def setLocation(self, new_location: pygame.Vector3):
        self.__centre = new_location

    def getFacing(self) -> pygame.Vector3:
        return self.__facing

    def setFacing(self, new_direction: pygame.Vector3):
        self.__facing = new_direction / np.sqrt(newDirection.x**2 + newDirection.y**2 + newDirection.z**2)

    def move(self, displacement_vector: pygame.Vector3):
        self.__centre += displacement_vector

    def move_x(self, displacement_in_x: float):
        self.move(pygame.Vector3(displacement_in_x, 0, 0))

    def move_y(self, displacement_in_y: float):
        self.move(pygame.Vector3(0, displacement_in_y, 0))

    def move_z(self, displacement_in_z: float):
        self.move(pygame.Vector3(0, 0, displacement_in_z))

    def move_forewards(self, displacement: float):
        self.move(self.__facing * displacement)