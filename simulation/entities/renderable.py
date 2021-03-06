import pygame

from simulation.entities.moveable import Moveable
from simulation.custom_xml.xml_loading import xml_bool, createPygameVector2, createPygameVector3, createPygameColor

class Renderable_2D(Moveable):
    def __init__(self, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        super().__init__(location = location, facing = facing, vertical = vertical, **kwargs)

    def render(self, surface: pygame.Surface):
        raise NotImplementedError("This method must be overridden in an inheriting class.")



class Renderable_2DLine(Renderable_2D):
    def __init__(self, length: float = 1, point1: pygame.Vector3 = pygame.Vector3(0, 0, 0), point2: pygame.Vector3 = pygame.Vector3(1, 0, 0), colour: pygame.Color = pygame.Color(255, 255, 255), point1_is_midpoint: bool = False, **kwargs):
        facing = (point2 - point1).normalize()
        super().__init__(location = point1, facing = facing, vertical = pygame.Vector3(0, 0, 1).cross(facing), **kwargs)
        self.__length = length
        self.__colour = colour
        self.__fromMidpoint = point1_is_midpoint

    def getLength(self) -> float:
        return self.__length

    def setLength(self, new_length: float):
        self.__length = new_length

    def render(self, surface: pygame.Surface):
        if self.__fromMidpoint:
            startPoint = (self.getLocation() - self.getFacing() * self.__length / 2).elementwise() * pygame.Vector3(surface.get_width(), surface.get_height(), 1)
            endpoint = (self.getLocation() + self.getFacing() * self.__length / 2).elementwise() * pygame.Vector3(surface.get_width(), surface.get_height(), 1)
            pygame.draw.line(surface,
                             self.__colour,
                             (startPoint.x, startPoint.y),
                             (endpoint.x, endpoint.y))
        else:
            endpoint = self.getLocation() + self.getFacing() * self.__length
            pygame.draw.line(surface,
                             self.__colour,
                             (self.getLocation().x, self.getLocation().y),
                             (endpoint.x, endpoint.y))

    @staticmethod
    def Renderable_2DLineFromXML(entity_xml, layer):
            return {"entity": Renderable_2DLine(length = float(entity_xml.attrib["length"]),
                                                             point1 = createPygameVector3(entity_xml.facing),
                                                             point2 = createPygameVector3(entity_xml.vertical),
                                                             colour = createPygameColor(entity_xml.colour),
                                                             point1_is_midpoint = xml_bool(entity_xml.attrib["point1_is_midpoint"]))}



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

    @staticmethod
    def Renderable_Simple2DCircleFromXML(entity_xml, layer):
            return {"entity": Renderable_Simple2DCircle(location = createPygameVector3(entity_xml.location),
                                                        facing = createPygameVector3(entity_xml.facing),
                                                        vertical = createPygameVector3(entity_xml.vertical),
                                                        colour = createPygameColor(entity_xml.colour),
                                                        radius = float(entity_xml.attrib["radius"]))}


        
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
        newVertices = []
        for i in range(len(self.__vertices)):
            newVertices.append(pygame.Vector3(self.__vertices[i].dot(self.getHorisontal()), self.__vertices[i].dot(self.getVertical()), self.__vertices[i].dot(self.getFacing())))
        for edge in self.__edges:
            if camera.isInView(self.getLocation() + newVertices[edge[0]] * self.__scale) or camera.isInView(self.getLocation() + newVertices[edge[1]] * self.__scale):
                startPosition = (camera.calculatePerspective(self.getLocation() + newVertices[edge[0]] * self.__scale)).elementwise() * pixelsPerMeter
                endPosition = (camera.calculatePerspective(self.getLocation() + newVertices[edge[1]] * self.__scale)).elementwise() * pixelsPerMeter
           
                pygame.draw.line(surface,
                                 self.__colour,
                                 (startPosition.x, surface.get_height() - startPosition.y),
                                 (endPosition.x, surface.get_height() - endPosition.y))



class Renderable_3DSolid(Renderable_3DWireframe):
    def __init__(self, vertices: list, edges: list, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), scale = 1, colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(vertices = vertices, edges = edges, location = location, facing = facing, vertical = vertical, scale = scale, colour = colour, **kwargs)
    #TODO: compute rendering or not of faces




    
from simulation.entities.prefabs import UnitCube_Wireframe, Sphere