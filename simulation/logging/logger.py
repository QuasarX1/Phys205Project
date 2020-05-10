import copy
import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np
import os
import pygame
import shutil

from simulation.entities.entity import Entity
from simulation.entities.moveable import Moveable
from simulation.physics_engine.newtonian.freeBody import FreeBody

def _correctBrightColour(colour: pygame.Color):
    if np.sqrt(0.299 * colour.r**2 + 0.587 * colour.g**2 + 0.114 * colour.b**2) > 170:
        colour.r -= 75 if colour.r > 75 else colour.r
        colour.g -= 75 if colour.g > 75 else colour.g
        colour.b -= 75 if colour.b > 75 else colour.b
    
    return colour

def _correctBrightColours(colours: list):
    return [_correctBrightColour(colour) for colour in colours]

class Logger(object):
    def __init__(self, entities: dict, name: str, runID: str, file_save_path = None, **kwargs):
        super().__init__(**kwargs)
        self.__entities = entities
        self.__time = [0]
        self.__filepath = file_save_path
        self.__runID = runID
        self.__name = name

        self._initialiseOutputFolder()

    _simulationOutputFolderInitialised = False

    def _initialiseOutputFolder(self):
        if self.__filepath is not None:
            if not Logger._simulationOutputFolderInitialised:
                try:
                    shutil.rmtree(os.path.join(self.__filepath, "logging_output/{}".format(self.__runID)))
                except: pass
                try:
                    os.mkdir(os.path.join(self.__filepath, "logging_output"))
                except: pass
                try:
                    os.mkdir(os.path.join(self.__filepath, "logging_output/{}".format(self.__runID)))
                except: pass

                Logger._simulationOutputFolderInitialised = True

            self.__filepath = os.path.join(self.__filepath, "logging_output/{}/{}".format(self.__runID, self.__name))
            try:
                os.mkdir(self.__filepath)
            except:
                raise ValueError("A logger with the same name already exists!")

    def _getEntities(self):
        return self.__entities
    
    def getEntities(self):
        return self.__entities.copy()

    def _getTime(self):
        return self.__time

    def getTime(self):
        return self.__time.copy()

    def log(self, sim, delta_t: float):
        self.__time.append(self.__time[-1] + delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        self.__time = [self.__time[-1] if not set_time_to_zero else 0]

    def getFilepath(self):
        return self.__filepath

    def setFilepath(self, new_filepath):
        self.__filepath = new_filepath

    def getRunID(self):
        return self.__runID

    def getName(self):
        return self.__name

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)



class ActionLogger(Logger):
    def __init__(self, trigger = lambda self, sim, delta_t: False, action = lambda self, sim: 0, zero_time_on_action: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.__trigger = trigger
        self.__zero_time_on_action = zero_time_on_action
        self.__action = action
        self.__actionCounter = 0

    def log(self, sim, delta_t: float):
        super().log(sim, delta_t)

        if self.__trigger(self, sim, delta_t):
            self.action(sim)
            self.resetLog(self.__zero_time_on_action)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)

    def action(self, sim):
        self.__action(sim)
        self.__actionCounter += 1

    def getActionCounter(self):
        return self.__actionCounter

    @staticmethod
    def createChunkOfDataTrigger(number_of_data_points: int):
        return lambda self, sim, delta_t: len(self._getTime()) >= number_of_data_points

    @staticmethod
    def createTimePeriodTrigger(time_period: float):
        return lambda self, sim, delta_t: self._getTime()[-1] - self.getActionCounter() * time_period >= time_period



class GraphingLogger(ActionLogger):
    def __init__(self, show_graphs = True, **kwargs):
        self.__showGraphs = show_graphs

        super().__init__(**kwargs)

    def getShowGraphs(self):
        return self.__showGraphs



