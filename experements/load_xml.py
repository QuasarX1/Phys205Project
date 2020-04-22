from lxml import etree, objectify
import pygame
from locate_simulation_library import simulation as sim, local_schema_location, local_test_xml_location

def createPygameVector2(xml_vector2):
    return pygame.Vector2(float(xml_vector2.attrib["x"]), float(xml_vector2.attrib["y"]))

def createPygameVector3(xml_vector3):
    return pygame.Vector3(float(xml_vector3.attrib["x"]), float(xml_vector3.attrib["y"]), float(xml_vector3.attrib["z"]))

def _createEntityFromXML(entity_xml):
    entityTypeString = entity_xml.tag.split("}")[1]

    if entityTypeString == "star":
        return {"entity": sim.entities.astro_bodies.Star(radius = float(entity_xml.attrib["radius"]),
                                              mass = float(entity_xml.free_body.attrib["mass"]),
                                              temperature = float(entity_xml.attrib["tempriture"]),
                                              location = createPygameVector3(entity_xml.location),
                                              facing = createPygameVector3(entity_xml.facing),
                                              vertical = createPygameVector3(entity_xml.vertical),
                                              initial_velocity = createPygameVector3(entity_xml.free_body.velocity),
                                              initial_angular_velocity = float(entity_xml.free_body.attrib["angular_velocity"])),
                "bound_entities": [binding_tag.text for binding_tag in entity_xml.free_body.getchildren() if binding_tag.tag.split("}")[1] == "bound_entity_name"]}
    
    #elif entityTypeString == "star":
    #    return sim.entities.astro_bodies.Star()

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

def create_simulation(xml_document: str = local_test_xml_location):
    #tree = load_XML(xml_document, local_schema_location)
    tree = __load_XML_without_schema(xml_document)
    simulation_xml = tree.getroot()

    hasCamera = hasattr(simulation_xml, "camera")
    if hasCamera:
        simulation = sim.Simulation(cameraDimentions = pygame.Vector2(float(simulation_xml.camera.get("width")), float(simulation_xml.camera.get("height"))), renderMode = sim.RenderMode.real_time if bool(simulation_xml.get("render_capability")) else sim.RenderMode.no_render)
    else:
        simulation = sim.Simulation(renderMode = sim.RenderMode.real_time if bool(simulation_xml.get("render_capability")) else sim.RenderMode.no_render)

    
    
    if hasCamera:
        camera_xml = simulation_xml.camera
        camera = simulation.getCamera()
        camera.setFov(float(camera_xml.get("field_of_vision")))
        #camera.setLocation(createPygameVector3(camera_xml.location))
        #camera.setFacing(createPygameVector3(camera_xml.facing))
        #camera.setVertical(createPygameVector3(camera_xml.vertical))

    for layer_xml in simulation_xml.getchildren()[1 if hasCamera else 0:]:
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
            entityCreationResult = _createEntityFromXML(entity_xml)
            entity = entityCreationResult["entity"]
            layer.addEntity(entityName, entity)

            if "bound_entities" in entityCreationResult.keys():
                for entity_name in entityCreationResult["bound_entities"]:
                    if entityName not in bindingDict.keys():
                        bindingDict[entityName] = [entityName]
                    else:
                        bindingDict[entityName].append(entityName)

        for key in bindingDict.keys():
            for entity_name in bindingDict[key]:
                layer.getEntity(key).bindEntity_by_name(entity_name, layer)

    return simulation