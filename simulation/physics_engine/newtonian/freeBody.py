import pygame

from simulation.entities import Moveable
from simulation.physics_engine.newtonian.forces import accelerationFromForceMass, forceBetweenTwoLargeBodies
from simulation.physics_engine.newtonian.suvat import displacement_without_final_velocity, final_velocity_without_displacement

class FreeBody(object):# Foreward declaration of FreeBody
    pass

class FreeBody(Moveable):
    def __init__(self, mass: float, moment_of_inertia: float,
                 initial_velocity: pygame.Vector3 = pygame.Vector3(0, 0, 0), initial_angular_velocity = 0,#TODO: angular a vector???
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 **kwargs):
        self.__mass = mass
        self.__momentOfInertia = moment_of_inertia
        self.__velocity = initial_velocity
        self.__angularVelocity = initial_angular_velocity

        self.__gravitationallyBoundEntities = []
        self.__forces = []

        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def getMass(self) -> float:
        return self.__mass

    def setMass(self, new_mass: float):
        self.__mass = new_mass

    def getMomentOfInertia(self) -> float:
        return self.__momentOfInertia

    def setMomentOfInertia(self, new_moment_of_inertia: float):
        self.__momentOfInertia = new_moment_of_inertia

    def getVelocity(self) -> pygame.Vector3:
        return self.__velocity

    def setVelocity(self, new_velocity: pygame.Vector3):
        self.__velocity = new_velocity

    def getAngularVelocity(self) -> float:
        return self.__mass

    def setAngularVelocity(self, new_angular_velocity: float):
        self.__angularVelocity = new_angular_velocity

    def addForce(self, force: pygame.Vector3):
        self.__forces.append(force)

    def getBoundEntities(self):
        return self.__gravitationallyBoundEntities

    def bindEntity(self, entity):
        if not isinstance(entity, FreeBody):
            raise TypeError("The entity's type did not inherit FreeBody.")

        self.__gravitationallyBoundEntities.append(entity)

    def bindEntity_by_name(self, name: str, layer):
        entity = layer.getEntity(name)

        if not isinstance(entity, FreeBody):
            raise TypeError("The entity's type did not inherit FreeBody.")

        self.__gravitationallyBoundEntities.append(entity)

    def unbindEntity(self, entity):
        if not issubclass(entity):
            raise TypeError("The entity's type did not inherit FreeBody.")
        
        self.__gravitationallyBoundEntities.remove(entity)

    def unbindEntity_by_name(self, name: str, layer):
        entity = layer.getEntity(name)

        if not issubclass(entity):
            raise TypeError("The entity's type did not inherit FreeBody.")

        self.__gravitationallyBoundEntities.remove(entity)

    def pre_update(self):
        for entity in self.__gravitationallyBoundEntities:
            radius = self.getLocation() - entity.getLocation()
            self.__forces.append(forceBetweenTwoLargeBodies(entity.getMass(), self.getMass(), radius.magnitude()) * radius.normalize())

    def update(self, delta_t, simulation):
        self.manual_update_FreeBody(delta_t, simulation)

    def manual_update_FreeBody(self, delta_t, simulation):
        netForce = pygame.Vector3(0, 0, 0)
        for force in self.__forces:
            netForce += force

        a = accelerationFromForceMass(netForce, self.__mass)
        #self.move(displacement_without_final_velocity(self.__velocity, delta_t, a))
        self.__velocity = final_velocity_without_displacement(self.__velocity, a, delta_t)
        self.move(displacement_without_final_velocity(self.__velocity, delta_t, a))

        #if self.__velocity.magnitude() < 0.01:
        #    self.__velocity = pygame.Vector3(0, 0, 0)

        self.rotate_azimuth(delta_t * self.__angularVelocity)

    def post_update(self):
        self.__forces = []