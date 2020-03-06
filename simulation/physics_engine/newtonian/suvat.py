
def final_velocity_without_displacement(initial_velocity, acceleration, time):
    return initial_velocity + acceleration * time

def displacement_without_final_velocity(initial_velocity, time, acceleration):
    return initial_velocity * time + 0.5 * acceleration * (time**2)

def displacement_without_acceleration(initial_velocity, final_velocity, time):
    return 0.5 * (initial_velocity + final_velocity) * time

def final_velocity_without_time(initial_velocity, acceleration, displacement):
    return np.sqrt(initial_velocity**2 + 2*acceleration*displacement)

def displacement_without_initial_velocity(final_velocity, time, acceleration):
    return finalfinal_velocity*time - 0.5*acceleration*(time**2)

def time_without_acceleration(displacement, initial_velocity, final_velocity):
    return (2*displacement)/(initial_velocity+finalfinal_velocity)

def initial_velocity_without_displacement(final_velocity, acceleration, time):
    return final_velocity - acceleration*time

def acceleration_without_displacement(initial_velocity, final_velocity, time):
    return (final_velocity-initial_velocity)/time

def time_without_displacement(initial_velocity, final_velocity, acceleration):
    return (final_velocity-initial_velocity)/acceleration

def initial_velocity_without_acceleration(displacement, time, final_velocity):
    return (2*displacement/time)- final_velocity

def final_velocity_without_acceleration(displacement, time, initial_velocity):
    return (2*displacement/time)- initial_velocity

def initial_velocity_without_time(final_velocity, acceleration, displacement):
    return np.sqrt(final_velocity**2 - 2*acceleration*displacement)

def acceleration_without_time(final_velocity, initial_velocity, displacement):
    return (final_velocity**2 - initial_velocity**2)/2*displacement

def displacement_without_time(final_velocity, initial_velocity, acceleration):
    return (final_velocity**2 - initial_velocity**2)/2*acceleration

