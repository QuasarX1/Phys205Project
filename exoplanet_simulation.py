import pygame
import numpy as np
from matplotlib import pyplot as plt
import sys
import simulation as sim
from simulation.main import RenderMode
from star import Star
from planet import Planet
from simulation.entities.prefabs import UnitCube_Wireframe
from simulation.logging.logger import PositionLogger, VelocityLogger, SeperationLogger



# Look for a command line paramater indication the render status ---------------------------------------------------------------------
if len(sys.argv) > 1:
    if sys.argv[1] in ("False", "false", "F", "f", "0"):
        renderOption = RenderMode.no_render
    elif sys.argv[1] in ("True", "true", "T", "t", "1"):
        renderOption = RenderMode.real_time
    else:
        raise ValueError("The first command line paramiter should indicate whether or not the simulation should be rendered (a boolean).")
else:
    renderOption = RenderMode.real_time# Overide this to change the defult setting



# Create a blank simulation ----------------------------------------------------------------------------------------------------------
#simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(0.01, 0.01))
#simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(500, 500))
simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600, cameraDimentions = pygame.Vector2(500, 500))



# Position the Camera ----------------------------------------------------------------------------------------------------------------
#simulation.getCamera().setLocation(pygame.Vector3(0, 500, 0))
#simulation.getCamera().setFacing(pygame.Vector3(0, -1, 0))
#simulation.getCamera().setVertical(pygame.Vector3(0, 0, 1))

#simulation.getCamera().setLocation(pygame.Vector3(-4 * 10**7, 0, 0))
#simulation.getCamera().setFacing(pygame.Vector3(1, 0, 0))

simulation.getCamera().setLocation(pygame.Vector3(0, 0, -4 * 10**7))


# Create and add display layers ------------------------------------------------------------------------------------------------------
simulation_layer = sim.layer.Layer_3D()
simulation.addLayer("simulation_layer", simulation_layer)



# Add display entities to the HUD layer ------------------------------------------------------------------------------------------



# Add massive bodies to a simulation layer ------------------------------------------------------------------------------------------
target_star = Star(radius = 6.371 * 10**6,
                   temperature = 5700,
                   mass = 6 * 10**24,#1.9891 * 10**30,#500000,
                   initial_velocity = pygame.Vector3(0, 0, 0),
                   location = pygame.Vector3(0, 0, 0))
simulation_layer.addEntity("target_star", target_star)

test_planet = Planet(radius = 1.737 * 10**6,
                     mass = 7.4 * 10**22,#1.9891 * 10**30,#500000,
                     initial_velocity = pygame.Vector3(0, 0, 1040),
                     location = pygame.Vector3(3.84 * 10**8, 0, 0),
                     colour = pygame.Color(0, 255, 0))
simulation_layer.addEntity("test_planet", test_planet)

#second_planet = Planet(radius = 1737 * 10 **3,
#                       mass = 7.4 * 10**22,#1.9891 * 10**30,#500000,
#                       initial_velocity = pygame.Vector3(0, 0, -1040),
#                       location = pygame.Vector3(-384000 * 10**3, 0, 0),
#                       colour = pygame.Color(0, 0, 255))
#simulation_layer.addEntity("second_planet", second_planet)




#import numpy as np
#from simulation.physics_engine.constants import G
#r = 100
#v = 2 * np.pi * r
#M = 4 * np.pi**2 * r**3 / G

#target_star = Star(radius = 50,
#                   temperature = 5700,
#                   mass = M,
#                   initial_velocity = pygame.Vector3(0, 0, 0),
#                   location = pygame.Vector3(0, 0, 0))
#simulation_layer.addEntity("target_star", target_star)

#test_planet = Planet(radius = 10,
#                     mass = 1,
#                     initial_velocity = pygame.Vector3(0, 0, v),
#                     location = pygame.Vector3(r, 0, 0),
#                     colour = pygame.Color(0, 255, 0))
#simulation_layer.addEntity("test_planet", test_planet)



# Bind objects that should be gravitationally bound-----------------------------------------------------------------------------------
target_star.bindEntity_by_name("test_planet", simulation_layer)
#target_star.bindEntity_by_name("second_planet", simulation_layer)

test_planet.bindEntity_by_name("target_star", simulation_layer)
#test_planet.bindEntity_by_name("second_planet", simulation_layer)

#second_planet.bindEntity_by_name("target_star", simulation_layer)
#second_planet.bindEntity_by_name("test_planet", simulation_layer)



# Set up logging for important quantities --------------------------------------------------------------------------------------------
if renderOption == RenderMode.real_time:
    #simulation.onItterationEnd += PositionLogger(test_planet, lambda self, sim, delta_t: len(self._getTime()) > 1000, False).log
    #simulation.onItterationEnd += VelocityLogger(test_planet, lambda self, sim, delta_t: len(self._getTime()) > 1000, False).log
    simulation.onItterationEnd += SeperationLogger(test_planet, target_star, lambda self, sim, delta_t: len(self._getTime()) > 1000, False).log
else:
    path = input("Where should any graphs be saved?\n>>> ")
    #simulation.onItterationEnd += PositionLogger(test_planet, lambda self, sim, delta_t: len(self._getTime()) > 1000, False, show_graphs = False, file_save_path = path).log
    #simulation.onItterationEnd += VelocityLogger(test_planet, lambda self, sim, delta_t: len(self._getTime()) > 1000, False, show_graphs = False, file_save_path = path).log
    #simulation.onItterationEnd += SeperationLogger(test_planet, target_star, lambda self, sim, delta_t: len(self._getTime()) > 1000, False, show_graphs = False, file_save_path = path).log
    #simulation.onItterationEnd += SeperationLogger(test_planet, target_star, lambda self, sim, delta_t: self._getTime()[-1] > 31557600, False, show_graphs = False, file_save_path = path).log
    simulation.onItterationEnd += SeperationLogger(test_planet, target_star, lambda self, sim, delta_t: self._getTime()[-1] > 31557600 / 8, False, show_graphs = False, file_save_path = path).log
    


# Run the simulation------------------------------------------------------------------------------------------------------------------
simulation.run()



# ------------------------------------------------------------------------------------------------------------------------------------