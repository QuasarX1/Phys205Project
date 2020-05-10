from enum import Enum
from lxml import etree, objectify
import numpy as np
import os
import pygame
from QuasarCode.edp import Event
import threading
import uuid

from simulation import Layer, Layer_2D, Layer_3D, Layer_Mixed, command_options as commands, local_test_xml_location, xml_bool, createPygameVector3, load_XML, load_XML_without_schema
from simulation.commands import commands_runtime
from simulation.entities import Entity, Renderable_Simple2DCircle, Renderable_2DLine
from simulation.entities.prefabs import Croshair, Croshair_3D, UnitCube_Wireframe, TriangularPyrimid_Wireframe, Sphere
from simulation.graphics import Camera, CameraPositionDisplay, CameraForceDisplay, CameraSpeedDisplay
from simulation.graphics.HUD import Text, ReferencePoint, UpdatingText, Button
from simulation.logging import ActionLogger, PositionLogger, VelocityLogger, SeperationLogger, BarycenterSeperationLogger

from simulation.entities.astro_bodies import Star, Planet

pygame.init()
pygame.font.init()

class SimulationClock(object):
    def tick(*args, **kwargs):
        raise NotImplementedError("")



class PygameClockWrapper(SimulationClock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clock = pygame.time.Clock()

    def tick(self, *args, **kwargs):
        return self.__clock.tick(*args, **kwargs)



class LinearTickClock(SimulationClock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__counter = 0

    def tick(self, *args, **kwargs):
        self.__counter += 1
        return 1



class RenderMode(Enum):
    no_render = 0,
    real_time = 1,
    save_file = 2



class Simulation(object):
    """
    Runs a constructed simulation in a self contained environment.
    
    Constructor:
        bool render -> Should the simulation be rendered? (True)
        float tickScale -> Number of seconds to simulate per 1 tick or per 1 second of a randered simulation. (1 earth day)
        float distanceScale -> Number of pixels used to represent 1 meter. (1)
    """

    def __init__(self, renderMode: RenderMode = RenderMode.real_time, timeScale: float = 1,
                 cameraDimentions: pygame.Vector2 = pygame.Vector2(1, 1), displayWindowDimentions = (500, 500), maxFPS = 60, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-set the simulation state
        self.__running: bool = False
        self.__paused: bool = True
        self.__total_delta_t: float = 0
        self.__runID = str(uuid.uuid4())

        # Events
        self.onItterationEnd: Event = Event()
        self.onRenderEnd: Event = Event()
        #self.onWindoDimentionChange: Event = Event()
        self.onClick: Event = Event()

        # Rendering Attributes
        self.__fullscreen = False
        self.__camera: Camera = Camera(dimentions = cameraDimentions)

        self.__distanceScale: float = None# pixels : simulated meters #TODO: should this be called meters per pixel?!
        self.__calculatePixelsPerMeter(displayWindowDimentions[0])
        self.__camera.setHeightOffset(displayWindowDimentions[1], self.__distanceScale)

        self.__renderMode: RenderMode = renderMode
        self.__displayOutput: bool = self.__renderMode == RenderMode.real_time
        
        self.__maxFPS:int = maxFPS# Only relivant for use with the pygame clock
        
        if self.__displayOutput:
            self.__screen: pygame.Surface = None
            self.__newScreenSurface(
                (
                    int(self.__camera.getWidth() * self.__distanceScale),
                    int(self.__camera.getHeight() * self.__distanceScale)
                ))
            pygame.display.set_caption("Exoplanet Simulation")

        else:
            self.__screen: pygame.Surface = self.createCameraSizedSurface()

        self.__layers: dict = {"background": Layer_3D(self.createCameraSizedSurface(), backgroundColour = pygame.Color(0, 0, 0)),
                               "HUD": Layer_Mixed(self.createSurface()),
                               "pause_menu": Layer_2D(self.createSurface(), pygame.Color(0, 0, 0, 175))}# Layers for entity storage
        self.__protectedLayerNames = ("background", "HUD", "pause_menu")

        if self.__displayOutput:
            self.__layers["HUD"].addEntity("time", UpdatingText(lambda self: commands_runtime(self.getReferencedObject("simulation")), "freesansbold.ttf", 15, {"simulation": self}, referencePoint = ReferencePoint.bottom_left, location = pygame.Vector3(0, 0.95, 0)))
            self.__layers["HUD"].getEntity("time").hide()

            self.__layers["HUD"].addEntity("camera_position", CameraPositionDisplay(self.__camera))
            self.__layers["HUD"].getEntity("camera_position").hide()

            self.__layers["HUD"].addEntity("camera_force", CameraForceDisplay(self.__camera, location = pygame.Vector3(0, 0.1, 0)))
            self.__layers["HUD"].getEntity("camera_force").hide()

            self.__layers["HUD"].addEntity("camera_speed", CameraSpeedDisplay(self.__camera, location = pygame.Vector3(0, 0.2, 0)))
            self.__layers["HUD"].getEntity("camera_speed").hide()

            self.__layers["HUD"].addEntity("croshair", Croshair())

            self.__layers["HUD"].addEntity("3D_croshair", Croshair_3D())
            self.__layers["HUD"].getEntity("3D_croshair").hide()

            self.__layers["pause_menu"].addEntity("title", Text("Pause Menu", "freesansbold.ttf", 30, referencePoint = ReferencePoint.top_centre, location = pygame.Vector3(0.5, 0, 0)))
            self.__layers["pause_menu"].getEntity("title").setUnderline()

            self.__layers["pause_menu"].addEntity("resume_button", Button(self, "resume", "freesansbold.ttf", 30, referencePoint = ReferencePoint.top_centre, location = pygame.Vector3(0.5, 0.2, 0)))
            self.__layers["pause_menu"].getEntity("resume_button").onClick += self.resume

            self.__layers["pause_menu"].addEntity("toggle_camera_metrics_button", Button(self, "toggle camera metrics", "freesansbold.ttf", 30, referencePoint = ReferencePoint.top_centre, location = pygame.Vector3(0.5, 0.4, 0)))
            self.__layers["pause_menu"].getEntity("toggle_camera_metrics_button").onClick += self.__toggleCameraMetrics

        # Clock Options
        self.__timeScale: float = timeScale# simulated seconds : real seconds

        if self.__displayOutput:
            # Use a real-time clock for live rendering
            # Each tick vairies in length
            self.__clock: SimulationClock = PygameClockWrapper()
            self.__tickConversion: float = 0.001# Seconds per Tick
        else:
            # Incremental ticks of 1 to reduce variation
            self.__clock: SimulationClock = LinearTickClock()
            self.__tickConversion: float = 1.0# Seconds per Tick

    @staticmethod
    def __createEntityFromXML(entity_xml, layer):
        entityTypeString = entity_xml.tag.split("}")[1]

        if entityTypeString == "planet":
            return Planet.PlanetFromXML(entity_xml, layer)

        elif entityTypeString == "star":
            return Star.StarFromXML(entity_xml, layer)
    
        elif entityTypeString == "croshair_3D":
            return Croshair_3D.Croshair_3DFromXML(entity_xml, layer)

        elif entityTypeString == "triangularpyrimid_wireframe":
            return TriangularPyrimid_Wireframe.TriangularPyrimid_WireframeFromXML(entity_xml, layer)

        elif entityTypeString == "unitcube_wireframe":
            return UnitCube_Wireframe.UnitCube_WireframeFromXML(entity_xml, layer)

        elif entityTypeString == "sphere":
            return Sphere.SphereFromXML(entity_xml, layer)

        elif entityTypeString == "croshair":
            return Croshair.CroshairFromXML(entity_xml, layer)

        elif entityTypeString == "renderable_simple2Dcircle":
            return Renderable_Simple2DCircle.Renderable_Simple2DCircleFromXML(entity_xml, layer)

        elif entityTypeString == "renderable_2Dline":
            return Renderable_2DLine.Renderable_2DLineFromXML(entity_xml, layer)

    @staticmethod
    def create_from_xml(path_to_xml: str = local_test_xml_location, forceVisable: bool = False, forceTimescale: float = None):
        """
        Create a simulation from a pre-created XML file.

        The XML must conform to http://raw.githubusercontent.com/QuasarX1/Phys205Project/dev/simulation/layout_schema/simulation_layout_schema.xsd.
        
        Paramiters:
            str path_to_xml -> The filepath to the XML document to be loaded
        """
        #tree = load_XML(path_to_xml)#, local_schema_location)
        tree = load_XML_without_schema(path_to_xml)
        simulation_xml = tree.getroot()

        hasCamera = hasattr(simulation_xml, "camera")
        if hasCamera:
            simulation = Simulation(cameraDimentions = pygame.Vector2(float(simulation_xml.camera.get("width")), float(simulation_xml.camera.get("height"))),
                                        renderMode = RenderMode.real_time if forceVisable or xml_bool(simulation_xml.get("render_capability")) else RenderMode.no_render,
                                        timeScale = float(simulation_xml.get("timescale") if forceTimescale is None else forceTimescale))
            camera_xml = simulation_xml.camera
            camera = simulation.getCamera()
            camera.setFov(np.pi * float(camera_xml.get("field_of_vision")))
            camera.setLocation(createPygameVector3(camera_xml.location))
            camera.setFacing(createPygameVector3(camera_xml.facing))
            camera.setVertical(createPygameVector3(camera_xml.vertical))
        else:
            simulation = sim.Simulation(renderMode = RenderMode.real_time if forceVisable or xml_bool(simulation_xml.get("render_capability")) else RenderMode.no_render,
                                        timeScale = float(simulation_xml.get("timescale") if forceTimescale is None else forceTimescale))

        remainingChildren = simulation_xml.getchildren()[1 if hasCamera else 0:]
        for i in range(len(remainingChildren)):
            if remainingChildren[i].tag == "comment":
                continue
            childTypeString = remainingChildren[i].tag.split("}")[1]

            if childTypeString in ("layer_2D", "layer_3D", "Layer_Mixed"):
                layer_xml = remainingChildren[i]

                if childTypeString == "layer_2D":
                    layer = Layer_2D(layer_xml.attrib["render_capability"])

                elif childTypeString == "layer_3D":
                    layer = Layer_3D(layer_xml.attrib["render_capability"])

                elif childTypeString == "Layer_Mixed":
                    layer = Layer_Mixed(layer_xml.attrib["render_capability"])

                simulation.addLayer(layer_xml.attrib["name"], layer)

                bindingDict = {}
                for entity_xml in layer_xml.getchildren():
                    if entity_xml.tag == "comment":
                        continue
                    entityName = entity_xml.attrib["name"]
                    entityCreationResult = Simulation.__createEntityFromXML(entity_xml, layer)
                    entity = entityCreationResult["entity"]
                    layer.addEntity(entityName, entity)

                    if "bound_entities" in entityCreationResult.keys():
                        bindingDict[entityName] = entityCreationResult["bound_entities"]

                for key in bindingDict.keys():
                    for entity_name in bindingDict[key]:
                        layer.getEntity(key).bindEntity_by_name(entity_name, layer)

            elif childTypeString in ("position_logger", "velocity_logger", "seperation_logger", "barycenter_seperation_logger"):
                logger_xml = remainingChildren[i]

                logger_kwargs = {"name":logger_xml.attrib["name"],
                                 "runID":simulation.getRunID(),
                                 "zero_time_on_action":xml_bool(logger_xml.attrib["zero_time_on_action"]),
                                 "show_graphs":xml_bool(logger_xml.attrib["show_graphs"])}

                logger_kwargs["entities"] = {}
                for entity_reference_xml in [child for child in logger_xml.getchildren() if child.tag.split("}")[1] == "logged_entity"]:
                    logger_kwargs["entities"][entity_reference_xml.attrib["entity_name"]] = simulation.getEntity(entity_reference_xml.attrib["layer_name"], entity_reference_xml.attrib["entity_name"])

                if logger_xml.attrib["trigger_type"] == "data_chunk":
                    logger_kwargs["trigger"] = ActionLogger.createChunkOfDataTrigger(int(logger_xml.attrib["trigger_limit"]))
                elif logger_xml.attrib["trigger_type"] == "time_period":
                    logger_kwargs["trigger"] = ActionLogger.createTimePeriodTrigger(float(logger_xml.attrib["trigger_limit"]))
                
                if "file_save_path" in logger_xml.attrib.keys():
                    logger_kwargs["file_save_path"] = logger_xml.attrib["file_save_path"]

                if childTypeString == "position_logger":
                    simulation.onItterationEnd += PositionLogger(**logger_kwargs)

                elif childTypeString == "velocity_logger":
                    simulation.onItterationEnd += VelocityLogger(**logger_kwargs)

                elif childTypeString == "seperation_logger":
                    simulation.onItterationEnd += SeperationLogger(referenceEntity = simulation.getEntity(logger_xml.reference_entity.attrib["layer_name"], logger_xml.reference_entity.attrib["entity_name"]),
                                                                   **logger_kwargs)

                elif childTypeString == "barycenter_seperation_logger":
                    measuredEntities = {}
                    for entity_reference_xml in [child for child in logger_xml.getchildren() if child.tag.split("}")[1] == "measure_entity"]:
                        measuredEntities[entity_reference_xml.attrib["entity_name"]] = float(entity_reference_xml.attrib["scale"])
                    simulation.onItterationEnd += BarycenterSeperationLogger(star = simulation.getEntity(logger_xml.star.attrib["layer_name"], logger_xml.star.attrib["entity_name"]),
                                                                             layer = simulation.getLayer(logger_xml.star.attrib["layer_name"]),
                                                                             measuredEntities = measuredEntities,
                                                                             **logger_kwargs)

        return simulation

    def __toggleCameraMetrics(self):
        self.__layers["HUD"].getEntity("croshair").setVisability(not self.__layers["HUD"].getEntity("croshair").isVisable())
        self.__layers["HUD"].getEntity("3D_croshair").setVisability(not self.__layers["HUD"].getEntity("3D_croshair").isVisable())
        self.__layers["HUD"].getEntity("time").setVisability(not self.__layers["HUD"].getEntity("time").isVisable())
        self.__layers["HUD"].getEntity("camera_position").setVisability(not self.__layers["HUD"].getEntity("camera_position").isVisable())
        self.__layers["HUD"].getEntity("camera_force").setVisability(not self.__layers["HUD"].getEntity("camera_force").isVisable())
        self.__layers["HUD"].getEntity("camera_speed").setVisability(not self.__layers["HUD"].getEntity("camera_speed").isVisable())

    def __calculatePixelsPerMeter(self, windowWidth):
        self.__distanceScale = windowWidth / self.__camera.getWidth()

    def __newScreenSurface(self, size: tuple):
        if not self.__fullscreen:
            self.__caschedScreenSize = size
        self.__screen = pygame.display.set_mode(size, flags = pygame.RESIZABLE)

    def __toggleFullscreen(self):
        self.__fullscreen = not self.__fullscreen
        pygame.display.quit()
        pygame.display.init()
        if self.__fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), flags = pygame.FULLSCREEN)
        else:
            self.__newScreenSurface(self.__caschedScreenSize)

    def __handleMouseCapture(self):
        if self.__displayOutput:
            pygame.mouse.set_visible(self.__paused)
            pygame.mouse.set_pos(self.__camera.getWidth() * self.__distanceScale / 2, self.__camera.getHeight() * self.__distanceScale / 2)
            pygame.event.set_grab(not self.__paused)
            pygame.mouse.get_rel()# Prevents mouse movement whilst paused from being used

    def createCameraSizedSurface(self):
        return self.createSurface(
            (
                int(self.__camera.getWidth() * self.__distanceScale),
                int(self.__camera.getHeight() * self.__distanceScale)
            ))

    def createSurface(self, dimentions: tuple = None):
        if dimentions is None:
            dimentions = self.__screen.get_size()
        return pygame.Surface(dimentions, flags = pygame.SRCALPHA)

    def getRunID(self):
        return self.__runID
        
    def getCamera(self) -> Camera:
        """
        Returns a reference to the simulation's camera.
        """
        return self.__camera

    def getLayer(self, name: str) -> Layer:
        """
        Returns the Layer object registered to the simulation with the specified name.

        Paramiters:
            str name -> The name of the layer
        """
        try:
            return self.__layers[name]
        except KeyError:
            return None

    def addLayer(self, name: str, layer: Layer):
        """
        Registers a new layer with the simulation.

        Paramiters:
            str name -> The name the new layer should be registered with
            Layer layer -> The layer to register
        """
        if name not in self.__layers.keys():
            self.__layers[name] = layer
            layer.setSurface(self.createCameraSizedSurface())
        else:
            raise KeyError("A layer already exists with the name {}.".format(name))

    def removeLayer(self, name: str):
        """
        Un-registers an existing layer from the simulation.

        Paramiters:
            str name -> The name of the existing layer that should be un-registered
        """
        if name in self.__protectedLayerNames:
            raise ValueError("The layer {} is a protected layer and as such can't be removed.".format(name))

        self.__layers.pop(name, None)

    def showLayer(self, layer_name):
        try:
            self.__layers[layer_name].show()
        except KeyError:
            pass

    def hideLayer(self, layer_name):
        try:
            self.__layers[layer_name].hide()
        except KeyError:
            pass

    def showHUD(self):
        self.__layers["HUD"].show()

    def hideHUD(self):
        self.__layers["HUD"].hide()

    def getEntity(self, layer_name: str, entity_name: str):
        return self.getLayer(layer_name).getEntity(entity_name)

    def getRunTime(self):
        return self.__total_delta_t

    def getTickScale(self):
        return self.__timeScale

    def getDistanceScale(self):
        return self.__distanceScale

    def getDisplaySurface(self):
        return self.__screen

    def pause(self):
        self.__paused = True
        self.__layers["pause_menu"].show()

    def resume(self):
        self.__paused = False
        self.__layers["pause_menu"].hide()

        self.__handleMouseCapture()

    def togglePauseState(self):
        self.__paused = not self.__paused
        self.__layers["pause_menu"].setVisability(self.__paused)

        if not self.__paused:
            self.__handleMouseCapture()

    def isPaused(self):
        return self.__paused

    def isRunning(self):
        return self.__running

    def isRenderable(self):
        return self.__renderMode != RenderMode.no_render

    def update(self, delta_t):
        """
        Update all layers registered with the simulation in the order in which they were registered.

        Paramiters:
            float delta_t -> The time in seconds that has passed since the last update
        """
        for layerName in self.__layers.keys():
            if layerName != "pause_menu":
                self.__layers[layerName].pre_update()#TODO: consider running these as paralell threads

        for layerName in self.__layers.keys():
            if layerName != "pause_menu":
                self.__layers[layerName].update(delta_t, self)#TODO: consider running these as paralell threads

        for layerName in self.__layers.keys():
            if layerName != "pause_menu":
                self.__layers[layerName].post_update()#TODO: consider running these as paralell threads

    def render(self):
        """
        Renders each layer in order provided the simulation is specified as being renderable.
        """
        if self.isRenderable():
            self.__screen.fill((0, 100, 255))

            if self.__layers["background"].render(self.__camera):
                self.__screen.blit(self.__layers["background"].surface, (0, -self.__camera.getHeightOffset()))

            for layerName in self.__layers.keys():
                if layerName not in self.__protectedLayerNames:
                    layer = self.__layers[layerName]
                    if layer.isRenderable():
                        success = False
                        if type(layer) is Layer_3D:
                            if layer.render(self.__camera, self.__distanceScale):
                                self.__screen.blit(layer.surface, (0, -self.__camera.getHeightOffset()))
                        else:# 2D and Mixed layers are rendered relitive to the whole screen
                            if layer.render():
                                self.__screen.blit(layer.surface, (0, 0))

            if self.__layers["HUD"].render():
                self.__screen.blit(self.__layers["HUD"].surface, (0, 0))

            if self.__layers["pause_menu"].render():
                self.__screen.blit(self.__layers["pause_menu"].surface, (0, 0))

            if self.__displayOutput:
                pygame.display.flip()
                #pygame.display.update()

            if self.onRenderEnd.getTotalSubscribers() > 0:
                    self.onRenderEnd.run(self, simulated_delta_t)

    def __run(self, autorun = True):
        self.__running = True
        self.__paused = not autorun

        if not self.__displayOutput:
            self.pause()

        if not self.__paused:
            self.__handleMouseCapture()

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.togglePauseState()
                        self.__handleMouseCapture()

                    elif event.key == pygame.K_F3:
                        self.__toggleCameraMetrics()

                    elif event.key == pygame.K_F4:
                        if event.mod & pygame.KMOD_ALT:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))

                    elif event.key == pygame.K_F11:
                        self.__toggleFullscreen()

                    elif event.key in (pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):# Go to simulation layer object at index 1
                        if self.__layers["simulation_layer"]:
                            if event.key == pygame.K_KP0 or pygame.K_0
                                entity = self.__layers["simulation_layer"].getEntityByIndex(0)
                            elif event.key == pygame.K_KP1 or pygame.K_1
                                entity = self.__layers["simulation_layer"].getEntityByIndex(1)
                            elif event.key == pygame.K_KP2 or pygame.K_2
                                entity = self.__layers["simulation_layer"].getEntityByIndex(2)
                            elif event.key == pygame.K_KP3 or pygame.K_3
                                entity = self.__layers["simulation_layer"].getEntityByIndex(3)
                            elif event.key == pygame.K_KP4 or pygame.K_4
                                entity = self.__layers["simulation_layer"].getEntityByIndex(4)
                            elif event.key == pygame.K_KP5 or pygame.K_5
                                entity = self.__layers["simulation_layer"].getEntityByIndex(5)
                            elif event.key == pygame.K_KP6 or pygame.K_6
                                entity = self.__layers["simulation_layer"].getEntityByIndex(6)
                            elif event.key == pygame.K_KP7 or pygame.K_7
                                entity = self.__layers["simulation_layer"].getEntityByIndex(7)
                            elif event.key == pygame.K_KP8 or pygame.K_8
                                entity = self.__layers["simulation_layer"].getEntityByIndex(8)
                            elif event.key == pygame.K_KP9 or pygame.K_9
                                entity = self.__layers["simulation_layer"].getEntityByIndex(9)
                            if entity is not None:
                                if hasattr(entity, "getScaleFactor"):
                                    self.__camera.setLocation(entity.getLocation() + pygame.Vector3(0, 0, -entity.getScaleFactor() * 2))
                                else:
                                    self.__camera.setLocation(entity.getLocation())
                                self.__camera.setFacing(pygame.Vector3(0, 0, 1))
                                self.__camera.setVertical(pygame.Vector3(0, 1, 0))
                                self.__camera.setVelocity(pygame.Vector3(0, 0, 0))

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:# Scroll Up
                        self.__camera.setNetForce(self.__camera.getNetForce() + 10)
                    elif event.button == 5:# Scroll Down
                        self.__camera.setNetForce(self.__camera.getNetForce() - 10)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.onClick.getTotalSubscribers() > 0:
                            self.onClick.run(self.__screen)

                elif event.type == pygame.VIDEORESIZE:
                    self.__calculatePixelsPerMeter(event.w)
                    self.__camera.setHeightOffset(event.h, self.__distanceScale)

                    for layer in self.__layers.values():
                        if type(layer) is Layer_3D: layer.setSurface(self.createCameraSizedSurface())
                        else: layer.setSurface(self.createSurface(event.dict['size']))
                    if not self.__fullscreen:
                        self.__newScreenSurface(event.dict['size'])

                    self.__handleMouseCapture()

            delta_t = self.__clock.tick(self.__maxFPS) * self.__tickConversion
            simulated_delta_t = self.__timeScale * delta_t
            if not self.__paused:
                self.__camera.pre_update()
                # delta_t passed to camera must be independant of the timescale of the simulation for live rendering
                self.__camera.update(delta_t if self.__displayOutput else simulated_delta_t, self)
                self.update(simulated_delta_t)
                self.__camera.post_update()
                self.__total_delta_t += simulated_delta_t

                if self.onItterationEnd.getTotalSubscribers() > 0:
                    self.onItterationEnd.run(self, simulated_delta_t)
            else:
                self.__layers["pause_menu"].update(delta_t, self)

            self.render()

            

    def __run_threaded(self, autorun = True) -> threading.Thread:
        """
        Runs the simulation untill it terminates or is manualy terminated.

        NOTE: This should not be used for live rendered simulations!
        """
        simulationThread = threading.Thread(target = self.__run, kwargs = {"autorun": autorun})
        simulationThread.start()
        return simulationThread

    def run(self):
        """
        --!! WARNING !!-- This is a blocking method

        Runs the simulation untill it terminates or is manualy terminated.

        Simulations that are rendered will capture the mouse pointer.
        In order to pause updating, press 'Escape' - this will also release the mouse pointer.
        """
        if self.__displayOutput:# Is the output live?
            self.__run(autorun = False)

        else:# Terminal controll required
            simulationThread = self.__run_threaded()

            os.system("cls")
            while self.isRunning():
                print("({}) >>> ".format("running" if not self.isPaused() else "paused"), end = "")
                command, *arguments = (input() + " ").split(" ")
                arguments = arguments[:-1]

                try:
                    output = commands[command][0](self, *arguments)
                    os.system("cls")
                    if output is not None and output != "":
                        print(output)
                except:
                    print("Invalid Command \"{}\". Run \"help\" for a list of commands.".format(command))

                print()

            simulationThread.join()
