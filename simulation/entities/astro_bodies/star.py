import pygame

from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody
from simulation.physics_engine.optics.colour import blackbody_visable_colour
from simulation.custom_xml.xml_loading import xml_bool, createPygameVector2, createPygameVector3, createPygameColor

class Star(FreeBody, Sphere):
    def __init__(self, radius, mass, temperature, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), **kwargs):
        self.__temperature = temperature
        colour = blackbody_visable_colour(temperature)#pygame.Color(255, 255, 0)#TODO: calculate the colour from Temp

        super().__init__(mass = mass, moment_of_inertia = 0, radius = radius, location = location, facing = facing, vertical = vertical, colour = colour, **kwargs)
        #TODO: change moment of inertia
    
    def getTemperature(self):
        return self.__temperature

    def setTemperature(self, new_temperature: float):
        self.__temperature = new_temperature

    def update(self, delta_t, simulation):#TODO: star updates here? or in free body?
        self.setColour(blackbody_visable_colour(self.__temperature))
        self.manual_update_FreeBody(delta_t, simulation)

    def bindStarSystemEntity(self, entity):
        for boundEntity in self.getBoundEntities():
            boundEntity.bindEntity(entity)
            entity.bindEntity(boundEntity)

        self.bindEntity(entity)
        entity.bindEntity(self)

    @staticmethod
    def StarFromXML(entity_xml, layer):
        rotational_period = float(entity_xml.free_body.attrib["rotational_period"])
        angular_velocity = 360 / rotational_period if rotational_period != 0 else 0
        return {"entity": Star(radius = float(entity_xml.attrib["radius"]),
                               mass = float(entity_xml.free_body.attrib["mass"]),
                               temperature = float(entity_xml.attrib["tempriture"]),
                               location = createPygameVector3(entity_xml.location),
                               facing = createPygameVector3(entity_xml.facing),
                               vertical = createPygameVector3(entity_xml.vertical),
                               initial_velocity = createPygameVector3(entity_xml.free_body.velocity),
                               initial_angular_velocity = angular_velocity),
                "bound_entities": [binding_tag.text for binding_tag in entity_xml.free_body.getchildren() if binding_tag.tag.split("}")[1] == "bound_entity_name"]}