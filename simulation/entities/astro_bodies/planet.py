import pygame

from simulation.entities.prefabs import Sphere
from simulation.physics_engine.newtonian.freeBody import FreeBody
from simulation.entities.astro_bodies.star import Star
from simulation.custom_xml.xml_loading import xml_bool, createPygameVector2, createPygameVector3, createPygameColor

class Planet(FreeBody, Sphere):
    def __init__(self, radius, mass, parentStar: Star, location: pygame.Vector3 = pygame.Vector3(0, 0, 0), facing: pygame.Vector3 = pygame.Vector3(1, 0, 0), vertical: pygame.Vector3 = pygame.Vector3(0, 1, 0), colour: pygame.Color = pygame.Color(255, 255, 255), **kwargs):
        super().__init__(mass = mass,
                         moment_of_inertia = 0,
                         radius = radius,
                         location = parentStar.getLocation() + location,
                         facing = facing,
                         vertical = vertical,
                         colour = colour,
                         **kwargs)

        parentStar.bindStarSystemEntity(self)
        #TODO: change moment of inertia

    @staticmethod
    def PlanetFromXML(entity_xml, layer):
        rotational_period = float(entity_xml.free_body.attrib["rotational_period"])
        angular_velocity = 360 / rotational_period if rotational_period != 0 else 0
        return {"entity": Planet(radius = float(entity_xml.attrib["radius"]),
                                 mass = float(entity_xml.free_body.attrib["mass"]),
                                 parentStar = layer.getEntity(entity_xml.attrib["parent_star"]),
                                 colour = createPygameColor(entity_xml.colour),
                                 location = createPygameVector3(entity_xml.location),
                                 facing = createPygameVector3(entity_xml.facing),
                                 vertical = createPygameVector3(entity_xml.vertical),
                                 initial_velocity = createPygameVector3(entity_xml.free_body.velocity),
                                 initial_angular_velocity = angular_velocity),
                "bound_entities": [binding_tag.text for binding_tag in entity_xml.free_body.getchildren() if binding_tag.tag.split("}")[1] == "bound_entity_name"]}