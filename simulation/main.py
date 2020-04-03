import pygame
import numpy as np
import threading
import os
from simulation.commands import commands
from simulation.layer import Layer, Layer_2D, Layer_3D
from simulation.entities.entity import Entity
from simulation.entities.renderable import Renderable_Simple2DRect
from simulation.entities.prefabs import UnitCube_Wireframe, TriangularPyrimid_Wireframe
from simulation.graphics.camera import Camera, CameraSpeedDisplay
from simulation.graphics.transformations import vector_to_array, array_to_vector, rotationMatrix, applyTransformation

pygame.init()
pygame.font.init()

class Simulation(object):
    """
    Runs a constructed simulation in a self contained environment.
    
    Constructor:
        bool render -> Should the simulation be rendered? (True)
        float tickScale -> Number of seconds to simulate per 1 tick or per 1 second of a randered simulation. (1 earth day)
        float distanceScale -> Number of pixels used to represent 1 meter. (1)
    """

    def __init__(self, render = True, tickScale = 3600 * 24, distanceScale = 1, **kwargs):
        super().__init__(**kwargs)
        self.canRender = render
        self.__layers = {"defult": Layer_2D(pygame.Surface((500, 500), pygame.SRCALPHA))}
        self.clock = pygame.time.Clock()
        self.onItterationEnd = lambda simulation, delta_t: None
        self.__running = False
        self.__paused = True
        self.__total_delta_t = 0
        self.__tickScale = tickScale# simulated time : real time
        self.__distanceScale = distanceScale# pixels : simulated meters

        if self.canRender:
            self.screen: pygame.Surface = pygame.display.set_mode((500, 500), flags = pygame.RESIZABLE)
            pygame.display.set_caption("Exoplanet Simulation")
            window_size = pygame.display.get_surface().get_size()
            self.__camera = Camera(dimentions = pygame.Vector2(window_size[0], window_size[1]))
            self.__layers["defult"].addEntity("camera_speed", CameraSpeedDisplay(self.__camera))
        else:
            self.screen = None
            self.__camera = Camera()

    @staticmethod
    def create_from_xml(path_to_xml: str):
        """
        Create a simulation from a pre-created XML file.

        The XML must conform to http://raw.githubusercontent.com/QuasarX1/Phys205Project/dev/simulation/layout_schema/simulation_layout_schema.xsd.
        
        Paramiters:
            str path_to_xml -> The filepath to the XML document to be loaded
        """
        raise NotImplementedError("This has not yet been implemented.")#TODO: add this using DOM from https://www.tutorialspoint.com/python/python_xml_processing.htm

    def getCamera(self) -> Camera:
        """
        Returns a reference to the simulation's camera.
        """
        return self.__camera

    def setCamera(self, new_camera: Camera):
        """
        Overwrites the simulation's camera with a new Camera object.

        Paramiters:
            Camera new_camera -> A new camera object to be used as the simulation's camera
        """
        self.__camera = new_camera

    def getLayer(self, name: str) -> Layer:
        """
        Returns the Layer object registered to the simulation with the specified name.

        Paramiters:
            str name -> The name of the layer
        """
        if name in self.__layers.keys():
            return self.__layers[name]
        else:
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
        else:
            raise KeyError("A layer already exists with the name {}.".format(name))

    def removeLayer(self, name: str):
        """
        Un-registers an existing layer from the simulation.

        Paramiters:
            str name -> The name of the existing layer that should be un-registered
        """
        if name in self.__layers.keys():
            self.__layers.pop(name, None)

    def getEntity(self, layer_name: str, entity_name: str):
        return self.getLayer(layer_name).getEntity(entity_name)

    def getRunTime(self):
        return self.__total_delta_t

    def getTickScale(self):
        return self.__tickScale

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
        if self.canRender:
            for layer in self.__layers.values():
                if type(layer) is Layer_3D: layer.render(self.__camera)
                else: layer.render()
                self.screen.blit(layer.surface, (0, 0))#(self.__camera.getWidth() / 2, self.__camera.getHeight() / 2))#(0, 0))

    def run(self):
        """
        --!! WARNING !!-- This is a blocking method

        Runs the simulation untill it terminates or is manualy terminated.

        Simulations that are rendered will capture the mouse pointer.
        In order to pause updating, press 'Escape' - this will also release the mouse pointer.
        """
        if self.canRender == True:
            self.__run()

        else:
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

    def __run(self):
        self.__running = True
        self.__paused = False
        if self.canRender:
            pygame.mouse.set_visible(False)#TODO: how to deal with non-rendering???
            pygame.event.set_grab(True)

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.togglePauseState()
                        if self.canRender:
                            pygame.mouse.set_visible(self.__paused)
                            pygame.mouse.set_pos(self.__camera.getWidth() / 2, self.__camera.getHeight() / 2)
                            pygame.event.set_grab(not self.__paused)
                            pygame.mouse.get_rel()# Prevents mouse movement whilst paused from being used

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:# Scroll Up
                        self.__camera.setNetForce(self.__camera.getNetForce() + 10)
                    elif event.button == 5:# Scroll Down
                        self.__camera.setNetForce(self.__camera.getNetForce() - 10)

                elif event.type == pygame.VIDEORESIZE:
                    self.__camera.setWidth(event.w)
                    self.__camera.setHeight(event.h)

            delta_t = self.clock.tick(60) / 1000
            simulated_delta_t = self.__tickScale * delta_t
            if not self.__paused:
                self.__camera.pre_update()
                self.__camera.update(delta_t, self)
                self.update(simulated_delta_t)
                self.__camera.post_update()
                self.__total_delta_t += simulated_delta_t
                self.onItterationEnd(self, simulated_delta_t)

            self.render()

            if self.canRender:
                pygame.display.flip()
                #pygame.display.update()
                self.screen.fill((0, 0, 0))

            #self.onRenderEnd(self, delta_t)

    def __run_threaded(self) -> threading.Thread:
        """
        Runs the simulation untill it terminates or is manualy terminated.

        NOTE: This should not be used for rendered simulations!
        """
        simulationThread = threading.Thread(target = self.__run)
        simulationThread.start()
        return simulationThread