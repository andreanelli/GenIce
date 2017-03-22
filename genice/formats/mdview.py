from genice.formats.baseclass import GenIce


class Formatter(GenIce):
    """
    Gro file format
    defined in http://manual.gromacs.org/current/online/gro.html
    """
    def run(self, options):
        water_type    = options.water[0]
        guests        = options.guests
        self.stage1()   #replicate the unit cell
        self.stage2()   #prepare random graph
        self.stage3()   #Make an ice graph
        self.stage4()   #Depolarize
        self.stage5()   #Orientation
        self.stage6(water_type)  #Water atoms
        self.stage7(guests)      #Guest atoms
        self.logger.info("Total number of atoms: {0}".format(len(self.atoms)))
        self.logger.info("Output in MDView format.")
        s = ""
        #if celltype == "rect":
        #    s += "-length '({0}, {1}, {2})'\n".format(cell[0,0]*10,cell[1,1]*10,cell[2,2]*10)
        s += "-center 0 0 0\n"
        s += "-fold\n"
        s += "{0}\n".format(len(self.atoms))
        for i in range(len(self.atoms)):
            molorder, resname, atomname, position = self.atoms[i]
        s += "{0:5} {1:9.4f} {2:9.4f} {3:9.4f}\n".format(atomname,position[0]*10,position[1]*10,position[2]*10)
        print(s,end="")
