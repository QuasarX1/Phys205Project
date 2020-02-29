import pygame
import numpy as np
from simulation.main import Simulation
from simulation.layer import Layer, Layer_2D, Layer_3D
from simulation.entities.entity import Entity
from simulation.entities.renderable import Renderable_Simple2DRect
from simulation.entities.prefabs import UnitCube_Wireframe, TriangularPyrimid_Wireframe
from simulation.graphics.camera import Camera
from simulation.graphics.transformations import vector_to_array, array_to_vector, rotationMatrix, applyTransformation

class HUDSimpleSquare(Renderable_Simple2DRect):
    def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), width = 50, height = 50, colour = pygame.Color(100, 100, 100), speed = 100, **kwargs):
        super().__init__(location, facing, width, height, colour, **kwargs)
        self.speed = speed

    def update(self, delta_t):
        self.move_forewards(delta_t * self.speed)

        if self.getLocation().x >= 475:
            self.setLocation(pygame.Vector3(475, 25, 25))
            self.setFacing(self.getFacing() * -1)
        elif self.getLocation().x <= 25:
            self.setLocation(pygame.Vector3(25, 25, 25))
            self.setFacing(self.getFacing() * -1)



class BoringCube(UnitCube_Wireframe):
    def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 50, colour = pygame.Color(100, 100, 100), speed = 100, **kwargs):
        super().__init__(location, facing, vertical, scale, colour, **kwargs)
        self.speed = speed#np.abs(startSpeed)# Using np.abs returns an int32 not an int - causes an array to be produced when multyplying by a vector

    def update(self, delta_t):
        pass

class BoringTriangularPyrimid(TriangularPyrimid_Wireframe):
    def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 50, colour = pygame.Color(100, 100, 100), speed = 100, **kwargs):
        super().__init__(location, facing, vertical, scale, colour, **kwargs)
        self.speed = speed#np.abs(startSpeed)# Using np.abs returns an int32 not an int - causes an array to be produced when multyplying by a vector

    def update(self, delta_t):
        pass



class MovingCube(BoringCube):
    def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 50, colour = pygame.Color(100, 100, 100), speed = 100, **kwargs):
        super().__init__(location, facing, vertical, scale, colour, speed, **kwargs)

    def update(self, delta_t):
        self.move_forewards(delta_t * self.speed)

        if self.getLocation().x >= 475:
            self.setLocation(pygame.Vector3(475, 25, 25))
            self.setFacing(self.getFacing() * -1)
        elif self.getLocation().x <= 25:
            self.setLocation(pygame.Vector3(25, 25, 25))
            self.setFacing(self.getFacing() * -1)

class MovingTriangularPyrimid(BoringTriangularPyrimid):
    def __init__(self, location = pygame.Vector3(25, 25, 25), facing = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 50, colour = pygame.Color(100, 100, 100), speed = 100, **kwargs):
        super().__init__(location, facing, vertical, scale, colour, speed, **kwargs)

    def update(self, delta_t):
        self.move_forewards(delta_t * self.speed)

        if self.getLocation().x >= 475:
            self.setLocation(pygame.Vector3(475, 25, 25))
            self.setFacing(self.getFacing() * -1)
        elif self.getLocation().x <= 25:
            self.setLocation(pygame.Vector3(25, 25, 25))
            self.setFacing(self.getFacing() * -1)



def addBooringCube(layer, location, name):
    layer.addEntity(name, BoringCube(pygame.Vector3(location[0], location[1], location[2]), pygame.Vector3(-1, 0, 0), colour = pygame.Color(255, 0, 0, 175)))



def runExampleSim():
    # Create a simulation object
    sim = Simulation()

    # Alter the properties of the camera
    camera = sim.getCamera()
    camera.setLocation(pygame.Vector3(0, 0, -200))
    #camera.setLocation(pygame.Vector3(-camera.getWidth() / 2, -camera.getHeight() / 2, -200))
    camera.setFov(np.pi / 2)

    # Add new layers
    sim.addLayer("test_3D", Layer_3D(pygame.Surface((500, 500), pygame.SRCALPHA)))

    # Add entities to the "defult" layer
    #sim.getLayer("defult").addEntity("test", HUDSimpleSquare())

    ## Add entities to the "test_3D" layer
    #layer_3D = sim.getLayer("test_3D")
    #layer_3D.addEntity("test_moving_object", MovingCube(pygame.Vector3(475, 25, 25), pygame.Vector3(-1, 0, 0), colour = pygame.Color(255, 0, 0, 175)))
    ##layer_3D.addEntity("test_moving_object", MovingCube(pygame.Vector3(475, 25, 25), pygame.Vector3(-1, 0, 0), colour = pygame.Color(255, 0, 0, 175)))
    #layer_3D.addEntity("test_static_object", BoringCube(pygame.Vector3(475, 25, 25), pygame.Vector3(-1, 0, 0), colour = pygame.Color(255, 0, 0, 175)))

    # Add entities to the "test_3D" layer
    layer_3D = sim.getLayer("test_3D")
    addBooringCube(layer_3D, (0, 0, 0), "0")
    addBooringCube(layer_3D, (50, 0, 0), "1")
    addBooringCube(layer_3D, (0, 50, 0), "2")
    addBooringCube(layer_3D, (50, 50, 0), "3")
    addBooringCube(layer_3D, (100, 0, 0), "4")
    addBooringCube(layer_3D, (100, 50, 0), "5")
    
    sim.run()
