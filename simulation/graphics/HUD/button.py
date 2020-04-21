import pygame
from QuasarCode.edp import Event

from simulation.graphics.HUD.text import Text, ReferencePoint

class Button(Text):
    def __init__(self, simulation, text: str, font_face: str, size: int = 1, referencePoint: ReferencePoint = ReferencePoint.top_left,
                 location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0),
                 vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), *args, **kwargs):
        super().__init__(text = text, font_face = font_face, size = size, referencePoint = referencePoint,
                         location = location, facing = facing, vertical = vertical, colour = colour, *args, **kwargs)
        self.__normalColour = colour
        self.__hoverColour = pygame.Color(int(colour.r / 2), int(colour.g / 2), int(colour.b / 2))
        self.__lastHovered = False
        self.onClick = Event()
        simulation.onClick += self.checkClick

    def checkClick(self, surface: pygame.Surface):
        if self.isVisable() and self.onClick.getTotalSubscribers() > 0 and self.beingHovered(surface):
            self.onClick.run()

    def beingHovered(self, surface: pygame.Surface):
        mousePos = pygame.mouse.get_pos()
        topLeft = self.getTopLeftPixelCoordinates(surface)
        bottomRight = (topLeft[0] + self.getWidth(), topLeft[1] + self.getHeight())
        return mousePos[0] >= topLeft[0] and mousePos[0] <= bottomRight[0] and mousePos[1] >= topLeft[1] and mousePos[1] <= bottomRight[1]

    def update(self, delta_t, simulation):
        hovering = self.beingHovered(simulation.getDisplaySurface())
        if not hovering and self.__lastHovered:
            self.setColour(self.__normalColour)
        elif hovering and not self.__lastHovered:
            self.setColour(self.__hoverColour)
        self.__lastHovered = hovering