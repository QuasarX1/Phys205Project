from lxml import etree, objectify
import pygame

local_schema_location = "../simulation/custom_xml/simulation_layout_schema.xsd"
local_test_xml_location = "../simulation/custom_xml/example_layout.xml"

def xml_bool(value: str):
    return value == "true"

def createPygameVector2(xml_vector2):
    return pygame.Vector2(float(xml_vector2.attrib["x"]), float(xml_vector2.attrib["y"]))

def createPygameVector3(xml_vector3):
    return pygame.Vector3(float(xml_vector3.attrib["x"]), float(xml_vector3.attrib["y"]), float(xml_vector3.attrib["z"]))

def createPygameColor(xml_color):
    return pygame.Color(int(xml_color.attrib["r"]), int(xml_color.attrib["g"]), int(xml_color.attrib["b"]), int(xml_color.attrib["a"]))

def load_XML(xml_document: str, xml_schema: str = local_schema_location):
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

def load_XML_without_schema(xml_document: str):
    xml_file = open(xml_document, "r", encoding='utf-8')
    tree = objectify.parse(xml_file)
    xml_file.close()
    return tree