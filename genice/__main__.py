#!/usr/bin/env python3
# -*- python -*-

import os
import sys
import argparse  as ap
import logging
from genice.importer import safe_import
from genice import lattice
import random
import numpy as np

def getoptions():
    parser = ap.ArgumentParser(description='')
    parser.add_argument('--rep',  '-r', nargs = 3, type=int,   dest='rep',  default=[2,2,2],
                        help='Repeat the unit cell in x,y, and z directions. [2,2,2]')
    parser.add_argument('--dens', '-d', nargs = 1, type=float, dest='dens', default=(-1,),
                        help='Specify the ice density in g/cm3')
    parser.add_argument('--seed', '-s', nargs = 1, type=int,   dest='seed', default=(1000,),
                        help='Random seed [1000]')
    parser.add_argument('--format', '-f', nargs = 1,           dest='format', default=("gromacs",), metavar="gmeqdypoc",
                        help='Specify file format [g(romacs)|m(dview)|e(uler)|q(uaternion)|d(igraph)|y(aplot)|p(ython module)|o(penScad)|c(entersofmass)|r(elative com)]')
    parser.add_argument('--water', '-w', nargs = 1,           dest='water', default=("tip3p",), metavar="model",
                        help='Specify water model. (tip3p, tip4p, etc.)')
    parser.add_argument('--guest', '-g', nargs = 1,           dest='guests', metavar="D=empty", action="append", 
                        help='Specify guest(s) in the cage type. (D=empty, T=co2*0.5+me*0.3, etc.)')
    parser.add_argument('--Guest', '-G', nargs = 1,           dest='spot_guests', metavar="13=me", action="append", 
                        help='Specify guest in the specific cage. (13=me, 32=co2, etc.)')
    parser.add_argument('--Group', '-H', nargs = 1,           dest='groups', metavar="13=bu-:0", action="append", 
                        help='Specify the group. (-H 13=bu-:0, etc.)')
    parser.add_argument('--anion', '-a', nargs = 1,           dest='anions', metavar="3=Cl", action="append", 
                        help='Specify a monatomic anion that replaces a water molecule. (3=Cl, 39=F, etc.)')
    parser.add_argument('--cation', '-c', nargs = 1,           dest='cations', metavar="3=Na", action="append", 
                        help='Specify a monatomic cation that replaces a water molecule. (3=Na, 39=NH4, etc.)')
    parser.add_argument('--nodep', action='store_true', dest='nodep',
                        help='No depolarization.')
    parser.add_argument('--debug', '-D', action='store_true', dest='debug',
                        help='Output debugging info.')
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet',
                        help='Do not output progress messages.')
    parser.add_argument('Type', nargs=1,
                       help='Crystal type (1c,1h,etc. See https://github.com/vitroid/GenIce for available ice structures.)')
    return parser.parse_args()


        

def main():
    #prepare user's workarea
    home = os.path.expanduser("~")
    if os.path.exists(home+"/Library/Application Support"): #MacOS
        homegenice = home+"/Library/Application Support/GenIce"
    else:
        homegenice = os.path.expanduser(home + "/.genice") #Other unix
    sys.path.append(homegenice)
    try:
        os.makedirs(homegenice+"/formats")
        os.makedirs(homegenice+"/lattices")
        os.makedirs(homegenice+"/molecules")
    except:
        pass #just ignore when failed.


    #Parse options
    options = getoptions()

    
    #Set verbosity level
    if options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")
    elif options.quiet:
        logging.basicConfig(level=logging.WARN,
                            format="%(levelname)s %(message)s")
    else:
        #normal
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s %(message)s")
    logger = logging.getLogger()
    logger.debug("Debug mode.")
    logger.debug(options.Type)

    water_type   = options.water[0]
    guests       = options.guests
    lattice_type = options.Type[0]
    file_format  = options.format[0]
    seed         = options.seed[0]
    rep          = options.rep
    density      = options.dens[0]
    depolarize   = not options.nodep
    anions = dict()
    if options.anions is not None:
        logger.info(options.anions)
        for v in options.anions:
            key, value = v[0].split("=")
            anions[int(key)] = value
    cations = dict()
    if options.cations is not None:
        for v in options.cations:
            key, value = v[0].split("=")
            cations[int(key)] = value
    spot_guests = dict()
    if options.spot_guests is not None:
        for v in options.spot_guests:
            key, value = v[0].split("=")
            spot_guests[int(key)] = value
    groups = dict()
    if options.groups is not None:
        for v in options.groups:
            key, value = v[0].split("=")
            groups[int(key)] = value

    del options  # Dispose for safety.
    # Set random seeds
    random.seed(seed)
    np.random.seed(seed)
    
    logger.debug("Lattice: {0}".format(lattice_type))
    # Main part of the program is contained in th Formatter object. (See formats/)
    logger.debug("Format: {0}".format(file_format))
    formatter = safe_import("format", file_format)
    lat = lattice.Lattice(lattice_type,
                          density=density,
                          rep=rep,
                          depolarize=depolarize,
                          cations=cations,
                          anions=anions,
                          spot_guests=spot_guests,
                          spot_groups=groups,
                          )
    # These arguments should also be in lattice, not in run()
    lat.format(water_type=water_type,
                guests=guests,
                formatter=formatter
                )
    
if __name__ == "__main__":
    main()
