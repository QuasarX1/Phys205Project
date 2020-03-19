import pygame

commands = {}

def commands_stop(simulation, *args, **kwargs):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    return "Stopped simulation"

commands["stop"] = (commands_stop, "Stops the simulation.")



def commands_pause(simulation, *args, **kwargs):
    simulation.pause()
    return "Paused simulation"

commands["pause"] = (commands_pause, "Pauses the simulation.")



def commands_resume(simulation, *args, **kwargs):
    simulation.resume()
    return "Resumed simulation"

commands["resume"] = (commands_resume, "Un-pauses the simulation.")



def commands_runtime(simulation, *args, **kwargs):
    return str(simulation.getRunTime())

commands["runtime"] = (commands_runtime, "Prints the total simulated time so far.")



def commands_seconds(simulation, *args, **kwargs):
    return str(simulation.getRunTime())

commands["seconds"] = (commands_seconds, "Prints the total simulated time so far in seconds.")



def commands_minutes(simulation, *args, **kwargs):
    return str(simulation.getRunTime() / 60)

commands["minutes"] = (commands_minutes, "Prints the total simulated time so far in minutes.")



def commands_hours(simulation, *args, **kwargs):
    return str(simulation.getRunTime() / 3600)

commands["hours"] = (commands_hours, "Prints the total simulated time so far in hours.")



def commands_earth_days(simulation, *args, **kwargs):
    return str(simulation.getRunTime() / 86400)

commands["earth_days"] = (commands_earth_days, "Prints the total simulated time so far in Earth days.")



def commands_earth_years(simulation, *args, **kwargs):
    return str(simulation.getRunTime() / 31557600)# Includes the 0.25 extra day per year

commands["earth_years"] = (commands_earth_years, "Prints the total simulated time so far in Earth years.")



def commands_help(simulation, *args, **kwargs):
    if len(args) == 0:
        output = ""
        for command in commands.keys():
            output += command + "\n"
        return output

    else:
        output = commands[args[0]][1]
        return output

commands["help"] = (commands_help, "help [command?]\nLists all the avalable commands or lists the description of a single command.")