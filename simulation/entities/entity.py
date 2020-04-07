import pygame
import numpy as np

class Entity(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__visable = True

    def isVisable(self) -> bool:
        return self.__visable

    def show(self):
        self.__visable = True

    def hide(self):
        self.__visable = False

    def setVisability(self, isVisible: bool):
        self.__visable = isVisible

    def pre_update(self):
        pass

    def update(self, delta_t, simulation):
        raise NotImplementedError("This method must be overridden in an inheriting class.")

    def post_update(self):
        pass