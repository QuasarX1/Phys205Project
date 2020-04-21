import pygame

from simulation.entities.astro_bodies.star import Star
from simulation.entities.astro_bodies.planet import Planet

class Sun(Star):
    def __init__(self, location = pygame.Vector3(0, 0, 0), initial_velocity = pygame.Vector3(0, 0, 0), **kwargs):
        super().__init__(radius = 6.96 * 10**8,# The Sun's equatorial radius in m
                         temperature = 5700,# Surface tempriture in K
                         mass = 1.989 * 10**30,# Mass of the Sun in Kg
                         initial_velocity = initial_velocity,
                         initial_angular_velocity = 360 / (60 * 60 * 24 * 25.05),# roatates (siderialy) once at the equator every 25.05 Earth days
                         location = location,
                         **kwargs)



class Mercury(Planet):
    def __init__(self, sun, location = None, initial_velocity = None, **kwargs):
        super().__init__(radius = 6.0518 * 10**6,# Equatorial radius in m
                         mass = 3.3011 * 10**23,# Mass in Kg
                         parentStar = sun,
                         initial_velocity = pygame.Vector3(0, 0, 4.7362 * 10**4) if initial_velocity is None else initial_velocity,# Orbital velocity in m/s
                         initial_angular_velocity = 360 / (60 * 60 * 24 * 58.646),# Roatates (siderialy) once at the equator every ...
                         location = pygame.Vector3(5.790905 * 10**10, 0, 0) if location is None else location,# Distance from the Sun in m
                         colour = pygame.Color(255, 150, 0),# Arbitrary colour
                         **kwargs)



class Venus(Planet):
    def __init__(self, sun, location = None, initial_velocity = None, **kwargs):
        super().__init__(radius = 2.4397 * 10**6,# Equatorial radius in m
                         mass = 4.8675 * 10**24,# Mass in Kg
                         parentStar = sun,
                         initial_velocity = pygame.Vector3(0, 0, 3.502 * 10**4) if initial_velocity is None else initial_velocity,# Orbital velocity in m/s
                         initial_angular_velocity = 360 / (60 * 60 * 24 * 243.025),# Roatates (siderialy) once at the equator every ...
                         location = pygame.Vector3(1.08208 * 10**11, 0, 0) if location is None else location,# Distance from the Sun in m
                         colour = pygame.Color(0, 0, 255),# Arbitrary colour
                         **kwargs)



class Earth(Planet):
    def __init__(self, sun, location = None, initial_velocity = None, **kwargs):
        super().__init__(radius = 1.737 * 10**6,# Equatorial radius in m
                         mass = 5.972 * 10**24,# Mass in Kg
                         parentStar = sun,
                         initial_velocity = pygame.Vector3(0, 0, 2.997930184 * 10**4) if initial_velocity is None else initial_velocity,# Orbital velocity in m/s
                         initial_angular_velocity = 360 / (60 * 60 * 23.56),# Roatates (siderialy) once at the equator every 23.56 hours
                         location = pygame.Vector3(1.496 * 10**11, 0, 0) if location is None else location,# Distance from the Sun in m
                         colour = pygame.Color(0, 255, 0),# Arbitrary colour
                         **kwargs)