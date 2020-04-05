import pygame
from simulation.entities.entity import Entity

class Renderable_2D(object):# Foreward declaration of Renderable_2D
    pass
class Renderable_3D(object):# Foreward declaration of Renderable_3D
    pass
class Camera(object):# Foreward declaration of Camera
    pass

class Layer(object):
    """
    A layer of entities in a simulation.
    Holds a group of similar entities and handles updating of entities.

    This is a base class and must be inherited.
    The "update" method MUST be overridden in a subclass!

    Constructor:
        pygame.Surface surface -> The surface on which to render the layer
                                  Can be omitted if the layer is to be registered to a simulation (pygame.Surface((1, 1), pygame.SRCALPHA))
        pygame.Color backgroundColour -> The background colour used to fill the pygame.Surface between renders (pygame.Color(0, 0, 0, 0))
        bool canRander -> Can the layer be rendered? (True)
    """

    def __init__(self, surface: pygame.Surface = pygame.Surface((1, 1), pygame.SRCALPHA), backgroundColour: pygame.Color = pygame.Color(0, 0, 0, 0), canRender: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.__canRender = canRender
        self.__entities = {}
        self.surface = surface
        self.backgroundColour = backgroundColour

    def isRenderable(self):
        return self.__canRender

    def show(self):
        self.__canRender = True

    def hide(self):
        self.__canRender = False

    def getSurface(self):
        return self.surface

    def setSurface(self, new_surface):
        self.surface = new_surface

    def getBackgroundColour(self):
        return self.backgroundColour

    def setBackgroundColour(self, new_background_colour):
        self.backgroundColour = new_background_colour

    def getEntity(self, name: str):
        """
        Returns a reference to an entity registered with the layer.

        Paramiters:
            str name -> The name the entity was registered with
        """
        if name in self.__entities.keys():
            return self.__entities[name]
        else:
            return None

    def addEntity(self, name: str, entity: Entity):
        """
        Regsisters an entity with the layer.

        Paramiters:
            str name -> The name the new entity should be registered with
            Entity entity -> The entity to register
        """
        raise NotImplementedError("This method must be overridden in an inheriting class.")

    def removeEntity(self, name: str):
        """
        Un-registers an existing entity from the layer.

        Paramiters:
            str name -> The name of the existing entity that should be un-registered
        """
        if name in self.__entities.keys():
            self.__entities.pop(name, None)

    def pre_update(self):
        """
        Calls the "pre_update" method of all registered entities.
        """
        for entity in self.__entities.values():
            entity.pre_update()

    def update(self, delta_t, simulation):
        """
        Updates all registered entities.

        Paramiters:
            float delta_t -> The time in seconds that has passed since the last update
        """
        for entity in self.__entities.values():
            entity.update(delta_t, simulation)

    def post_update(self):
        """
        Calls the "post_update" method of all registered entities.
        """
        for entity in self.__entities.values():
            entity.post_update()

    def render(self, pixelsPerMeter = 1, surfaceOveride: pygame.Surface = None):
        """
        --!! WARNING !!-- This method throws a "NotImplementedError" - it MUST be overridden in a subclass

        Renders all the entities in the layer.

        Paramiters:
            pygame.Surface surfaceOveride -> Specify a different surface to render to instead of the defult one (None)
        """
        raise NotImplementedError("This method must be overridden in an inheriting class.")

class Layer_2D(Layer):
    """
    A layer specificly for 2D rendered entities (that inherit from "Renderable_2D").

    Constructor:
        pygame.Surface surface -> The surface on which to render the layer
                                  Can be omitted if the layer is to be registered to a simulation (pygame.Surface((1, 1), pygame.SRCALPHA))
        pygame.Color backgroundColour -> The background colour used to fill the pygame.Surface between renders (pygame.Color(0, 0, 0, 0))
        bool canRander -> Can the layer be rendered? (True)
    """

    def addEntity(self, name: str, entity: Renderable_2D):
        """
        Registers a new Renderable_2D entity with the simulation.

        Paramiters:
            str name -> The name the new entity should be registered with
            Renderable_2D entity -> The entity to register
        """
        if not issubclass(type(entity), Renderable_2D):
            raise TypeError("The entities added to a 2D layer must be 2D renderables.")

        if name not in self._Layer__entities.keys():
            self._Layer__entities[name] = entity
        else:
            raise KeyError("An entity already exists with the name {}.".format(name))

    def render(self, surfaceOveride: pygame.Surface = None):
        """
        Renders all entities in the layer provide the layer is allowed to be rendered.

        Paramiters:
            pygame.Surface surfaceOveride -> Specify a different surface to render to instead of the defult one (None)
        """
        if self.isRenderable():
            self.surface.fill(self.backgroundColour)

            if surfaceOveride is None:
                for entity in self._Layer__entities.values():
                    entity.render(self.surface)
            else:
                for entity in self._Layer__entities.values():
                    entity.render(surfaceOveride)

class Layer_3D(Layer):
    """
    A layer specificly for 3D rendered entities (that inherit from "Renderable_3D").

    Constructor:
        pygame.Surface surface -> The surface on which to render the layer
                                  Can be omitted if the layer is to be registered to a simulation (pygame.Surface((1, 1), pygame.SRCALPHA))
        pygame.Color backgroundColour -> The background colour used to fill the pygame.Surface between renders (pygame.Color(0, 0, 0, 0))
        bool canRander -> Can the layer be rendered? (True)
    """

    def addEntity(self, name: str, entity: Renderable_3D):
        """
        Registers a new Renderable_3D entity with the simulation.

        Paramiters:
            str name -> The name the new entity should be registered with
            Renderable_3D entity -> The entity to register
        """
        if not issubclass(type(entity), Renderable_3D):
            raise TypeError("The entities added to a 3D layer must be 3D renderables.")

        if name not in self._Layer__entities.keys():
            self._Layer__entities[name] = entity
        else:
            raise KeyError("An entity already exists with the name {}.".format(name))

    def render(self, camera: Camera, pixelsPerMeter = 1, surfaceOveride: pygame.Surface = None):
        """
        Renders all entities in the layer provide the layer is allowed to be rendered.
        Rendering is done with respect to the camera's position and orientation.

        Paramiters:
            Camera camera -> The camera object for the simulation
            pygame.Surface surfaceOveride -> Specify a different surface to render to instead of the defult one (None)
        """
        if self.isRenderable():
            self.surface.fill(self.backgroundColour)

            
            if surfaceOveride is None:
                for entity in self._Layer__entities.values():
                    entity.render(self.surface, camera, pixelsPerMeter)
            else:
                for entity in self._Layer__entities.values():
                    entity.render(surfaceOveride, camera, pixelsPerMeter)

from simulation.entities.renderable import Renderable_2D, Renderable_3D
from simulation.graphics.camera import Camera