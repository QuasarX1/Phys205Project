import pygame
import numpy as np

class Entity(object):
    def pre_update(self):
        pass

    def update(self, delta_t, simulation):
        raise NotImplementedError("This method must be overridden in an inheriting class.")

    def post_update(self):
        pass