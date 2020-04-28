from lxml import etree, objectify
import pygame
import numpy as np
from locate_simulation_library import simulation as sim, local_schema_location, local_test_xml_location

def createPygameVector2(xml_vector2):
    return pygame.Vector2(float(xml_vector2.attrib["x"]), float(xml_vector2.attrib["y"]))

def createPygameVector3(xml_vector3):
    return pygame.Vector3(float(xml_vector3.attrib["x"]), float(xml_vector3.attrib["y"]), float(xml_vector3.attrib["z"]))

def createPygameColor(xml_color):
    return pygame.Color(int(xml_color.attrib["r"]), int(xml_color.attrib["g"]), int(xml_color.attrib["b"]), int(xml_color.attrib["a"]))

def _createEntityFromXML(entity_xml, layer):
    entityTypeString = entity_xml.tag.split("}")[1]

    if entityTypeString == "planet":
        rotational_period = float(entity_xml.free_body.attrib["rotational_period"])
        angular_velocity = 360 / rotational_period if rotational_period != 0 else 0
        return {"entity": sim.entities.astro_bodies.Planet(radius = float(entity_xml.attrib["radius"]),
                                                           mass = float(entity_xml.free_body.attrib["mass"]),
                                                           parentStar = layer.getEntity(entity_xml.attrib["parent_star"]),
                                                           colour = createPygameColor(entity_xml.colour),
                                                           location = createPygameVector3(entity_xml.location),
                                                           facing = createPygameVector3(entity_xml.facing),
                                                           vertical = createPygameVector3(entity_xml.vertical),
                                                           initial_velocity = createPygameVector3(entity_xml.free_body.velocity),
                                                           initial_angular_velocity = angular_velocity),
                "bound_entities": [binding_tag.text for binding_tag in entity_xml.free_body.getchildren() if binding_tag.tag.split("}")[1] == "bound_entity_name"]}

    elif entityTypeString == "star":
        rotational_period = float(entity_xml.free_body.attrib["rotational_period"])
        angular_velocity = 360 / rotational_period if rotational_period != 0 else 0
        return {"entity": sim.entities.astro_bodies.Star(radius = float(entity_xml.attrib["radius"]),
                                                         mass = float(entity_xml.free_body.attrib["mass"]),
                                                         temperature = float(entity_xml.attrib["tempriture"]),
                                                         location = createPygameVector3(entity_xml.location),
                                                         facing = createPygameVector3(entity_xml.facing),
                                                         vertical = createPygameVector3(entity_xml.vertical),
                                                         initial_velocity = createPygameVector3(entity_xml.free_body.velocity),
                                                         initial_angular_velocity = angular_velocity),
                "bound_entities": [binding_tag.text for binding_tag in entity_xml.free_body.getchildren() if binding_tag.tag.split("}")[1] == "bound_entity_name"]}
    
    elif entityTypeString == "croshair_3D":
        return {"entity": sim.entities.prefabs.Croshair_3D(location = createPygameVector3(entity_xml.location),
                                                           facing = createPygameVector3(entity_xml.facing),
                                                           vertical = createPygameVector3(entity_xml.vertical),
                                                           colour = createPygameColor(entity_xml.colour),
                                                           scale = float(entity_xml.attrib["scale"]))}

    elif entityTypeString == "triangularpyrimid_wireframe":
        return {"entity": sim.entities.prefabs.TriangularPyrimid_Wireframe(location = createPygameVector3(entity_xml.location),
                                                                           facing = createPygameVector3(entity_xml.facing),
                                                                           vertical = createPygameVector3(entity_xml.vertical),
                                                                           colour = createPygameColor(entity_xml.colour),
                                                                           scale = float(entity_xml.attrib["scale"]))}

    elif entityTypeString == "unitcube_wireframe":
        return {"entity": sim.entities.prefabs.UnitCube_Wireframe(location = createPygameVector3(entity_xml.location),
                                                                  facing = createPygameVector3(entity_xml.facing),
                                                                  vertical = createPygameVector3(entity_xml.vertical),
                                                                  colour = createPygameColor(entity_xml.colour),
                                                                  scale = float(entity_xml.attrib["scale"]))}

    elif entityTypeString == "sphere":
        return {"entity": sim.entities.prefabs.Sphere(location = createPygameVector3(entity_xml.location),
                                                      facing = createPygameVector3(entity_xml.facing),
                                                      vertical = createPygameVector3(entity_xml.vertical),
                                                      colour = createPygameColor(entity_xml.colour),
                                                      radius = float(entity_xml.attrib["radius"]))}

    elif entityTypeString == "croshair":
        return {"entity": sim.entities.prefabs.Croshair(location = createPygameVector3(entity_xml.location),
                                                        colour = createPygameColor(entity_xml.colour),
                                                        scale = float(entity_xml.attrib["scale"]))}

    elif entityTypeString == "renderable_simple2Dcircle":
        return {"entity": sim.entities.Renderable_Simple2DCircle(location = createPygameVector3(entity_xml.location),
                                                                 facing = createPygameVector3(entity_xml.facing),
                                                                 vertical = createPygameVector3(entity_xml.vertical),
                                                                 colour = createPygameColor(entity_xml.colour),
                                                                 radius = float(entity_xml.attrib["radius"]))}

    elif entityTypeString == "renderable_2Dline":
        return {"entity": sim.entities.Renderable_2DLine(length = float(entity_xml.attrib["length"]),
                                                         point1 = createPygameVector3(entity_xml.facing),
                                                         point2 = createPygameVector3(entity_xml.vertical),
                                                         colour = createPygameColor(entity_xml.colour),
                                                         point1_is_midpoint = bool(entity_xml.attrib["point1_is_midpoint"]))}

