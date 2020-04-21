from simulation.entities.entity import Entity

class Entity_Reference(object):
    def __init__(self, layer_name: str, entity_name: str):
        self.layer_name = layer_name
        self.entity_name = entity_name

    def getObject(self, sim) -> Entity:
        return sim.getEntity(self.layer_name, self.entity_name)