import pygame
import numpy as np
from matplotlib import pyplot as plt
import sys
import simulation as sim
from star import Star
from planet import Planet



# Look for a command line paramiter indication the render status ---------------------------------------------------------------------
if len(sys.argv) > 1:
    if sys.argv[1] in ("False", "false", "F", "f", "0"):
        renderOption = False
    elif sys.argv[1] in ("True", "true", "T", "t", "1"):
        renderOption = True
    else:
        raise ValueError("The first command line paramiter should indicate whether or not the simulation should be rendered (a boolean).")
else:
    renderOption = True# Overide this to change the defult setting



# Create a blank simulation ----------------------------------------------------------------------------------------------------------
simulation = sim.Simulation(render = renderOption)



# Position the Camera ----------------------------------------------------------------------------------------------------------------
#simulation.getCamera().setLocation(pygame.Vector3(0, 200, 0))
#simulation.getCamera().setFacing(pygame.Vector3(0, -1, 0))
#simulation.getCamera().setVertical(pygame.Vector3(0, 0, 1))

simulation.getCamera().setLocation(pygame.Vector3(0, 0, -4 * 10**7))


# Create and add display layers ------------------------------------------------------------------------------------------------------
HUD = sim.layer.Layer_2D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("HUD", HUD)

simulation_layer = sim.layer.Layer_3D(pygame.Surface((500, 500), pygame.SRCALPHA))
simulation.addLayer("simulation_layer", simulation_layer)



# Add massive boddies to a simulation layer ------------------------------------------------------------------------------------------
target_star = Star(radius = 6371 * 10**3,
                   temperature = 100,
                   mass = 6 * 10**24,#1.9891 * 10**30,#500000,
                   initial_velocity = pygame.Vector3(0, 0, 0),
                   location = pygame.Vector3(0, 0, 0))
simulation_layer.addEntity("target_star", target_star)

test_planet = Planet(radius = 1737 * 10 **3,
                     mass = 7.4 * 10**22,#1.9891 * 10**30,#500000,
                     initial_velocity = pygame.Vector3(0, 0, 1040),
                     location = pygame.Vector3(384000 * 10**3, 0, 0),
                     colour = pygame.Color(0, 255, 0))
simulation_layer.addEntity("test_planet", test_planet)

second_planet = Planet(radius = 1737 * 10 **3,
                       mass = 7.4 * 10**22,#1.9891 * 10**30,#500000,
                       initial_velocity = pygame.Vector3(0, 0, -1040),
                       location = pygame.Vector3(-384000 * 10**3, 0, 0),
                       colour = pygame.Color(0, 0, 255))
simulation_layer.addEntity("second_planet", second_planet)



# Bind obbjects that should be gravetationaly bound-----------------------------------------------------------------------------------
target_star.bindEntity_by_name("test_planet", simulation_layer)
target_star.bindEntity_by_name("second_planet", simulation_layer)

test_planet.bindEntity_by_name("target_star", simulation_layer)
test_planet.bindEntity_by_name("second_planet", simulation_layer)

second_planet.bindEntity_by_name("target_star", simulation_layer)
second_planet.bindEntity_by_name("test_planet", simulation_layer)



# Set up logging for important quantities --------------------------------------------------------------------------------------------


class PositionLog(object):
    def __init__(self, entity):
        self.x = [entity.getLocation().x]
        self.z = [entity.getLocation().z]
        self.t = [0]

        self.entity = entity

    def log(self, sim, delta_t):
        self.x.append(self.entity.getLocation().x)
        self.z.append(self.entity.getLocation().z)
        self.t.append(self.t[-1] + delta_t)

        if len(self.t) > 100:
            sim.pause()
        
            plt.plot(self.x, self.t)
            plt.plot(self.z, self.t)
            plt.show()
        
            plt.plot(self.x, self.z)
            plt.show()
        
            self.x = [self.entity.getLocation().x]
            self.z = [self.entity.getLocation().z]
            self.t = [0]
        
            #input("Press enter to run next chunk... ")
            sim.resume()

class VelocityLog(object):
    def __init__(self, entity):
        self.x = [entity.getVelocity().x]
        self.y = [entity.getVelocity().y]
        self.z = [entity.getVelocity().z]
        self.t = [0]

        self.entity = entity

    def log(self, sim, delta_t):
        self.x.append(self.entity.getVelocity().x)
        self.y.append(self.entity.getVelocity().y)
        self.z.append(self.entity.getVelocity().z)
        self.t.append(self.t[-1] + delta_t)

        if len(self.t) > 5000:
            sim.pause()
        
            #plt.plot(self.x, self.t)
            #plt.plot(self.y, self.t)
            #plt.plot(self.z, self.t)
            #plt.show()

            plt.plot([np.sqrt(self.x[i]**2 + self.y[i]**2 + self.z[i]**2) for i in range(len(self.t))], self.t)
            plt.show()
        
            self.x = [self.entity.getVelocity().x]
            self.y = [self.entity.getVelocity().y]
            self.z = [self.entity.getVelocity().z]
            self.t = [0]
        
            #input("Press enter to run next chunk... ")
            sim.resume()

class FacingLog(object):
    def __init__(self, entity):
        self.x = [entity.getFacing().x]
        self.y = [entity.getFacing().y]
        self.z = [entity.getFacing().z]
        self.t = [0]

        self.entity = entity

    def log(self, sim, delta_t):
        self.x.append(self.entity.getFacing().x)
        self.y.append(self.entity.getFacing().y)
        self.z.append(self.entity.getFacing().z)
        self.t.append(self.t[-1] + delta_t)

        if len(self.t) > 100:
            sim.pause()
        
            plt.plot(self.x, self.t)
            plt.plot(self.z, self.t)
            plt.show()
        
            plt.plot(self.x, self.z)
            plt.show()
        
            self.x = [self.entity.getFacing().x]
            self.y = [self.entity.getFacing().y]
            self.z = [self.entity.getFacing().z]
            self.t = [0]
        
            #input("Press enter to run next chunk... ")
            sim.resume()

logger = PositionLog(test_planet)
#logger = VelocityLog(test_planet)
#logger = FacingLog(simulation.getCamera())

from simulation.logging.logger import PositionLogger, VelocityLogger, SeperationLogger
#logger = PositionLogger(test_planet, lambda self, sim, delta_t: len(self._getTime()) > 1000, False)
#logger = SeperationLogger(test_planet, target_star, lambda self, sim, delta_t: len(self._getTime()) > 1000, False)

simulation.onItterationEnd = logger.log



# Run the simulation------------------------------------------------------------------------------------------------------------------
simulation.run()



# ------------------------------------------------------------------------------------------------------------------------------------