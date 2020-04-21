import pygame
from pygame import Vector3, Rect, Color
import sys
import numpy as np

pygame.init()

def vector_to_array(vector: pygame.Vector3):
    return np.array([[vector.x], [vector.y], [vector.z]])

def array_to_vector(array: np.ndarray):
    return pygame.Vector3(array[0], array[1], array[2])

def rotationMatrix(axis: Vector3, angle: float):
    length = np.sqrt(axis.x**2 + axis.y**2 + axis.z**2)
    axis.x /= length
    axis.y /= length
    axis.z /= length
    
    mat = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    mat[0, 0] = axis.x**2 * (1 - np.cos(angle)) + np.cos(angle)
    mat[0, 1] = axis.y * axis.x * (1 - np.cos(angle)) - axis.z * np.sin(angle)
    mat[0, 2] = axis.z * axis.x * (1 - np.cos(angle)) + axis.y * np.sin(angle)

    mat[1, 0] = axis.x * axis.y * (1 - np.cos(angle)) + axis.z * np.sin(angle)
    mat[1, 1] = axis.y**2 * (1 - np.cos(angle)) + np.cos(angle)
    mat[1, 2] = axis.z * axis.y * (1 - np.cos(angle)) - axis.x * np.sin(angle)

    mat[2, 0] = axis.x * axis.z * (1 - np.cos(angle)) - axis.y * np.sin(angle)
    mat[2, 1] = axis.y * axis.z * (1 - np.cos(angle)) + axis.x * np.sin(angle)
    mat[2, 2] = axis.z**2 * (1 - np.cos(angle)) + np.cos(angle)

    return mat

def applyTransformation(transformation_matrix: np.ndarray, vector: pygame.Vector3):
    return array_to_vector(transformation_matrix.dot(vector_to_array(vector)))

#xPoint = np.array([[1], [0], [0]])
#zAxis = Vector3(0, 0, 3)
#print(xPoint)
#print(rotationMatrix(zAxis, np.pi / 2))
#print(rotationMatrix(zAxis, np.pi / 2).dot(xPoint))

#print(array_to_vector(xPoint))
#print(vector_to_array(zAxis))

point = Vector3(3.0, 0.0, 0.0)
zAxix = Vector3(0.0, 0.0, 1.0)
rotation = rotationMatrix(zAxix, np.pi / 2)
point_image = applyTransformation(rotation, point)
print(point_image)
point_image = applyTransformation(rotation, point)
print(point_image)
point_image = applyTransformation(rotation, point)
print(point_image)
point_image = applyTransformation(rotation, point)
print(point_image)





class Drawable(object):
    def __init__(self):
        self._rect = Rect(0, 0, 50, 50)
        self._colour = Color(255, 255, 255)
    
    def update(self):
        pass

    def getRect(self):
        return self._rect
    
    def getColour(self):
        return self._colour

class Moveable(Drawable):
    def __init__(self):
        super().__init__()
    
    def moveUp(self, pixels):
        self._rect = self._rect.move(0, -pixels)
    
    def moveDown(self, pixels):
        self._rect = self._rect.move(0, pixels)
    
    def moveLeft(self, pixels):
        self._rect = self._rect.move(-pixels, 0)
    
    def moveRight(self, pixels):
        self._rect = self._rect.move(pixels, 0)

class TestObject(Moveable):
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.distance = 0
        self.maxDistance = 450

    def update(self):
        if self.maxDistance == 0:
            return

        if self.direction == 0:
            self.moveRight(1)
            self.distance += 1

        elif self.direction == 1:
            self.moveDown(1)
            self.distance += 1

        elif self.direction == 2:
            self.moveLeft(1)
            self.distance += 1

        else:
            self.moveUp(1)
            self.distance += 1
        
        if self.distance == self.maxDistance:
            self.distance = 0
            self.direction += 1
            if self.direction == 4:
                self.direction = 0
                self.maxDistance -= 100
                self.moveDown(50)
                self.moveRight(50)

class Simulation(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.entities = []

        self.entities.append(TestObject())
    
    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #print(getClockSeconds())

            for i in range(len(self.entities)):
                self.entities[i].update()
            
            for i in range(len(self.entities)):
                self.drawObject(self.entities[i])

            pygame.display.flip()
            #pygame.display.update()

    def drawObject(self, shape: Drawable):
        pygame.draw.rect(self.screen, shape.getColour(), shape.getRect())
    
    def getClockSeconds(self):
        return self.clock.get_time() / 1000