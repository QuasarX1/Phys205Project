import pygame
import numpy as np

class Entity(object):
    def update(self, delta_t):
        raise NotImplementedError("This method must be overridden in an inheriting class.")