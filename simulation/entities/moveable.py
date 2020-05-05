
import copy
import numpy as np
import pygame

from simulation.entities.entity import Entity

class Moveable(Entity):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        super().__init__(**kwargs)
        self.__centre: pygame.Vector3 = location
        self.__facing: pygame.Vector3 = facing.normalize()
        self.__vertical: pygame.Vector3 = vertical.normalize()

    def getLocation(self) -> pygame.Vector3:
        return self.__centre

    def setLocation(self, new_location: pygame.Vector3):
        self.__centre = new_location

    def getFacing(self) -> pygame.Vector3:
        return self.__facing

    def setFacing(self, new_direction: pygame.Vector3):
        self.__facing = new_direction.normalize()

    def getVertical(self) -> pygame.Vector3:
        return self.__vertical

    def setVertical(self, new_direction: pygame.Vector3):
        self.__vertical = new_direction.normalize()

    def getHorisontal(self):
        return self.__vertical.cross(self.__facing).normalize()
        #return self.__facing.cross(self.__vertical).normalize()

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

    def move_upwards(self, displacement: float):
        self.move(self.__vertical * displacement)

    def move_right(self, displacement: float):
        self.move(self.getHorisontal() * displacement)

    def rotate_azimuth(self, angle):
        """
        Angle in degrees
        """
        self.__facing.rotate_ip(angle, self.__vertical)# function signiture back to front on docs for 2.0

    def rotate_altitude(self, angle):
        """
        Angle in degrees
        """
        axis = self.getHorisontal()
        self.__facing.rotate_ip(angle, axis)# function signiture back to front on docs for 2.0
        self.__vertical.rotate_ip(angle, axis)# function signiture back to front on docs for 2.0

    def rotate_roll(self, angle):
        """
        Angle in degrees
        """
        self.__vertical.rotate_ip(angle, self.__facing)# function signiture back to front on docs for 2.0