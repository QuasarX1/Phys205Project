from simulation.physics_engine.constants import G

def forceFromMassAcceleration(mass, acceleration):
    """Finds force using f = ma """
    return mass * acceleration

def massFromForceAcceleration(force, acceleration):
    """Finds mass using m = f/a """
    return force / acceleration

def accelerationFromForceMass(force, mass):
    """Finds acceleration using a = f/m"""
    return force / mass

def forceBetweenTwoLargeBodies(mass1, mass2, radius):
    """Finds force using F1 = F2 = G ((m1 x m2)/r^2)"""
    return -G * mass1 * mass2 / radius**2

def radiusFromForceMassBetweenTwoLargeBodies(mass1, mass2, force):
    """Finds radius from F1 = F2 = G ((m1 x m2)/r^2)"""
    return (-G * ((mass1 * mass2) / force))**1 / 2

def massFromRadiusForceBetweenTwoLargeBodies(mass, force, radius):
    """Finds the other mass from F1 = F2 = G ((m1 x m2)/r^2)"""
    #return (bob.G * ((mass1 * mass2)/force))**1/2
    return 1/(-G * (mass / (force * radius**2)))