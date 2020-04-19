import pygame
import numpy as np
from matplotlib import pyplot as plt
import sys
import uuid
import simulation as sim
from simulation.main import RenderMode
from star import Star
from planet import Planet
from simulation.entities.prefabs import UnitCube_Wireframe
from simulation.logging.logger import GraphingLogger, PositionLogger, VelocityLogger, SeperationLogger



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
#simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(0.01, 0.01))
#simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(500, 500))
simulation = sim.Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(500, 500))
#simulation = sim.Simulation(renderMode = renderOption, timeScale = 3944700, cameraDimentions = pygame.Vector2(500, 500))

runID = str(uuid.uuid4())



# Position the Camera ----------------------------------------------------------------------------------------------------------------
# Nessessary for Earth-Sun Distance
#simulation.getCamera().setLocation(pygame.Vector3(0, 0, -1.496 * 10**11))
simulation.getCamera().setLocation(pygame.Vector3(0, 0, -20 * 10**8))


# Create and add display layers ------------------------------------------------------------------------------------------------------
simulation_layer = sim.layer.Layer_3D()
simulation.addLayer("simulation_layer", simulation_layer)



# Add display entities to the HUD layer ------------------------------------------------------------------------------------------



# Add massive bodies to a simulation layer ------------------------------------------------------------------------------------------
sun = Star(radius = 6.96 * 10**8,# The Sun's equatorial radius in m
           temperature = 5700,# Surface tempriture in K
           mass = 1.989 * 10**30,# Mass of the Sun in Kg
           initial_velocity = pygame.Vector3(0, 0, 0),
           initial_angular_velocity = 360 / (60 * 60 * 24 * 25.05),# roatates (siderialy) once at the equator every 25.05 Earth days
           location = pygame.Vector3(0, 0, 0))
simulation_layer.addEntity("sun", sun)

earth = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
               mass = 5.972 * 10**24,# Earth's mass in Kg
               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
               colour = pygame.Color(0, 255, 0))# Arbitrary colour
simulation_layer.addEntity("earth", earth)



# Bind objects that should be gravitationally bound-----------------------------------------------------------------------------------
sun.bindEntity_by_name("earth", simulation_layer)

earth.bindEntity_by_name("sun", simulation_layer)



# Set up logging for important quantities --------------------------------------------------------------------------------------------
simulation.onItterationEnd += PositionLogger(name = "earth_position_logger",
                                             runID = runID,
                                             entity = earth,
                                             trigger = GraphingLogger.createTimePeriodTrigger(60*60*24*365.25),
                                             zero_time_on_action = False,
                                             show_graphs = showGraphs,
                                             file_save_path = filepath).log

    

# Run the simulation------------------------------------------------------------------------------------------------------------------
simulation.run()



# ------------------------------------------------------------------------------------------------------------------------------------