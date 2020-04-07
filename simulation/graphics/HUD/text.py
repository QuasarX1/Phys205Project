import pygame
from enum import Enum
from simulation.entities.renderable import Renderable_2D

class ReferencePoint(Enum):
    top_left = 0,
    top_centre = 1,
    top_right = 2,
    centre_left = 3,
    centre = 4,
    centre_right = 5,
    bottom_left = 0,
    bottom_centre = 1,
    bottom_right = 2

class Text(Renderable_2D):
    def __init__(self, text: str, font_face: str, size: int = 1, referencePoint: ReferencePoint = ReferencePoint.top_left,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, *args, **kwargs)
        self.__fontFace = font_face
        self.__fontSize = size
        self.__font = None
        self.__createFont()
        self.__text = text
        self.__colour = colour
        self.__renderedText = None
        self.__renderText()
        self.__referencePoint = referencePoint

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

    def getTopLeftPixelCoordinates(self, surface: pygame.Surface):
        if self.__referencePoint == ReferencePoint.top_left:
            xOffset = 0
            yOffset = 0
        elif self.__referencePoint == ReferencePoint.top_centre:
            xOffset = self.__renderedText.get_width() / 2
            yOffset = 0
        elif self.__referencePoint == ReferencePoint.top_right:
            xOffset = self.__renderedText.get_width()
            yOffset = 0
        elif self.__referencePoint == ReferencePoint.centre_left:
            xOffset = 0
            yOffset = self.__renderedText.get_height() / 2
        elif self.__referencePoint == ReferencePoint.centre:
            xOffset = self.__renderedText.get_width() / 2
            yOffset = self.__renderedText.get_height() / 2
        elif self.__referencePoint == ReferencePoint.centre_right:
            xOffset = self.__renderedText.get_width()
            yOffset = self.__renderedText.get_height() / 2
        elif self.__referencePoint == ReferencePoint.bottom_left:
            xOffset = 0
            yOffset = self.__renderedText.get_height()
        elif self.__referencePoint == ReferencePoint.bottom_centre:
            xOffset = self.__renderedText.get_width() / 2
            yOffset = self.__renderedText.get_height()
        elif self.__referencePoint == ReferencePoint.bottom_right:
            xOffset = self.__renderedText.get_width()
            yOffset = self.__renderedText.get_height()

        return (self.getLocation().x * surface.get_width() - xOffset, self.getLocation().y * surface.get_height() - yOffset)

    def getWidth(self):
        return self.__renderedText.get_width() 

    def getHeight(self):
        return self.__renderedText.get_height()

    def render(self, surface: pygame.Surface):
        surface.blit(self.__renderedText, self.getTopLeftPixelCoordinates(surface))



class UpdatingText(Text):
    def __init__(self, function, font_face: str, size: int = 1, objectReferences: dict = {},
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        self.__objects = objectReferences
        self.__function = function
        super().__init__(text = str(self.__function(self)), font_face = font_face, size = size,
                         location = location, facing = facing, vertical = vertical, colour = colour, *args, **kwargs)

    def getReferencedObject(self, dictKey):
        return self.__objects[dictKey]

    def update(self, delta_t, simulation):
        new_text = str(self.__function(self))
        if self.getText() != new_text:# This removes the redundant processing for re-creating the font
            self.setText(new_text)