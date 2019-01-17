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

class FWB:
    def __init__(self):
        self.numNodes  = 0
        self.sinkid    = None
        self.numDsc    = [] # number of descendants
        self.parentOf  = []
        self.childOf   = []
        self.bws       = []
        self.schedSize = 0
        # self.capacity  = None
        self.nodeSlots  = None
        self.nodeBw    = None

    def set_number_of_nodes(self, numNodes):
        assert (numNodes > 0), "Number of nodes must be greater than zero"
        self.numNodes = numNodes

    def set_sink_id(self, sinkid):
        self.sinkid = sinkid

    def set_available_bandwidths(self, bws):
        self.bws = bws
        self.bws.sort()

    def get_slot_schedule(self):
        return self.nodeSlots

    def get_slot_schedule_size(self):
        return self.schedSize

    def get_bandwidth_schedule(self):
        return self.nodeBw

    # The parameter parentOf must be a list of lists with length equals to the 
    # number of nodes
    def set_parent_info(self, parentOf):
        assert (len(parentOf) == self.numNodes), "Missing information about" + \
                                                 " some nodes"
        self.parentOf = parentOf
        # generating "child of" information to help in the schedule
        self.childOf = [[]] * self.numNodes
        for i in range(len(self.parentOf)):
            for child in self.parentOf[i]:
                self.childOf[child].append(i)

    def __calculate_descendants(self):
        # Algorithm 1 like
        self.numDsc = [None] * self.numNodes
        self.__calculate_node_descendants(self.sinkid)

    def __calculate_node_descendants(self, node):
        numDsc = len(self.parentOf[node])
        for child in self.parentOf[node]:
            if self.numDsc[child] is None:
                self.__calculate_node_descendants(child)
            numDsc += self.numDsc[child]
        self.numDsc[node] = numDsc
        return numDsc        

    # Returns (schedule of timeslots, scheduling size, schedule of bandwidths)
    def schedule(self):
        assert (self.numNodes != 0), "No node to schedule"
        assert (len(self.bws) != 0), "No bandwidth available"

        self.factors = [x / min(self.bws) for x in self.bws]
        self.schedSize = 0
        self.nodeSlots = [[]] * self.numNodes
        self.nodeBw    = [None] * self.numNodes
        self.__calculate_descendants()
        capacity = max(self.bws) / min(self.bws)

        nids = [x for x in range(1, self.numNodes)]
        random.shuffle(nids)
        while len(nids) != 0:
            nid = nids.pop()
            print("Node {}".format(nid))
            workload = self.numDsc[nid] + 1
            if workload >= capacity:
                self.nodeBw[nid] = self.bws[-1]
                factor = self.factors[-1]
            else:
                i = 0
                while self.factors[i] < workload:
                    i += 1
                self.nodeBw[nid] = self.bws[i]
                factor = self.factors[i]
            # finding the number of slots required for the node transmissions
            nTs = math.ceil(workload / factor)
            # finding the slots used by its neighbors
            neighborsSlots = []
            if self.childOf[nid] is not None:
                for parent in self.childOf[nid]:
                    for slotNum in self.nodeSlots[parent]:
                        neighborsSlots.append(slotNum)
            if self.parentOf[nid] is not None:
                for child in self.parentOf[nid]:
                    for slotNum in self.nodeSlots[child]:
                        neighborsSlots.append(slotNum)
            neighborsSlots = list(set(neighborsSlots)) # removing duplicates
            print(neighborsSlots)
            # picking the slots
            i = 0
            print(nTs)
            while len(self.nodeSlots[nid]) != nTs:
                if not (i in neighborsSlots):
                    self.nodeSlots[nid].append(i)
                    if i > self.schedSize:
                        # updating the schedule size
                        self.schedSize = i
                i += 1



