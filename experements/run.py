import sys

optionalParamiters = ("--file", "--timescale")
flags = ("--help", "--show")

def parseCommandlineArgs(argv, flags, optionalParamiters):
    arguments = []
    for argument in argv:
        for value in argument.split("="):
            arguments.append(value)

    def extractValue(arguments, i):
        if i < len(arguments) - 1:
            value = arguments[i + 1]
            if value in optionalParamiters or value in flags:
                raise ValueError("Malformed list of argument strings. The value expected for paramiter {} was instead annother paramiter or flag.".format(arguments[i]))
            return value
        else:
            raise ValueError("Malformed list of argument strings. The paramiter {} was the final argument provided and therfore has no associated value.".format(arguments[i]))

    flagsPresent = [False for i in range(len(flags))]
    argumentsPresent = [False for i in range(len(optionalParamiters))]
    argumentsDict = {}

    for i in range(1, len(arguments)):
        argument = arguments[i]
        if argument in flags:
            flagsPresent[flags.index(argument)] = True
        elif argument in optionalParamiters:
            argumentsPresent[optionalParamiters.index(argument)] = True
            argumentsDict[argument] = extractValue(arguments, i)
            i += 1

    return flagsPresent, argumentsPresent, argumentsDict

flagsPresent, argumentsPresent, argumentsDict = parseCommandlineArgs(sys.argv, flags, optionalParamiters)

if flagsPresent[0]:
    print("Help for running simulation experements:")
    print()
    print("    Command Flags:")
    for flag in flags:
        print("        {}".format(flag))
    print()
    print("    Command Arguments:")
    for paramiter in optionalParamiters:
        print("        {}".format(paramiter))
    print()
    sys.exit()

from locate_simulation_library import simulation as sim, local_test_xml_location

kwargs = {}
flags_kwargs_map = {"--show":"forceVisable"}
arguments_kwargs_map = {"--file":("path_to_xml", str), "--timescale":("forceTimescale", float)}
for i in range(1, len(flags)):
    kwargs[flags_kwargs_map[flags[i]]] = flagsPresent[i]
for i, paramiter in enumerate(optionalParamiters):
    if argumentsPresent[i]:
        kwargs[arguments_kwargs_map[paramiter][0]] = arguments_kwargs_map[paramiter][1](argumentsDict[paramiter])

simulation = sim.Simulation.create_from_xml(**kwargs) if "path_to_xml" in list(kwargs.keys()) else sim.Simulation.create_from_xml(path_to_xml = local_test_xml_location, **kwargs)

simulation.run()