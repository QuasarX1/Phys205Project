import numpy as np
from matplotlib import pyplot as plt
import os

folders = {"Red Dwarf":     (
                            ("./logging_output/RDNR/proxima_centuri_location_logger/Component_Displacement/proxima centuri",
                             "./logging_output/RDNG/proxima_centuri_location_logger/Component_Displacement/proxima centuri",
                             "./logging_output/RDFR/proxima_centuri_location_logger/Component_Displacement/proxima centuri",
                             "./logging_output/RDFG/proxima_centuri_location_logger/Component_Displacement/proxima centuri"
                            ),
                            0.123
                            ),

         "Yellow Dwarf":    (
                            ("./logging_output/YDNR/sun_location_logger/Component_Displacement/sun",
                             "./logging_output/YDNG/sun_location_logger/Component_Displacement/sun",
                             "./logging_output/YDFR/sun_location_logger/Component_Displacement/sun",
                             "./logging_output/YDFG/sun_location_logger/Component_Displacement/sun"
                             ),
                             1
                             ),

         "White Dwarf":     (
                            ("./logging_output/WDNR/SiriusB_location_logger/Component_Displacement/SiriusB",
                             "./logging_output/WDNG/SiriusB_location_logger/Component_Displacement/SiriusB",
                             "./logging_output/WDFR/SiriusB_location_logger/Component_Displacement/SiriusB",
                             "./logging_output/WDFG/SiriusB_location_logger/Component_Displacement/SiriusB"
                             ),
                             1.04
                             ),

         "Neutron Star":    (
                            ("./logging_output/NSNR/PSR_location_logger/Component_Displacement/PSR B1257+12",
                             "./logging_output/NSNG/PSR_location_logger/Component_Displacement/PSR B1257+12",
                             "./logging_output/NSFR/PSR_location_logger/Component_Displacement/PSR B1257+12",
                             "./logging_output/NSFG/PSR_location_logger/Component_Displacement/PSR B1257+12"
                             ),
                             1.4
                             ),

         "Red Giant":       (
                            ("./logging_output/RGNR/Aldebaran_location_logger/Component_Displacement/Aldebaran",
                             "./logging_output/RGNG/Aldebaran_location_logger/Component_Displacement/Aldebaran",
                             "./logging_output/RGFR/Aldebaran_location_logger/Component_Displacement/Aldebaran",
                             "./logging_output/RGFG/Aldebaran_location_logger/Component_Displacement/Aldebaran"
                             ),
                             1.7
                             ),

         "Red Supergiant":  (
                            ("./logging_output/RSNR/betelgeuse_location_logger/Component_Displacement/betelgeuse",
                             "./logging_output/RSNG/betelgeuse_location_logger/Component_Displacement/betelgeuse",
                             "./logging_output/RSFR/betelgeuse_location_logger/Component_Displacement/betelgeuse",
                             "./logging_output/RSFG/betelgeuse_location_logger/Component_Displacement/betelgeuse"
                             ),
                             20
                             ),

         "Blue Supergiant": (
                            ("./logging_output/BSNR/Zeta_location_logger/Component_Displacement/Zeta",
                             "./logging_output/BSNG/Zeta_location_logger/Component_Displacement/Zeta",
         #                    "./logging_output/BSFR/Zeta_location_logger/Component_Displacement/Zeta",
         #                    "./logging_output/BSFG/Zeta_location_logger/Component_Displacement/Zeta"
                             ),
                             56.1
                             )
         }

star_wobbles = {}
for star_type in folders:
    print("--|| Loading files for {} ||--".format(star_type))
    print("--|| Progress: [{}] ||--".format(" " * len(folders[star_type][0])), end = "")
    print("\r--|| Progress: [", end = "")
    star_wobbles[star_type] = []
    for i, folder in enumerate(folders[star_type][0]):
        file = os.path.join(folder, [file for file in os.listdir(folder) if file.split(".")[1] == "csv"][0])
        data = np.genfromtxt(file, delimiter = ",", skip_header = 1)
        star_wobbles[star_type].append(np.max(data, axis=0)[1] - np.min(data, axis=0)[1])
        print("=", end = "")
    print("\n--|| Done ||--")
    print()


for i, typeOfOrbit in enumerate(("Near Rocky", "Near Gaseous", "Distant Rocky", "Distant Gaseous")):
    masses = []
    wobbleMagnitudes = []
    for star_type in star_wobbles:
        if i < len(star_wobbles[star_type]):
            masses.append(folders[star_type][1])
            wobbleMagnitudes.append(star_wobbles[star_type][i])

    print("--|| {} Raw Results ||--".format(typeOfOrbit))
    for j in range(len(masses)):
        print("    {} Solar Masses => {} m".format(masses[i], wobbleMagnitudes[i]))
    print("--|| Done ||--")
    print()

    print("--|| Graphing Results for {} ||--".format(typeOfOrbit))
    plt.xscale('log')
    plt.plot(masses, wobbleMagnitudes)
    plt.title("{} Stellar Wobble against Stellar Mass".format(typeOfOrbit))
    plt.xlabel("Star Mass (Solar Masses)")
    plt.ylabel("Stellar Wobble Diameter (m)")
    plt.savefig("{} Stellar Wobble against Stellar Mass.png".format(typeOfOrbit))
    plt.show()
    print("--|| Done ||--")
    print()