class PositionLogger(GraphingLogger):
    def __init__(self, entities: dict, name = "Position_Logger", **kwargs):
        self.__positions = {}

        for key in entities.keys():
            if not issubclass(type(entities[key]), Moveable):
                raise TypeError("The entity named \"{}\" was not of type \"Moveable\"".format(key))
            self.__positions[key] = [copy.copy(entities[key].getLocation())]

        super().__init__(name = name, entities = entities, action = self._customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement"))
            for key in entities.keys():
                os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement/{}".format(key)))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Distance_Over_Time"))

    def _getPositions(self):
        return self.__positions

    def log(self, sim, delta_t: float):
        for key in self.__positions.keys():
            self.__positions[key].append(copy.copy(self._getEntities()[key].getLocation()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        for key in self.__positions.keys():
            self.__positions[key] = [self.__positions[key][-1]]

    def _customAction(self, sim):
        filepath = self.getFilepath()

        distance = {}
        x = {}
        y = {}
        z = {}
        t = self._getTime()

        for key in self.__positions.keys():
            distance[key] = []
            x[key] = []
            y[key] = []
            z[key] = []
            for position in self.__positions[key]:
                distance[key].append(position.magnitude())
                x[key].append(position.x)
                y[key].append(position.y)
                z[key].append(position.z)
        
        timeStamp = datetime.datetime.now().strftime("%Y %m %d %H %M %S %f")

        plt.figure()
        for key in self.__positions.keys():
            plt.plot(t, x[key], color = "blue", label = "{} X Position".format(key))
            plt.plot(t, y[key], color = "orange", label = "{} Y Position".format(key))
            plt.plot(t, z[key], color = "green", label = "{} Z Position".format(key))
            plt.xlabel("Time (s)")
            plt.ylabel("Component Displacement (m)")
            plt.legend()
            if filepath is not None:
                temp_filePath = os.path.join(filepath, "Component_Displacement/{}/{}".format(key, timeStamp))

                plt.savefig(temp_filePath + ".png")

                csvFile = open(temp_filePath + ".csv", "x", newline = "")
                writer = csv.writer(csvFile)
                writer.writerow(["t", "x", "y", "z"])
                for i in range(len(t)):
                    writer.writerow([t[i], x[key][i], y[key][i], z[key][i]])
                csvFile.close()

            if self.getShowGraphs():
                plt.show()
            plt.clf()
            plt.close()
        
        
        plt.figure(figsize = (7, 7))
        for key in self.__positions.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(x[key], z[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(x[key], z[key], label = key)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "X_Z_Plane/{}".format(timeStamp))

            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__positions.keys():
                row.append("{} x".format(key))
                row.append("{} z".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__positions.keys():
                    row.append(x[key][i])
                    row.append(z[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()
        

        plt.figure()
        for key in self.__positions.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(t, distance[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(t, distance[key], label = key)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "Distance_Over_Time/{}".format(timeStamp))

            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__positions.keys():
                row.append("{} distance".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__positions.keys():
                    row.append(distance[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()



class VelocityLogger(GraphingLogger):
    def __init__(self, entities: dict, name = "Velocity_Logger", **kwargs):
        self.__velocities = {}

        for key in entities.keys():
            if not issubclass(type(entities[key]), FreeBody):
                raise TypeError("The entity named \"{}\" was not of type \"FreeBody\"".format(key))
            self.__velocities[key] = [copy.copy(entities[key].getVelocity())]

        super().__init__(name = name, entities = entities, action = self._customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Velocity"))
            for key in entities.keys():
                os.mkdir(os.path.join(self.getFilepath(), "Component_Velocity/{}".format(key)))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Velocity_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Speed_Over_Time"))

    def log(self, sim, delta_t: float):
        for key in self.__positions.keys():
            self.__velocities[key].append(copy.copy(self._getEntities()[key]["entity"].getVelocity()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        for key in self.__positions.keys():
            self.__velocities[key] = [self.__velocities[key][-1]]

    def _customAction(self, sim):
        filepath = self.getFilepath()

        speed = {}
        x = {}
        y = {}
        z = {}
        t = self._getTime()

        for key in self.__velocities.keys():
            speed[key] = []
            x[key] = []
            y[key] = []
            z[key] = []
            for velocity in self.__velocities[key]:
                speed[key].append(velocity.magnitude())
                x[key].append(velocity.x)
                y[key].append(velocity.y)
                z[key].append(velocity.z)
        
        timeStamp = datetime.datetime.now().strftime("%Y %m %d %H %M %S %f")

        plt.figure()
        for key in self.__velocities.keys():
            plt.plot(t, x[key], color = "blue", label = "{} X Velocity".format(key))
            plt.plot(t, y[key], color = "orange", label = "{} Y Velocity".format(key))
            plt.plot(t, z[key], color = "green", label = "{} Z Velocity".format(key))
            plt.xlabel("Time (s)")
            plt.ylabel("Component Velocity ($ms^{-1}$)")
            plt.legend()
            if filepath is not None:
                temp_filePath = os.path.join(filepath, "Component_Velocity/{}/{}".format(key, timeStamp))

                plt.savefig(temp_filePath + ".png")

                csvFile = open(temp_filePath + ".csv", "x", newline = "")
                writer = csv.writer(csvFile)
                writer.writerow(["t", "x velocity", "y velocity", "z velocity"])
                for i in range(len(t)):
                    writer.writerow([t[i], x[key][i], y[key][i], z[key][i]])
                csvFile.close()

            if self.getShowGraphs():
                plt.show()
            plt.clf()
            plt.close()
        

        plt.figure(figsize = (7, 7))
        for key in self.__velocities.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(x[key], z[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(x[key], z[key], label = key)
        plt.xlabel("X Velocity (m)")
        plt.ylabel("Z Velocity (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "X_Z_Velocity_Plane/{}".format(timeStamp))

            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__velocities.keys():
                row.append("{} x velocity".format(key))
                row.append("{} z velocity".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__velocities.keys():
                    row.append(x[key][i])
                    row.append(z[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()
        

        plt.figure()
        for key in self.__velocities.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(t, speed[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(t, speed[key], label = key)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed ($ms^{-1}$)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "Speed_Over_Time/{}".format(timeStamp))
        
            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__velocities.keys():
                row.append("{} speed".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__velocities.keys():
                    row.append(speed[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()



class SeperationLogger(PositionLogger):
    def __init__(self, entities: dict, referenceEntity: Moveable, name = "Seperation_Logger", **kwargs):
        entities["reference_entity"] = referenceEntity
        super().__init__(entities = entities, name = name, **kwargs)

    def _customAction(self, sim):
        filepath = self.getFilepath()
        positions = self._getPositions()

        distance = {}
        displacement_x = {}
        displacement_y = {}
        displacement_z = {}
        t = self._getTime()

        validKeys = [key for key in positions.keys() if key != "reference_entity"]

        for key in validKeys:
            distance[key] = []
            displacement_x[key] = []
            displacement_y[key] = []
            displacement_z[key] = []
            for i in range(len(t)):
                entityLocation = positions[key][i]
                referenceLocation = positions["reference_entity"][i]

                displacement = entityLocation - referenceLocation
                distance[key].append(displacement.magnitude())
                displacement_x[key].append(displacement.x)
                displacement_y[key].append(displacement.y)
                displacement_z[key].append(displacement.z)

        timeStamp = datetime.datetime.now().strftime("%Y %m %d %H %M %S %f")

        plt.figure()
        for key in validKeys:
            temp_filePath = os.path.join(filepath, "Component_Displacement/{}/{}".format(key, timeStamp))

            plt.plot(t, displacement_x[key], color = "blue", label = "{} X Displacement".format(key))
            plt.plot(t, displacement_y[key], color = "orange", label = "{} Y Displacement".format(key))
            plt.plot(t, displacement_z[key], color = "green", label = "{} Z Displacement".format(key))
            plt.xlabel("Time (s)")
            plt.ylabel("Seperation Component Displacement (m)")
            plt.legend()
            if filepath is not None:
                plt.savefig(temp_filePath + ".png")

                csvFile = open(temp_filePath + ".csv", "x", newline = "")
                writer = csv.writer(csvFile)
                writer.writerow(["t", "x seperation", "y seperation", "z seperation"])
                for i in range(len(t)):
                    writer.writerow([t[i], displacement_x[key][i], displacement_y[key][i], displacement_z[key][i]])
                csvFile.close()

            if self.getShowGraphs():
                plt.show()
            plt.clf()
            plt.close()
        

        plt.figure(figsize = (7, 7))
        for key in validKeys:
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(displacement_x[key], displacement_z[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(displacement_x[key], displacement_z[key], label = key)
        plt.xlabel("X Seperation (m)")
        plt.ylabel("Z Seperation (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "X_Z_Plane/{}".format(timeStamp))

            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in validKeys:
                row.append("{} x seperation".format(key))
                row.append("{} z seperation".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in validKeys:
                    row.append(displacement_x[key][i])
                    row.append(displacement_z[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()


        plt.figure()
        for key in validKeys:
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(t, distance[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(t, distance[key], label = key)
        plt.xlabel("Time (s)")
        plt.ylabel("Seperation (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "Distance_Over_Time/{}".format(timeStamp))
        
            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in validKeys:
                row.append("{} seperation".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in validKeys:
                    row.append(distance[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()



class BarycenterSeperationLogger(GraphingLogger):
    def __init__(self, star, layer, entities: dict = {}, measuredEntities: dict = {}, name = "Barycenter_Seperation_Logger", **kwargs):
        entities[layer.getEntityName(star)] = star
        for boundEntity in star.getBoundEntities():
            entities[layer.getEntityName(boundEntity)] = boundEntity
        self.__positions = {}
        self.__mass = {}
        self.__measuredEntities = measuredEntities if len(measuredEntities) > 0 else {key:1.0 for key in entities}

        for key in entities.keys():
            if not issubclass(type(entities[key]), Moveable):
                raise TypeError("The entity named \"{}\" was not of type \"Moveable\"".format(key))
            self.__positions[key] = [copy.copy(entities[key].getLocation())]
            self.__mass[key] = [copy.copy(entities[key].getMass())]

        super().__init__(name = name, entities = entities, action = self._customAction, **kwargs)

        if self.getFilepath() is not None:
            os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement"))
            for key in entities.keys():
                os.mkdir(os.path.join(self.getFilepath(), "Component_Displacement/{}".format(key)))
            os.mkdir(os.path.join(self.getFilepath(), "X_Z_Plane"))
            os.mkdir(os.path.join(self.getFilepath(), "Distance_Over_Time"))

    def _getPositions(self):
        return self.__positions

    def log(self, sim, delta_t: float):
        for key in self.__positions.keys():
            self.__positions[key].append(copy.copy(self._getEntities()[key].getLocation()))
            self.__mass[key].append(copy.copy(self._getEntities()[key].getMass()))
        super().log(sim, delta_t)

    def resetLog(self, set_time_to_zero: bool = False):
        super().resetLog(set_time_to_zero)
        for key in self.__positions.keys():
            self.__positions[key] = [self.__positions[key][-1]]
            self.__mass[key] = [self.__mass[key][-1]]

    def _customAction(self, sim):
        filepath = self.getFilepath()

        barycenter = []
        distance = {}
        x = {}
        y = {}
        z = {}
        t = self._getTime()

        for i in range(len(list(self.__positions.values())[0])):
            massWeightedDistanceSum = pygame.Vector3(0, 0, 0)
            totalMass = 0
            for key in self.__positions.keys():
                massWeightedDistanceSum += self.__positions[key][i] * self.__mass[key][i]
                totalMass += self.__mass[key][i]
            barycenter.append(massWeightedDistanceSum / totalMass)

        for key in self.__measuredEntities.keys():
            distance[key] = []
            x[key] = []
            y[key] = []
            z[key] = []
            for i, position in enumerate(self.__positions[key].copy()):
                position -= barycenter[i]
                distance[key].append(position.magnitude() * self.__measuredEntities[key])
                x[key].append(position.x * self.__measuredEntities[key])
                y[key].append(position.y * self.__measuredEntities[key])
                z[key].append(position.z * self.__measuredEntities[key])
        
        timeStamp = datetime.datetime.now().strftime("%Y %m %d %H %M %S %f")

        plt.figure()
        for key in self.__measuredEntities.keys():
            plt.plot(t, x[key], color = "blue", label = "{} X Position".format(key))
            plt.plot(t, y[key], color = "orange", label = "{} Y Position".format(key))
            plt.plot(t, z[key], color = "green", label = "{} Z Position".format(key))
            plt.xlabel("Time (s)")
            plt.ylabel("Component Displacement from Barycenter (m)")
            plt.legend()
            if filepath is not None:
                temp_filePath = os.path.join(filepath, "Component_Displacement/{}/{}".format(key, timeStamp))

                plt.savefig(temp_filePath + ".png")

                csvFile = open(temp_filePath + ".csv", "x", newline = "")
                writer = csv.writer(csvFile)
                writer.writerow(["t", "x displacement", "y displacement", "z displacement"])
                for i in range(len(t)):
                    writer.writerow([t[i], x[key][i], y[key][i], z[key][i]])
                csvFile.close()

            if self.getShowGraphs():
                plt.show()
            plt.clf()
            plt.close()
        
        
        plt.figure(figsize = (7, 7))
        for key in self.__measuredEntities.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(x[key], z[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(x[key], z[key], label = key)
        plt.xlabel("X Displacement (m)")
        plt.ylabel("Z Displacement (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "X_Z_Plane/{}".format(timeStamp))

            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__measuredEntities.keys():
                row.append("{} x displacement".format(key))
                row.append("{} z displacement".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__measuredEntities.keys():
                    row.append(x[key][i])
                    row.append(z[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()
        

        plt.figure()
        for key in self.__measuredEntities.keys():
            entity = self._getEntities()[key]
            if hasattr(entity, "getColour"):
                plt.plot(t, distance[key], label = key, color = tuple([value / 255 for value in _correctBrightColour(entity.getColour())]))
            else:
                plt.plot(t, distance[key], label = key)
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (m)")
        plt.legend()
        if filepath is not None:
            temp_filePath = os.path.join(filepath, "Distance_Over_Time/{}".format(timeStamp))
        
            plt.savefig(temp_filePath + ".png")

            csvFile = open(temp_filePath + ".csv", "x", newline = "")
            writer = csv.writer(csvFile)
            row = ["t"]
            for key in self.__measuredEntities.keys():
                row.append("{} distance".format(key))
            writer.writerow(row)
            for i in range(len(t)):
                row = [t[i]]
                for key in self.__measuredEntities.keys():
                    row.append(distance[key][i])
                writer.writerow(row)
            csvFile.close()

        if self.getShowGraphs():
            plt.show()
        plt.clf()
        plt.close()