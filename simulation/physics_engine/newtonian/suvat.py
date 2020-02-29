
def final_velocity(initial_velocity, acceleration, time):
    return initial_velocity + acceleration * time

def displacement1(initial_velocity, time, acceleration):
    return initial_velocity * time + 0.5 * acceleration * (time**2)

def displacement2(initial_velocity, final_velocity, time):
    return 0.5 * (initial_velocity + final_velocity) * time

