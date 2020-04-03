import pygame
from simulation.entities.renderable import Renderable_2D

class Text(Renderable_2D):
    def __init__(self, text: str, font_face: str, size: int = 1,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        super().__init__(location, facing, vertical, *args, **kwargs)
        self.__fontFace = font_face
        self.__fontSize = size
        self.__font = None
        self.__createFont()
        self.__text = text
        self.__colour = colour
        self.__renderedText = None
        self.__renderText()

    def getText(self):
        return self.__text

    def setText(self, new_text):
        self.__text = new_text
        self.__renderText()

    def getFontFace(self):
        return self.__fontFace

    def setFontFace(self, new_font_face):
        self.__fontFace = new_font_face
        self.__createFont()
        self.__renderText()

    def getFontSize(self):
        return self.__fontSize

    def setFontSize(self, new_font_size):
        self.__fontSize = new_font_size
        self.__createFont()
        self.__renderText()

    def getColour(self) -> pygame.Color:
        return self.__colour

    def setColour(self, new_colour: pygame.Color):
        self.__colour = new_colour
        self.__renderText()

    def __createFont(self):
        self.__font = pygame.font.Font(self.__fontFace, self.__fontSize)

    def __renderText(self):
        self.__renderedText = self.__font.render(self.__text, 1, self.__colour)

    def update(self, delta_t, simulation):
        pass

    def render(self, surface: pygame.Surface):
        surface.blit(self.__renderedText, (self.getLocation().x, self.getLocation().y))