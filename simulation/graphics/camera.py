import numpy as np
import pygame

from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.freeBody import FreeBody



class Line(object):
    def __init__(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dz = p2.z - p1.z

        if dx != 0:
            self.dl_by_dx = np.sqrt(1 + (dy / dx)**2 + (dz / dx)**2) * dx / np.abs(dx)
        else:
            self.dl_by_dx = np.inf
        if dy != 0:
            self.dl_by_dy = np.sqrt(1 + (dx / dy)**2 + (dz / dy)**2) * dy / np.abs(dy)
        else:
            self.dl_by_dy = np.inf
        if dz != 0:
            self.dl_by_dz = np.sqrt(1 + (dx / dz)**2 + (dy / dz)**2) * dz / np.abs(dz)
        else:
            self.dl_by_dz = np.inf



class Ray(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.projectionVector = pygame.Vector2(self.dl_by_dz / self.dl_by_dx, self.dl_by_dz / self.dl_by_dy)

    def projection(self, delta_z):
        return delta_z * self.projectionVector



class Camera(FreeBody, Moveable):
    def __init__(self, dimentions: pygame.Vector2 = pygame.Vector2(500, 500), field_of_vision: float = np.pi / 2, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(0, 0, 1), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), *args, **kwargs):
        super().__init__(mass = 1, moment_of_inertia = 0, location = location, facing = facing, vertical = vertical, *args, **kwargs)
        self.__width: float = dimentions.x
        self.__height: float = dimentions.y
        self.__fov: float = field_of_vision
        self.__focus_distance: float = None
        self.__setFov()
        self.__renderHeightOffset = None
        self.__movementForce = 13000# Newtons
        self.__resistanceToMovementForce = 10000# Newtons

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
        translation = pygame.Vector2(self.getLocation().x + self.getWidth() / 2, self.getLocation().y + self.getHeight() / 2)
        #ray = Ray(self.getFocus(), location)
        location = location - self.getLocation()
        ray = Ray(pygame.Vector3(0, 0, -self.__focus_distance),
                  pygame.Vector3(location.dot(self.getHorisontal()), location.dot(self.getVertical()), location.dot(self.getFacing())))
        return ray.projection(self.__focus_distance) + translation

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
            vertical -= 1
        if keys[pygame.K_LSHIFT]:
            vertical += 1

        strafe = 0
        if keys[pygame.K_a]:
            #strafe -= 1
            strafe += 1
        if keys[pygame.K_d]:
            #strafe += 1
            strafe -= 1

        if forewards != 0:
            self.addForce((self.getFacing() * forewards).normalize() * self.__movementForce)
        if vertical != 0 or strafe != 0:
            self.addForce((self.getVertical() * vertical + self.getHorisontal() * strafe).normalize() * self.__movementForce / 10)

        if np.abs(self.getVelocity().dot(self.getFacing())) > 0:
            self.addForce((self.getVelocity().dot(self.getFacing()) * self.getFacing()).normalize() * -1 * self.__resistanceToMovementForce)

        if np.abs(self.getVelocity().dot(self.getHorisontal())) > 0:
            self.addForce((self.getVelocity().dot(self.getHorisontal()) * self.getHorisontal()).normalize() * -1 * self.__resistanceToMovementForce / 10)

        if np.abs(self.getVelocity().dot(self.getVertical())) > 0:
            self.addForce((self.getVelocity().dot(self.getVertical()) * self.getVertical()).normalize() * -1 * self.__resistanceToMovementForce / 10)


    def update(self, delta_t, simulation):
        self.manual_update_FreeBody(delta_t, simulation) 
        
        if np.abs(self.getVelocity().dot(self.getFacing())) < 200:
            self.setVelocity(self.getVelocity() - self.getVelocity().dot(self.getFacing()) * self.getFacing())

        if np.abs(self.getVelocity().dot(self.getHorisontal())) < 30:
            self.setVelocity(self.getVelocity() - self.getVelocity().dot(self.getHorisontal()) * self.getHorisontal())

        if np.abs(self.getVelocity().dot(self.getVertical())) < 30:
            self.setVelocity(self.getVelocity() - self.getVelocity().dot(self.getVertical()) * self.getVertical())

        mouseDeltaX, mouseDeltaY = pygame.mouse.get_rel()
        if mouseDeltaY != 0:
            self.rotate_altitude((mouseDeltaY / self.__focus_distance) * 180 / np.pi)
        if mouseDeltaX != 0:
            self.rotate_azimuth((mouseDeltaX / self.__focus_distance) * 180 / np.pi)



class Camera_2D(Camera):
    def __init__(self, dimentions: pygame.Vector2 = pygame.Vector2(500, 500), *args, **kwargs):
        super().__init__(dimentions = dimentions, field_of_vision = 0.000000001, location = pygame.Vector3(0, 0, 0), facing = pygame.Vector3(0, 0, 1), vertical = pygame.Vector3(0, 1, 0), *args, **kwargs)
        self.isInView = lambda *args, **kwargs: True#TODO: overload ths instead with an actual check

    def calculatePerspective(self, location: pygame.Vector3):
        return super().calculatePerspective(location) - pygame.Vector2(self.getLocation().x + self.getWidth() / 2, self.getLocation().y + self.getHeight() / 2)




from simulation.graphics.HUD import Text, UpdatingText

class CameraPositionDisplay(UpdatingText):
    def __init__(self, camera: Camera,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        self.__camera = camera
        super().__init__(function = lambda self: "{:.2f} {:.2f} {:.2f}".format(self.getReferencedObject("camera").getLocation().x, self.getReferencedObject("camera").getLocation().y, self.getReferencedObject("camera").getLocation().z),
                         font_face = "freesansbold.ttf", size = 30, objectReferences = {"camera":camera},
                         location = location, facing = facing, vertical = vertical, colour = colour, *args, **kwargs)



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