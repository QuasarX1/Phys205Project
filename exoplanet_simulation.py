import simulation as sim
from star import Star

simulation = sim.Simulation()

HUD = sim.layer.Layer_2D()
simulation.addLayer("HUD", HUD)

simulation_layer = sim.layer.Layer_3D()
simulation.addLayer("simulation_layer", simulation_layer)


simulation.addEntity("target_star", Star(10, 100, 500000))