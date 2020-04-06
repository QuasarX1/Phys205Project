import pygame
from simulation.entities.moveable import Moveable

class Renderable_2D(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def render(self, surface: pygame.Surface):
        raise NotImplementedError("This method must be overridden in an inheriting class.")



"""
class Renderable_Simple2DRect(Renderable_2D):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 width: float = 10, height: float = 10, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)
        self.__width = width
        self.__height = height
        self.__colour = colour

        self.__rect_casche = None
        self.__generateRect()

    @staticmethod
    def createFromRect(rect: pygame.Rect, facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), colour: pygame.Color = pygame.Color(255, 255, 255)):
        entity = Renderable_Simple2DRect(facing = facing, colour = colour)
        entity.setRect(rect)
        return entity

    def __generateRect(self):
        loc = self.getLocation()
        self.__rect_casche = pygame.Rect(loc.x - self.__width / 2, loc.y - self.__height / 2, self.__width, self.__height)

    def move(self, displacement_vector: pygame.Vector3):
        super().move(displacement_vector)
        self.__generateRect()

    def getWidth(self) -> float:
        self.__width

    def setWidth(self, new_width: float):
        self.__width = new_width
        self.__generateRect()

    def getHeight(self) -> float:
        return self.__height

    def setHeight(self, new_height: float):
        self.__height = new_height
        self.__generateRect()
        
    def getRect(self) -> pygame.Rect:
        return self.__rect_casche

    def setRect(self, new_rect: pygame.Rect):
        self.__rect_casche = new_rect
        self.__width = new_rect.width
        self.__height = new_rect.height
        self.setLocation(pygame.Vector3(new_rect.x + new_rect.width / 2, new_rect.y + new_rect.height / 2, self.getLocation().z))

    def getColour(self) -> pygame.Color:
        return self.__colour

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.__colour, self.__rect_casche)
"""



class Renderable_Simple2DPolygon(Renderable_2D):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 points: list = [pygame.Vector2(-0.5, -0.5), pygame.Vector2(0.5, -0.5), pygame.Vector2(0.5, 0.5), pygame.Vector2(-0.5, 0.5)],
                 scale_factor: float = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)
        self.__points: list = points
        self.__scale = scale_factor
        self.__colour = colour

    def getScaleFactor(self) -> float:
        return self.__scale

    def setScaleFactor(self, new_scale: float):
        self.__scale = new_scale

    def render(self, surface: pygame.Surface):
        pygame.draw.polygon(surface, self.__colour, [(self.getLocation() + point * self.__scale) * pygame.Vector2(surface.get_width(), surface.get_height()) for point in self.__points])



class Renderable_Simple2DCircle(Renderable_2D):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0),
                 radius: float = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)
        self.__points: list = points
        self.__radius = radius
        self.__colour = colour

    def getRadius(self) -> float:
        return self.__radius

    def setRadius(self, new_radius: float):
        self.__radius = new_radius

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.__colour, self.getLocation() * pygame.Vector3(surface.get_width(), surface.get_height(), 1), self.__radius * surface.get_width())


        
from simulation.graphics.camera import Camera

class Renderable_3D(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def render(self, surface: pygame.Surface, camera: Camera, pixelsPerMeter = 1):
        raise NotImplementedError("This method must be overridden in an inheriting class.")

class Renderable_3DWireframe(Renderable_3D):
    def __init__(self, vertices: list, edges: list, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)
        self.__vertices = vertices
        self.__edges = edges
        self.__scale = scale
        self.__colour = colour

    def getColour(self) -> pygame.Color:
        return self.__colour

    def setColour(self, new_colour: pygame.Color):
        self.__colour = new_colour

    def getScaleFactor(self) -> float:
        return self.__scale

    def setScaleFactor(self, new_scale: float):
        self.__scale = new_scale

    def render(self, surface: pygame.Surface, camera: Camera, pixelsPerMeter = 1):
        translation = camera.getLocation()
        translation = pygame.Vector2(translation.x + camera.getWidth() / 2, translation.y + camera.getHeight() / 2)
        for edge in self.__edges:
            if camera.isInView(self.getLocation() + self.__vertices[edge[0]] * self.__scale) or camera.isInView(self.getLocation() + self.__vertices[edge[1]] * self.__scale):
                startPosition = (camera.calculatePerspective(self.getLocation() + self.__vertices[edge[0]] * self.__scale) + translation) * pixelsPerMeter - camera.getHeightOffset() * pygame.Vector2(0, 1)
                endPosition = (camera.calculatePerspective(self.getLocation() + self.__vertices[edge[1]] * self.__scale) + translation) * pixelsPerMeter - camera.getHeightOffset() * pygame.Vector2(0, 1)
           
                pygame.draw.line(surface,
                                 self.__colour,
                                 (startPosition.x, startPosition.y),
                                 (endPosition.x, endPosition.y))



class Renderable_3DSolid(Renderable_3DWireframe):
    def __init__(self, vertices: list, edges: list, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(vertices = vertices, edges = edges, location = location, facing = facing, vertical = vertical, scale = scale, colour = colour, **kwargs)
    #TODO: compute rendering or not of faces