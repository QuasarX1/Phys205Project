import pygame
import numpy as np
import threading
import os
from enum import Enum
from QuasarCode.edp import Event
from simulation.commands import commands
from simulation.layer import Layer, Layer_2D, Layer_3D
from simulation.entities.entity import Entity
from simulation.graphics.camera import Camera, CameraForceDisplay, CameraSpeedDisplay
from simulation.graphics.transformations import vector_to_array, array_to_vector, rotationMatrix, applyTransformation

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

    def tick(*args, **kwargs):
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

    def __init__(self, renderMode: RenderMode = RenderMode.real_time, timeScale: float = 3600.0 * 24.0,
                 cameraDimentions: tuple = (1, 1), displayWindowDimentions = (500, 500), maxFPS = 60, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Events
        self.onItterationEnd: Event = Event()
        self.onRenderEnd: Event = Event()
        self.onWindoDimentionChange: Event = Event()

        # Rendering Attributes
        self.__fullscreen = False
        self.__camera: Camera = Camera(dimentions = cameraDimentions)

        self.__distanceScale: float = None# pixels : simulated meters
        self.__calculatePixelsPerMeter(displayWindowDimentions[0])

        self.__camera.setHeightOffset(displayWindowDimentions[1], self.__distanceScale)

        self.__renderMode: RenderMode = renderMode
        self.__displayOutput: bool = self.__renderMode == RenderMode.real_time
        
        self.__maxFPS:int = maxFPS# Only relivant for use with the pygame clock

        self.__layers: dict = {"background": Layer_2D(self.createCameraSizedSurface()), "HUD": Layer_2D(self.createCameraSizedSurface())}# Layers for entity storage
        self.__protectedLayerNames = ("background", "HUD")
        
        if self.__displayOutput:
            self.__screen: pygame.Surface = None
            self.__newScreenSurface(
                (
                    int(self.__camera.getWidth() * self.__distanceScale),
                    int(self.__camera.getHeight() * self.__distanceScale)
                ))
            pygame.display.set_caption("Exoplanet Simulation")

            #TODO: add a toggalable option on the pause menu for these
            self.__layers["HUD"].addEntity("camera_force", CameraForceDisplay(self.__camera))
            self.__layers["HUD"].addEntity("camera_speed", CameraSpeedDisplay(self.__camera, location = pygame.Vector3(0, 0.1, 0)))
        else:
            self.__screen: pygame.Surface = self.createCameraSizedSurface()

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

        # Pre-set the simulation state
        self.__running: bool = False
        self.__paused: bool = True
        self.__total_delta_t: float = 0

    @staticmethod
    def create_from_xml(path_to_xml: str):
        """
        Create a simulation from a pre-created XML file.

        The XML must conform to http://raw.githubusercontent.com/QuasarX1/Phys205Project/dev/simulation/layout_schema/simulation_layout_schema.xsd.
        
        Paramiters:
            str path_to_xml -> The filepath to the XML document to be loaded
        """
        raise NotImplementedError("This has not yet been implemented.")#TODO: add this using DOM from https://www.tutorialspoint.com/python/python_xml_processing.htm

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

    def createSurface(self, dimentions: tuple):
        return pygame.Surface(dimentions, flags = pygame.SRCALPHA)
        
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

    def pause(self):
        self.__paused = True

    def resume(self):
        self.__paused = False

    def togglePauseState(self):
        self.__paused = not self.__paused

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
        for layer in self.__layers.values():
            layer.pre_update()#TODO: consider running these as paralell threads

        for layer in self.__layers.values():
            layer.update(delta_t, self)#TODO: consider running these as paralell threads

        for layer in self.__layers.values():
            layer.post_update()#TODO: consider running these as paralell threads

    def render(self):
        """
        Renders each layer in order provided the simulation is specified as being renderable.
        """
        if self.isRenderable():
            self.__screen.fill((0, 0, 0))

            self.__layers["background"].render()
            self.__screen.blit(self.__layers["background"].surface, (0, 0))

            for layerName in self.__layers.keys():
                if layerName not in self.__protectedLayerNames:
                    layer = self.__layers[layerName]
                    if layer.isRenderable():
                        if type(layer) is Layer_3D: layer.render(self.__camera, self.__distanceScale)
                        else: layer.render()
                        self.__screen.blit(layer.surface, (0, 0))

            self.__layers["HUD"].render()
            self.__screen.blit(self.__layers["HUD"].surface, (0, 0))

            if self.__displayOutput:
                pygame.display.flip()
                #pygame.display.update()

            if self.onRenderEnd.getTotalSubscribers() > 0:
                    self.onRenderEnd.run(self, simulated_delta_t)

    def __run(self):
        self.__running = True

        if not self.__displayOutput:
            self.__paused = False

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

                    elif event.key == pygame.K_F11:
                        self.__toggleFullscreen()
                        self.__handleMouseCapture()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:# Scroll Up
                        self.__camera.setNetForce(self.__camera.getNetForce() + 10)
                    elif event.button == 5:# Scroll Down
                        self.__camera.setNetForce(self.__camera.getNetForce() - 10)

                elif event.type == pygame.VIDEORESIZE:
                    self.__calculatePixelsPerMeter(event.w)
                    self.__camera.setHeightOffset(event.h, self.__distanceScale)

                    for layer in self.__layers.values():
                        if type(layer) is Layer_3D: layer.setSurface(self.createCameraSizedSurface())
                        else: layer.setSurface(self.createSurface(event.dict['size']))
                    if not self.__fullscreen:
                        self.__newScreenSurface(event.dict['size'])

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

            self.render()

            

    def __run_threaded(self) -> threading.Thread:
        """
        Runs the simulation untill it terminates or is manualy terminated.

        NOTE: This should not be used for live rendered simulations!
        """
        simulationThread = threading.Thread(target = self.__run)
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
            self.__run()

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