def load_XML(xml_document: str, xml_schema: str):
    xml_file = open(xml_document, "r", encoding='utf-8')
    schema_file = open(xml_schema, "r", encoding='utf-8')
    schema = etree.XMLSchema(file = schema_file)
    schema_file.close()
    try:
        tree = objectify.parse(xml_file, objectify.makeparser(schema = schema))
    except etree.XMLSyntaxError:
        raise ValueError("The XML provided did not conform to the associated schema.")
    xml_file.close()
    return tree

def __load_XML_without_schema(xml_document: str):
    xml_file = open(xml_document, "r", encoding='utf-8')
    tree = objectify.parse(xml_file)
    xml_file.close()
    return tree

def create_simulation(xml_document: str = local_test_xml_location, forceVisable: bool = False, forceTimescale: float = None):
    #tree = load_XML(xml_document, local_schema_location)
    tree = __load_XML_without_schema(xml_document)
    simulation_xml = tree.getroot()

    hasCamera = hasattr(simulation_xml, "camera")
    if hasCamera:
        simulation = sim.Simulation(cameraDimentions = pygame.Vector2(float(simulation_xml.camera.get("width")), float(simulation_xml.camera.get("height"))),
                                    renderMode = sim.RenderMode.real_time if forceVisable or bool(simulation_xml.get("render_capability")) else sim.RenderMode.no_render,
                                    timeScale = float(simulation_xml.get("timescale") if forceTimescale is None else forceTimescale))
        camera_xml = simulation_xml.camera
        camera = simulation.getCamera()
        camera.setFov(np.pi * float(camera_xml.get("field_of_vision")))
        camera.setLocation(createPygameVector3(camera_xml.location))
        camera.setFacing(createPygameVector3(camera_xml.facing))
        camera.setVertical(createPygameVector3(camera_xml.vertical))
    else:
        simulation = sim.Simulation(renderMode = sim.RenderMode.real_time if forceVisable or bool(simulation_xml.get("render_capability")) else sim.RenderMode.no_render,
                                    timeScale = float(simulation_xml.get("timescale") if forceTimescale is None else forceTimescale))

    for layer_xml in simulation_xml.getchildren()[1 if hasCamera else 0:]:
        if layer_xml.tag == "comment":
            continue

        layerTypeString = layer_xml.tag.split("}")[1]
        if layerTypeString == "layer_2D":
            layer = sim.Layer_2D(layer_xml.attrib["render_capability"])

        elif layerTypeString == "layer_3D":
            layer = sim.Layer_3D(layer_xml.attrib["render_capability"])

        elif layerTypeString == "Layer_Mixed":
            layer = sim.Layer_Mixed(layer_xml.attrib["render_capability"])

        simulation.addLayer(layer_xml.attrib["name"], layer)

        bindingDict = {}
        for entity_xml in layer_xml.getchildren():
            entityName = entity_xml.attrib["name"]
            entityCreationResult = _createEntityFromXML(entity_xml, layer)
            entity = entityCreationResult["entity"]
            layer.addEntity(entityName, entity)

            if "bound_entities" in entityCreationResult.keys():
                bindingDict[entityName] = entityCreationResult["bound_entities"]

        for key in bindingDict.keys():
            for entity_name in bindingDict[key]:
                layer.getEntity(key).bindEntity_by_name(entity_name, layer)

    return simulation