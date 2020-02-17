import pygame
from simulation.entities.moveable import Moveable

class Camera(Moveable):
    def __init__(self):
        self.__width = 300
        self.__height = 200
        self.__focus_distance = 1