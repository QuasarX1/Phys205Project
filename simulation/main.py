import pygame
import numpy as np
from simulation.layer import Layer, Layer_2D, Layer_3D
from simulation.entities.entity import Entity
from simulation.entities.renderable import Renderable_Simple2DRect
from simulation.entities.prefabs import UnitCube_Wireframe, TriangularPyrimid_Wireframe
from simulation.graphics.camera import Camera
from simulation.graphics.transformations import vector_to_array, array_to_vector, rotationMatrix, applyTransformation

pygame.init()

class Simulation(object):
    """
    Runs a constructed simulation in a self contained environment.
    
    Constructor:
        bool render -> Should the simulation be rendered? (True)
    """

    def __init__(self, render = True, **kwargs):
        super().__init__(**kwargs)
        self.canRender = render
        self.__layers = {"defult": Layer_2D(pygame.Surface((500, 500), pygame.SRCALPHA))}
        self.clock = pygame.time.Clock()

        if self.canRender:
            self.screen: pygame.Surface = pygame.display.set_mode((500, 500), flags = pygame.RESIZABLE)
            pygame.display.set_caption("Exoplanet Simulation")
            window_size = pygame.display.get_surface().get_size()
            self.__camera = Camera(dimentions = pygame.Vector2(window_size[0], window_size[1]))
        else:
            self.screen = None
            self.__camera = Camera()

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

    def update(self, delta_t):
        """
        Update all layers registered with the simulation in the order in which they were registered.

        Paramiters:
            float delta_t -> The time in seconds that has passed since the last update
        """
        for layer in self.__layers.values():
            layer.pre_update()#TODO: consider running these as paralell threads

        for layer in self.__layers.values():
            layer.update(delta_t)#TODO: consider running these as paralell threads

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
        --!! WARNING: This is a blocking method !!--

        Runs the simulation untill it terminates or is manualy terminated.

        Simulations that are rendered will capture the mouse pointer.
        In order to pause updating, press 'Escape' - this will also release the mouse pointer.
        """
        running = True
        paused = False
        pygame.mouse.set_visible(False)#TODO: how to deal with non-rendering???
        pygame.event.set_grab(True)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        if self.canRender:
                            pygame.mouse.set_visible(paused)
                            pygame.event.set_grab(not paused)

                elif event.type == pygame.VIDEORESIZE:
                    self.__camera.setWidth(event.w)
                    self.__camera.setHeight(event.h)

            delta_t = self.clock.tick(60) / 1000
            if not paused:
                self.__camera.update(delta_t)
                self.update(delta_t)

            self.render()

            if self.render:
                pygame.display.flip()
                #pygame.display.update()
                self.screen.fill((0, 0, 0))