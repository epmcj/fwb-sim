###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  FWBI (FWB + interference) scheduler algorithm implementation.            ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
import random
import math
from fwb import FWB

class FWBI(FWB):
    def __init__(self):
        super(FWBI, self).__init__()
        self.interRange     = None
        self.canInterWith   = None

    # set information about which nodes a node can interfere with if they 
    # transmit together
    def set_interference_info(self, canInterWith):
        assert (len(canInterWith) == self.numNodes), "Missing interference " + \
                                                "information about some nodes"
        self.canInterWith = canInterWith

    def get_neighbors_slots(self, nid):
        assert (self.canInterWith != None), "Missing interference information"
        neighborsSlots = super(FWBI, self).get_neighbors_slots(nid)
        # adding slots to avoid possible interference
        if self.canInterWith[nid] is not None:
            for node in self.canInterWith[nid]:
                # parent slots
                for slotNum in self.nodeSlots[node]:
                    neighborsSlots.append(slotNum)
        return list(set(neighborsSlots)) # removing duplicates