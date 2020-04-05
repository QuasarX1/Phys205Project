import pygame
import numpy as np
from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.freeBody import FreeBody
from simulation.graphics.HUD.text import Text, UpdatingText

class Camera(FreeBody, Moveable):
    def __init__(self, dimentions: pygame.Vector2 = pygame.Vector2(500, 500), field_of_vision: float = np.pi / 2, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(0, 0, 1), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), *args, **kwargs):
        super().__init__(mass = 1, moment_of_inertia = 0, location = location, facing = facing, vertical = vertical, *args, **kwargs)
        self.__width: float = dimentions.x
        self.__height: float = dimentions.y
        self.__fov: float = field_of_vision
        self.__focus_distance: float = None
        self.__setFov()
        self.__renderHeightOffset = None
        self.__movementForce = 1300# Newtons
        self.__resistanceToMovementForce = 1000# Newtons

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

    def getNetForce(self):
        return self.__movementForce - self.__resistanceToMovementForce

    def setNetForce(self, new_net_force):
        self.__movementForce = self.__resistanceToMovementForce + np.abs(new_net_force)

    def getHeightOffset(self):
        if self.__renderHeightOffset is None:
            raise NotImplementedError("setHeightOffset has not yet been called. It must be called at least once!")

        return self.__renderHeightOffset

    def setHeightOffset(self, windowHeight: int, distanceScale: float):
        self.__renderHeightOffset = (self.__height * distanceScale - windowHeight) / 2

    def calculatePerspective(self, location: pygame.Vector3):
        ratio = self.__focus_distance / (location - self.getFocus()).dot(self.getFacing())

        return pygame.Vector2(location.dot(self.getHorisontal()) * ratio, location.dot(self.getVertical()) * ratio)

    def isInView(self, point: pygame.Vector3):
        locationToPoint = point - self.getLocation()
        focusToPoint = point - self.getFocus()

        inView = True
        inView &= locationToPoint.dot(self.getFacing()) > 0# In front of the camera

        try:
            inView &= np.abs(focusToPoint.dot(self.getFacing()) / locationToPoint.dot(self.getHorisontal())) > np.abs(2 * self.__focus_distance / self.__width)# Right of left fov bound and Left of right fov bound
        except ZeroDivisionError:
            inView &= True

        try:
            inView &= np.abs(focusToPoint.dot(self.getFacing()) / locationToPoint.dot(self.getVertical())) > np.abs(2 * self.__focus_distance / self.__height)# Above lower fov bound and Below upper fov bound
        except ZeroDivisionError:
            inView &= True

        return inView


    def pre_update(self):
        keys = pygame.key.get_pressed()

        forewards = 0
        if keys[pygame.K_w]:
            forewards += 1
        if keys[pygame.K_s]:
            forewards -= 1

        vertical = 0
        if keys[pygame.K_SPACE]:
            vertical += 1
        if keys[pygame.K_LSHIFT]:
            vertical -= 1

        strafe = 0
        if keys[pygame.K_d]:
            strafe += 1
        if keys[pygame.K_a]:
            strafe -= 1

        if forewards != 0 or vertical != 0 or strafe != 0:
            self.addForce((self.getFacing() * forewards + self.getVertical() * vertical + self.getHorisontal() * strafe).normalize() * self.__movementForce)

        currentVelocity = self.getVelocity()
        if currentVelocity != pygame.Vector3(0, 0, 0):
            self.addForce(currentVelocity.normalize() * -1 * self.__resistanceToMovementForce)


    def update(self, delta_t, simulation):
        self.manual_update_FreeBody(delta_t, simulation) 
        
        if self.getVelocity().magnitude() < 10:
            self.setVelocity(pygame.Vector3(0, 0, 0))

        mouseDeltaX, mouseDeltaY = pygame.mouse.get_rel()
        if mouseDeltaY != 0:
            self.rotate_altitude((mouseDeltaY / self.__focus_distance) * 180 / np.pi)
        if mouseDeltaX != 0:
            self.rotate_azimuth((-mouseDeltaX / self.__focus_distance) * 180 / np.pi)



class CameraForceDisplay(UpdatingText):
    def __init__(self, camera: Camera,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        self.__camera = camera
        super().__init__(function = lambda self: str(self.getReferencedObject("camera").getNetForce()),
                         font_face = "freesansbold.ttf", size = 30, objectReferences = {"camera":camera},
                         location = location, facing = facing, vertical = vertical, colour = colour, *args, **kwargs)



class CameraSpeedDisplay(UpdatingText):
    def __init__(self, camera: Camera,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        self.__camera = camera
        super().__init__(function = lambda self: str(self.getReferencedObject("camera").getVelocity().magnitude()),
                         font_face = "freesansbold.ttf", size = 30, objectReferences = {"camera":camera},
                         location = location, facing = facing, vertical = vertical, colour = colour, *args, **kwargs)