import pygame
from pygame import Vector3, Rect, Color
import sys

pygame.init()

def forceDueToG(M, m, r):
    return -6.67384 * 10**(-11) * M * m / (r**2)

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

Simulation().run()