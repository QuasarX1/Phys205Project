import pygame
import numpy as np
from simulation.entities.moveable import Moveable

class Camera(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(0, 0, 1), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), dimentions: pygame.Vector2 = pygame.Vector2(500, 500), field_of_vision: float = np.pi / 2, **kwargs):
        super().__init__(location, facing, vertical, **kwargs)
        self.__width: float = dimentions.x
        self.__height: float = dimentions.y
        self.__fov: float = field_of_vision
        self.__focus_distance: float = None
        self.__setFov()

    def getFov(self) -> float:
        return self.__fov

    def __setFov(self):
        self.__focus_distance: float = float(self.__width / 2 / np.tan(self.__fov / 2))# This be +ve

    def setFov(self, new_field_of_vision: float):
        self.__fov = new_field_of_vision
        self.__setFov()

    def getWidth(self) -> float:
        return self.__width

    def setWidth(self, new_width: float):
        self.__width = new_width
        self.__setFov()

    def getHeight(self) -> float:
        return self.__height

    def setHeight(self, new_height: float):
        self.__height = new_height

    def getFocus(self):
        return self.getLocation() - self.__focus_distance * self.getFacing()

    #def calculatePerspective(self, location: pygame.Vector3):#TODO: upgrade perspective calculation
    #    result = location * self.__focus_distance / (location.z - (self.getLocation() - (self.__focus_distance * self.getFacing())).z)
    #    #result = (location + pygame.Vector3(self.__width / 2, self.__height / 2, 0)) * self.__focus_distance / (location.z - ((self.getLocation() + pygame.Vector3(self.__width / 2, self.__height / 2, 0)) - (self.__focus_distance * self.getFacing())).z)
    #    #result = location * self.__focus_distance / (location.z - ((self.getLocation() + pygame.Vector3(self.__width / 2, self.__height / 2, 0)) - (self.__focus_distance * self.getFacing())).z)
        
    #    focusToObject = location - self.getLocation() - (self.__focus_distance * self.getFacing())

    #    focusToObject_inFacingDirection = focusToObject.dot(self.getFacing())

    #    x_projection = self.__focus_distance * focusToObject.dot(self.getFacing()) / focusToObject_inFacingDirection
    #    y_projection = self.__focus_distance * focusToObject.dot(self.getVertical().cross(self.getFacing())) / focusToObject_inFacingDirection
        
    #    return pygame.Vector2(x_projection, y_projection)

    def calculatePerspective(self, location: pygame.Vector3):#TODO: upgrade perspective calculation
        result = location * self.__focus_distance / (location.z - (self.getLocation() - (self.__focus_distance * self.getFacing())).z)
        #result = (location + pygame.Vector3(self.__width / 2, self.__height / 2, 0)) * self.__focus_distance / (location.z - ((self.getLocation() + pygame.Vector3(self.__width / 2, self.__height / 2, 0)) - (self.__focus_distance * self.getFacing())).z)
        
        return pygame.Vector2(result.x, result.y)

    def isInView(self, point: pygame.Vector3):
        locationToPoint = point - self.getLocation()
        focusToPoint = point - self.getFocus()

        inView = True
        inView &= locationToPoint.dot(self.getFacing()) > 0# Infront of the camera
        inView &= np.abs(focusToPoint.dot(self.getFacing()) / locationToPoint.dot(self.getHorisontal())) > np.abs(2 * self.__focus_distance / self.__width)# Right of left fov bound and Left of right fov bound
        inView &= np.abs(focusToPoint.dot(self.getFacing()) / locationToPoint.dot(self.getVertical())) > np.abs(2 * self.__focus_distance / self.__height)# Above lower fov bound and Below upper fov bound
        return inView


    def update(self, delta_t):
        keys = pygame.key.get_pressed()

        forewards = 0
        if keys[pygame.K_w]:
            forewards += 1
        if keys[pygame.K_s]:
            forewards -= 1

        if forewards != 0:
            self.move_forewards(100 * forewards * delta_t)#TODO: remove hard coded velocity

        strafe = 0
        if keys[pygame.K_d]:
            strafe += 1
        if keys[pygame.K_a]:
            strafe -= 1

        if strafe != 0:
            self.move_right(100 * strafe * delta_t)#TODO: remove hard coded velocity

        mouseDeltaX, mouseDeltaY = pygame.mouse.get_rel()
        if mouseDeltaY != 0:
            self.rotate_altitude((mouseDeltaY / self.__focus_distance) * 180 / np.pi)
        if mouseDeltaX != 0:
            self.rotate_azimuth((mouseDeltaX / self.__focus_distance) * 180 / np.pi)