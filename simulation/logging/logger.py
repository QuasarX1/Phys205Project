import numpy as np
import copy
import os
import datetime
import shutil
from matplotlib import pyplot as plt
from simulation import Simulation
from simulation.entities.entity import Entity
from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.freeBody import FreeBody

class Logger(object):
    def __init__(self, entities: dict, **kwargs):
        super().__init__(**kwargs)
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
    def __init__(self, entities: dict, trigger = lambda self, sim, delta_t: False, action = lambda self, sim: 0, zero_time_on_action: bool = False, **kwargs):
        super().__init__(entities = entities, **kwargs)
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



class GraphingLogger(ActionLogger):
    def __init__(self, name: str, runID: str, show_graphs = True, file_save_path = None, **kwargs):
        self.__showGraphs = show_graphs
        self.__filepath = file_save_path
        self.__runID = runID
        if self.__filepath is not None:
            try:
                shutil.rmtree(os.path.join(self.__filepath, "graphing_output/{}".format(runID)))
            except: pass
            try:
                os.mkdir(os.path.join(self.__filepath, "graphing_output"))
            except: pass
            self.__filepath = os.path.join(self.__filepath, "graphing_output/{}".format(runID))
            os.mkdir(self.__filepath)

        super().__init__(**kwargs)

    def getFilepath(self):
        return self.__filepath

    def getShowGraphs(self):
        return self.__showGraphs

    def getRunID(self):
        return self.__runID



class PositionLogger(GraphingLogger):
    def __init__(self, entity: Moveable, name = "Position_Logger", runID = "run", **kwargs):
        self.__positions = [copy.copy(entity.getLocation())]
        super().__init__(name = name, runID = runID, entities = {"entity":entity}, action = self.__customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement"))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Distance_Over_Time"))

    def log(self, sim: Simulation, delta_t: float):
        self.__positions.append(copy.copy(self._getEntities()["entity"].getLocation()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        self.__positions = [self.__positions[-1]]

    def __customAction(self, sim: Simulation):
        sim.pause()

        filepath = self.getFilepath()

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
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "Component_Displacement/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        
        plt.plot(x, z)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "X_Z_Plane/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        plt.plot(t, distance)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "Distance_Over_Time/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        sim.resume()



class VelocityLogger(ActionLogger):
    def __init__(self, entity: FreeBody, name = "Velocity_Logger", runID = "run", **kwargs):
        self.__velocities = [copy.copy(entity.getVelocity())]
        super().__init__(name = name, runID = runID, entities = {"entity":entity}, action = self.__customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Velocity"))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Velocity_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Speed_Over_Time"))
        
        
        
        
        #self.__showGraphs = show_graphs
        #self.__filepath = file_save_path
        #if self.__filepath is not None:
        #    try:
        #        shutil.rmtree(os.path.join(self.__filepath, "graphing_output"))
        #    except: pass

        #    os.mkdir(os.path.join(self.__filepath, "graphing_output"))
        #    os.mkdir(os.path.join(self.__filepath, "graphing_output/Velocity_Log_Component_Velocity"))
        #    os.mkdir(os.path.join(self.__filepath, "graphing_output/Velocity_Log_X_Z_Velocity_Plane"))
        #    os.mkdir(os.path.join(self.__filepath, "graphing_output/Velocity_Log_Speed_Over_Time"))

        #self.__velocities = [copy.copy(entity.getVelocity())]
        #super().__init__(entities = {"entity":entity}, trigger = trigger, action = self.__customAction, zero_time_on_action = zero_time_on_action, *args, **kwargs)

    def log(self, sim: Simulation, delta_t: float):
        self.__velocities.append(copy.copy(self._getEntities()["entity"].getVelocity()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        self.__velocities = [self.__velocities[-1]]

    def __customAction(self, sim: Simulation):
        sim.pause()

        filepath = self.getFilepath()

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
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "Component_Velocity/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        plt.plot(x, z)
        plt.xlabel("X Velocity (m)")
        plt.ylabel("Z Velocity (m)")
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "X_Z_Velocity_Plane/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        plt.plot(t, speed)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed ($ms^{-1}$)")
        if filepath is not None:
            plt.savefig(os.path.join(filepath, "graphing_output/Velocity_Log_Speed_Over_Time/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        sim.resume()



class SeperationLogger(ActionLogger):
    def __init__(self, entity: Moveable, referenceEntity: Moveable, name = "Seperation_Logger", runID = "run", **kwargs):
        self.__positions = {"entity":[copy.copy(entity.getLocation())], "reference_entity":[copy.copy(referenceEntity.getLocation())]}
        super().__init__(name = name, runID = runID, entities = {"entity":entity, "reference_entity":referenceEntity}, action = self.__customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement"))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Distance_Over_Time"))
    
    #def __init__(self, entity: Moveable, referenceEntity: Moveable, trigger = lambda self, sim, delta_t: False, zero_time_on_action: bool = False, show_graphs = True, file_save_path = None, *args, **kwargs):
    #    self.__showGraphs = show_graphs
    #    self.__filepath = file_save_path
    #    if self.__filepath is not None:
    #        try:
    #            shutil.rmtree(os.path.join(self.__filepath, "graphing_output"))
    #        except: pass

    #        os.mkdir(os.path.join(self.__filepath, "graphing_output"))
    #        os.mkdir(os.path.join(self.__filepath, "graphing_output/Seperation_Log_Component_Displacement"))
    #        os.mkdir(os.path.join(self.__filepath, "graphing_output/Seperation_Log_X_Z_Plane"))
    #        os.mkdir(os.path.join(self.__filepath, "graphing_output/Seperation_Log_Distance_Over_Time"))

    #    self.__positions = {"entity":[copy.copy(entity.getLocation())], "reference_entity":[copy.copy(referenceEntity.getLocation())]}
    #    super().__init__(entities = {"entity":entity, "reference_entity":referenceEntity}, trigger = trigger, action = self.__customAction, zero_time_on_action = zero_time_on_action, *args, **kwargs)

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

        filepath = self.getFilepath()

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
        if self.filepath is not None:
            plt.savefig(os.path.join(self.filepath, "Component_Displacement/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        plt.plot(displacement_x, displacement_z)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        if self.filepath is not None:
            plt.savefig(os.path.join(self.filepath, "X_Z_Plane/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()

        plt.plot(t, distance)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        if self.filepath is not None:
            plt.savefig(os.path.join(self.filepath, "Distance_Over_Time/{}.png".format(datetime.datetime.now().strftime("%Y %m %d %H %M %S %f"))))
        if self.getShowGraphs():
            plt.show()
        else:
            plt.clf()
        
        sim.resume()