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
#simulation = Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(0.01, 0.01))
#simulation = Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(500, 500))
simulation = Simulation(renderMode = renderOption, timeScale = 3600.0 * 24.0, cameraDimentions = pygame.Vector2(500, 500))
#simulation = Simulation(renderMode = renderOption, timeScale = 3944700, cameraDimentions = pygame.Vector2(500, 500))

runID = simulation.getRunID()



# Position the Camera ----------------------------------------------------------------------------------------------------------------
# Nessessary for Earth-Sun Distance
#simulation.getCamera().setLocation(pygame.Vector3(0, 0, -1.496 * 10**11))
simulation.getCamera().setLocation(pygame.Vector3(0, 0, -20 * 10**8))


# Create and add display layers ------------------------------------------------------------------------------------------------------
simulation_layer = sim.layer.Layer_3D()
simulation.addLayer("simulation_layer", simulation_layer)



# Add display entities to the HUD layer ------------------------------------------------------------------------------------------



# Add massive bodies to a simulation layer ------------------------------------------------------------------------------------------
sun = Sun()
simulation_layer.addEntity("sun", sun)

mercury = Mercury(sun)
simulation_layer.addEntity("mercury", mercury)

venus = Venus(sun)
simulation_layer.addEntity("venus", venus)

earth = Earth(sun)
simulation_layer.addEntity("earth", earth)

mars = Mars(sun)
simulation_layer.addEntity("mars", mars)

jupiter = Jupiter(sun)
simulation_layer.addEntity("jupiter", jupiter)

saturn = Saturn(sun)
simulation_layer.addEntity("saturn", saturn)

uranus = Uranus(sun)
simulation_layer.addEntity("uranus", uranus)

neptune = Neptune(sun)
simulation_layer.addEntity("neptune", neptune)

pluto = Pluto(sun)
simulation_layer.addEntity("pluto", pluto)


'''
sun = Star(radius = 6.96 * 10**8,# The Sun's equatorial radius in m
           temperature = 5700,# Surface tempriture in K
           mass = 1.989 * 10**30,# Mass of the Sun in Kg
           initial_velocity = pygame.Vector3(0, 0, 0),
           initial_angular_velocity = 360 / (60 * 60 * 24 * 25.05),# roatates (siderialy) once at the equator every 25.05 Earth days
           location = pygame.Vector3(0, 0, 0))
simulation_layer.addEntity("sun", sun)

mercury = Planet(radius = 2.4397 * 10**6,# Equatorial radius in m
               mass = 3.3011 * 10**23,# Mass in Kg
               parentStar = sun,
               initial_velocity = pygame.Vector3(0, 0, 4.7362 * 10**4),# Orbital velocity in m/s
               initial_angular_velocity = 360 / (60 * 60 * 24 * 58.646),# Roatates (siderialy) once at the equator every ...
               location = pygame.Vector3(5.790905 * 10**10, 0, 0),# Distance from the Sun in m
               colour = pygame.Color(255, 150, 0))# Arbitrary colour
simulation_layer.addEntity("mercury", mercury)

#venus = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("venus", venus)

earth = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
               mass = 5.972 * 10**24,# Earth's mass in Kg
               parentStar = sun,
               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
               colour = pygame.Color(0, 255, 0))# Arbitrary colour
simulation_layer.addEntity("earth", earth)

#mars = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("mars", mars)

#juypter = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("juypter", juypter)

#saturn = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("saturn", saturn)

#uranus = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("uranus", uranus)

#neptune = Planet(radius = 1.737 * 10**6,# Earth's equatorial radius in m
#               mass = 5.972 * 10**24,# Earth's mass in Kg
#               parentStar = sun,
#               initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4),# The Earth's orbital velocity in m/s
#               initial_angular_velocity = 360 / (60 * 60 * 23.56),# roatates (siderialy) once at the equator every 23.56 hours
#               location = pygame.Vector3(1.496 * 10**11, 0, 0),# The distance between the Earth and the Sun in m
#               colour = pygame.Color(0, 255, 0))# Arbitrary colour
#simulation_layer.addEntity("neptune", neptune)
'''



# Set up logging for important quantities --------------------------------------------------------------------------------------------
logging_time_period_interior = 60*60*24*365.25 * 165
trigger_function_interior = ActionLogger.createTimePeriodTrigger(logging_time_period_interior)

logging_time_period_exterior = 60*60*24*365.25 * 165
trigger_function_exterior = ActionLogger.createTimePeriodTrigger(logging_time_period_exterior)

simulation.onItterationEnd += SeperationLogger(name = "interior_plannet_orbit_logger",
                                               runID = runID,
                                               entities = {"mercury": mercury, "venus": venus, "earth": earth, "mars": mars},
                                               trigger = trigger_function_interior,
                                               zero_time_on_action = False,
                                               show_graphs = showGraphs,
                                               file_save_path = filepath,
                                               referenceEntity = sun)

simulation.onItterationEnd += SeperationLogger(name = "exterior_plannet_orbit_logger",
                                               runID = runID,
                                               entities = {"jupiter": jupiter, "saturn": saturn, "uranus": uranus, "neptune": neptune, "pluto": pluto},
                                               trigger = trigger_function_exterior,
                                               zero_time_on_action = False,
                                               show_graphs = showGraphs,
                                               file_save_path = filepath,
                                               referenceEntity = sun)

#simulation.onItterationEnd += SeperationLogger(name = "exterior_plannet_orbit_logger",
#                                               runID = runID,
#                                               entities = {"juypter": juypter, "saturn": saturn, "uranus": uranus, "neptune": neptune},
#                                               trigger = trigger_function,
#                                               zero_time_on_action = False,
#                                               show_graphs = showGraphs,
#                                               file_save_path = filepath,
#                                               referenceEntity = sun)

simulation.onItterationEnd += PositionLogger(name = "sun_position_logger",
                                             runID = runID,
                                             entities = {"sun": sun},
                                             trigger = trigger_function_exterior,
                                             zero_time_on_action = False,
                                             show_graphs = showGraphs,
                                             file_save_path = filepath)

    

# Run the simulation------------------------------------------------------------------------------------------------------------------
simulation.run()



# ------------------------------------------------------------------------------------------------------------------------------------