import numpy as np
import copy
from matplotlib import pyplot as plt
from simulation import Simulation
from simulation.entities.entity import Entity
from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Logger(object):
    def __init__(self, entities: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entities = entities
        self.__time = [0]

    def _getEntities(self):
        return self.__entities
    
    def getEntities(self):
        return self.__entities.copy()

    def _getTime(self):
        return self.__time

    def getTime(self):
        return self.__time.copy()

    def log(self, sim: Simulation, delta_t: float):
        self.__time.append(self.__time[-1] + delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        self.__time = [self.__time[-1] if not set_time_to_zero else 0]



class ActionLogger(Logger):
    def __init__(self, entities: dict, trigger = lambda self, sim, delta_t: False, action = lambda self, sim: 0, zero_time_on_action: bool = False, *args, **kwargs):
        super().__init__(entities = entities, *args, **kwargs)
        self.__trigger = trigger
        self.__zero_time_on_action = zero_time_on_action
        self.__action = action

    def log(self, sim: Simulation, delta_t: float):
        super().log(sim, delta_t)

        if self.__trigger(self, sim, delta_t):
            self.action(sim)
            self.resetLog(self.__zero_time_on_action)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)

    def action(self, sim: Simulation):
        self.__action(sim)



class PositionLogger(ActionLogger):
    def __init__(self, entity: Moveable, trigger = lambda self, sim, delta_t: False, zero_time_on_action: bool = False, *args, **kwargs):
        self.__positions = [copy.copy(entity.getLocation())]
        super().__init__(entities = {"entity":entity}, trigger = trigger, action = self.__customAction, zero_time_on_action = zero_time_on_action, *args, **kwargs)

    def log(self, sim: Simulation, delta_t: float):
        self.__positions.append(copy.copy(self._getEntities()["entity"].getLocation()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        self.__positions = [self.__positions[-1]]

    def __customAction(self, sim: Simulation):
        sim.pause()

        distance = []
        x = []
        y = []
        z = []
        t = self._getTime()

        for position in self.__positions:
            distance.append(position.magnitude())
            x.append(position.x)
            y.append(position.y)
            z.append(position.z)
        
        plt.plot(t, x, color = "blue", label = "X Position")
        plt.plot(t, y, color = "orange", label = "Y Position")
        plt.plot(t, z, color = "green", label = "Z Position")
        plt.xlabel("Time (s)")
        plt.ylabel("Component Displacement (m)")
        plt.legend()
        plt.show()
        
        plt.plot(x, z)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        plt.show()
        
        plt.plot(t, distance)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        plt.show()
        
        sim.resume()



class VelocityLogger(ActionLogger):
    def __init__(self, entity: FreeBody, trigger = (lambda self, sim, delta_t: False), zero_time_on_action: bool = False, *args, **kwargs):
        self.__velocities = [copy.copy(entity.getVelocity())]
        super().__init__(entities = {"entity":entity}, trigger = trigger, action = self.__customAction, zero_time_on_action = zero_time_on_action, *args, **kwargs)

    def log(self, sim: Simulation, delta_t: float):
        self.__velocities.append(copy.copy(self._getEntities()["entity"].getVelocity()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        self.__velocities = [self.__velocities[-1]]

    def __customAction(self, sim: Simulation):
        sim.pause()

        speed = []
        x = []
        y = []
        z = []
        t = self._getTime()

        for velocity in self.__velocities:
            speed.append(np.abs(velocity.magnitude()))
            x.append(velocity.x)
            y.append(velocity.y)
            z.append(velocity.z)
        
        plt.plot(t, x, color = "blue", label = "X Velocity")
        plt.plot(t, y, color = "orange", label = "Y Velocity")
        plt.plot(t, z, color = "green", label = "Z Velocity")
        plt.xlabel("Time (s)")
        plt.ylabel("Component Velocity ($ms^{-1}$)")
        plt.legend()
        plt.show()
        
        plt.plot(x, z)
        plt.xlabel("X Velocity (m)")
        plt.ylabel("Z Velocity (m)")
        plt.show()
        
        plt.plot(t, speed)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed ($ms^{-1}$)")
        plt.show()
        
        sim.resume()



class SeperationLogger(ActionLogger):
    def __init__(self, entity: Moveable, referenceEntity: Moveable, trigger = lambda self, sim, delta_t: False, zero_time_on_action: bool = False, *args, **kwargs):
        self.__positions = {"entity":[copy.copy(entity.getLocation())], "reference_entity":[copy.copy(referenceEntity.getLocation())]}
        super().__init__(entities = {"entity":entity, "reference_entity":referenceEntity}, trigger = trigger, action = self.__customAction, zero_time_on_action = zero_time_on_action, *args, **kwargs)

    def log(self, sim: Simulation, delta_t: float):
        self.__positions["entity"].append(copy.copy(self._getEntities()["entity"].getLocation()))
        self.__positions["reference_entity"].append(copy.copy(self._getEntities()["reference_entity"].getLocation()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        self.__positions["entity"] = [self.__positions["entity"][-1]]
        self.__positions["reference_entity"] = [self.__positions["reference_entity"][-1]]

    def __customAction(self, sim: Simulation):
        sim.pause()

        distance = []
        displacement_x = []
        displacement_y = []
        displacement_z = []
        t = self._getTime()

        for i in range(len(t)):
            entityLocation = self.__positions["entity"][i]
            referenceLocation = self.__positions["reference_entity"][i]

            displacement = entityLocation - referenceLocation
            distance.append(displacement.magnitude())
            displacement_x.append(displacement.x)
            displacement_y.append(displacement.y)
            displacement_z.append(displacement.z)

        plt.plot(t, displacement_x, color = "blue", label = "X Displacement")
        plt.plot(t, displacement_y, color = "orange", label = "Y Displacement")
        plt.plot(t, displacement_z, color = "green", label = "Z Displacement")
        plt.xlabel("Time (s)")
        plt.ylabel("Seperation Component Displacement (m)")
        plt.legend()
        plt.show()
        
        plt.plot(displacement_x, displacement_z)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        plt.show()

        plt.plot(t, distance)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        plt.show()
        
        sim.resume()