###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  [...]                                                                    ##
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
        self.nodesPositions = []
        self.canInterWith   = []

    def set_interference_range(self, interRange):
        assert (interRange >= 0), "interference range must be >= 0"
        self.interRange = interRange

    def get_neighbors_slots(self, nid):
        # finding the slots used by its parents, siblings, children and nodes 
        # that can interfere with it.
        neighborsSlots = []
        if self.childOf[nid] is not None:
            for parent in self.childOf[nid]:
                # parent slots
                for slotNum in self.nodeSlots[parent]:
                    neighborsSlots.append(slotNum)
                # siblings slots
                for sibling in self.parentOf[parent]:
                    for slotNum in self.nodeSlots[sibling]:
                        neighborsSlots.append(slotNum)
        if self.parentOf[nid] is not None:
            for child in self.parentOf[nid]:
                for slotNum in self.nodeSlots[child]:
                    neighborsSlots.append(slotNum)
        return list(set(neighborsSlots)) # removing duplicates