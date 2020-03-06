import pygame
from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.forces import accelerationFromForceMass

class FreeBody(Moveable):
    def __init__(self, mass, moment_of_inertia,
                 initial_velocity = 0, initial_angular_velocity = 0,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 **kwargs):
        self.__mass = mass
        self.__momentOfInertia = moment_of_inertia
        self.__velocity = initial_velocity
        self.__angularVelocity = initial_angular_velocity

        self.__forces = []

        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def getMass(self):
        return self.__mass

    def setMass(self, new_mass: float):
        self.__mass = new_mass

    def getMomentOfInertia(self):
        return self.__momentOfInertia

    def setMomentOfInertia(self, new_moment_of_inertia: float):
        self.__momentOfInertia = new_moment_of_inertia

    def getVelocity(self):
        return self.__velocity

    def setVelocity(self, new_velocity: float):
        self.__velocity = new_velocity

    def getAngularVelocity(self):
        return self.__mass

    def setAngularVelocity(self, new_angular_velocity: float):
        self.__angularVelocity = new_angular_velocity

    def update(self, delta_t):
        self.manual_update_FreeBody(delta_t)

    def manual_update_FreeBody(self, delta_t):
       a =  accelerationFromForceMass(sum(self.__forces), self.__mass)
