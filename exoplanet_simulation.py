# Extrenal library import statements -------------------------------------------------------------------------------------------------
from matplotlib import pyplot as plt
import numpy as np
import pygame
import sys
import uuid



# Simulation package import statements -----------------------------------------------------------------------------------------------
import simulation as sim
from simulation import Simulation
from simulation import RenderMode
from simulation.entities.astro_bodies import Star, Planet, Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
from simulation.entities.prefabs import UnitCube_Wireframe
from simulation.logging import ActionLogger, PositionLogger, VelocityLogger, SeperationLogger



# Look for a command line paramater indication the render status ---------------------------------------------------------------------
if len(sys.argv) > 1:
    if sys.argv[1] in ("False", "false", "F", "f", "0"):
        renderOption = RenderMode.no_render
    elif sys.argv[1] in ("True", "true", "T", "t", "1"):
        renderOption = RenderMode.real_time
    else:
        raise ValueError("The first command line paramiter should indicate whether or not the simulation should be rendered (a boolean).")

    if len(sys.argv) > 2:
        filepath = sys.argv[2]

    else:
        filepath = None

else:
    # Overide these to change the defult settings
    renderOption = RenderMode.real_time
    filepath = None

if renderOption == RenderMode.real_time:
    showGraphs = True
else:
    showGraphs = False



# Create a blank simulation ----------------------------------------------------------------------------------------------------------
simulation = Simulation(renderMode = renderOption, timeScale = 900, cameraDimentions = pygame.Vector2(500, 500))

runID = simulation.getRunID()



# Position the Camera ----------------------------------------------------------------------------------------------------------------
# Nessessary for Earth-Sun Distance
#simulation.getCamera().setLocation(pygame.Vector3(0, 0, -1.496 * 10**11))# At Earth's orbital radius
simulation.getCamera().setLocation(pygame.Vector3(0, 0, -20 * 10**8))# Closer in towards the Sun

# Top down view - currently not working
#simulation.getCamera().setLocation(pygame.Vector3(0, 20 * 10**8, 0))
#simulation.getCamera().setFacing(pygame.Vector3(0, -1, 0))
#simulation.getCamera().setVertical(pygame.Vector3(0, 0, 1))


# Create and add display layers ------------------------------------------------------------------------------------------------------
simulation_layer = sim.layer.Layer_3D()
simulation.addLayer("simulation_layer", simulation_layer)



# Add massive bodies to a simulation layer ------------------------------------------------------------------------------------------
sun = Sun()
simulation_layer.addEntity("sun", sun)

#mercury = Mercury(sun)
#simulation_layer.addEntity("mercury", mercury)

#venus = Venus(sun)
#simulation_layer.addEntity("venus", venus)

earth = Earth(sun)
simulation_layer.addEntity("earth", earth)

#mars = Mars(sun)
#simulation_layer.addEntity("mars", mars)

#jupiter = Jupiter(sun)
#simulation_layer.addEntity("jupiter", jupiter)

#saturn = Saturn(sun)
#simulation_layer.addEntity("saturn", saturn)

#uranus = Uranus(sun)
#simulation_layer.addEntity("uranus", uranus)

#neptune = Neptune(sun)
#simulation_layer.addEntity("neptune", neptune)

#pluto = Pluto(sun)
#simulation_layer.addEntity("pluto", pluto)



# Set up logging for important quantities --------------------------------------------------------------------------------------------
logging_time_period_interior = 60*60*24*365.25 * 165
trigger_function_interior = ActionLogger.createTimePeriodTrigger(logging_time_period_interior)

logging_time_period_exterior = 60*60*24*365.25 * 165
trigger_function_exterior = ActionLogger.createTimePeriodTrigger(logging_time_period_exterior)

#simulation.onItterationEnd += SeperationLogger(name = "interior_plannet_orbit_logger",
#                                               runID = runID,
#                                               entities = {"mercury": mercury, "venus": venus, "earth": earth, "mars": mars},
#                                               trigger = trigger_function_interior,
#                                               zero_time_on_action = False,
#                                               show_graphs = showGraphs,
#                                               file_save_path = filepath,
#                                               referenceEntity = sun)

#simulation.onItterationEnd += SeperationLogger(name = "earth_orbit_logger",
#                                               runID = runID,
#                                               entities = {"earth": earth},
#                                               trigger = trigger_function_interior,
#                                               zero_time_on_action = False,
#                                               show_graphs = showGraphs,
#                                               file_save_path = filepath,
#                                               referenceEntity = sun)

#simulation.onItterationEnd += SeperationLogger(name = "exterior_plannet_orbit_logger",
#                                               runID = runID,
#                                               entities = {"jupiter": jupiter, "saturn": saturn, "uranus": uranus, "neptune": neptune, "pluto": pluto},
#                                               trigger = trigger_function_exterior,
#                                               zero_time_on_action = False,
#                                               show_graphs = showGraphs,
#                                               file_save_path = filepath,
#                                               referenceEntity = sun)

#simulation.onItterationEnd += SeperationLogger(name = "exterior_plannet_orbit_logger",
#                                               runID = runID,
#                                               entities = {"juypter": juypter, "saturn": saturn, "uranus": uranus, "neptune": neptune},
#                                               trigger = trigger_function,
#                                               zero_time_on_action = False,
#                                               show_graphs = showGraphs,
#                                               file_save_path = filepath,
#                                               referenceEntity = sun)

#simulation.onItterationEnd += PositionLogger(name = "sun_position_logger",
#                                             runID = runID,
#                                             entities = {"sun": sun},
#                                             trigger = trigger_function_exterior,
#                                             zero_time_on_action = False,
#                                             show_graphs = showGraphs,
#                                             file_save_path = filepath)

    

# Run the simulation------------------------------------------------------------------------------------------------------------------
simulation.run()



# ------------------------------------------------------------------------------------------------------------------------------------