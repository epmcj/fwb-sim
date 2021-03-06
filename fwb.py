###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  FWB scheduler algorithm implementation.                                  ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
import random
import math
from scheduler import Scheduler

class FWB(Scheduler):
    def __init__(self):
        self.numNodes  = 0
        self.sinkid    = None
        self.numDsc    = [] # number of descendants
        self.parentOf  = []
        self.childOf   = []
        self.bws       = []
        self.schedSize = 0
        self.nodeSlots = None
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

    def set_network_topology(self, relations):
        # relations must be a (parent, child) tuple list for each node in the 
        # network
        self.parentOf = [ [] for i in range(self.numNodes) ]
        self.childOf  = [ [] for i in range(self.numNodes) ]
        for parent, child in relations:
            self.parentOf[parent].append(child)
            self.childOf[child].append(parent)
        # removing duplicates
        for i in range(self.numNodes):
            self.parentOf[i] = list(set(self.parentOf[i]))
            self.childOf[i]  = list(set(self.childOf[i]))

    def __calculate_descendants(self):
        assert (self.sinkid is not None), "Missing sink Node" 
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

    # uses bfs to generate the order
    def __get_node_exploration_order(self, startNode):
        nids   = [startNode]
        goNext = [startNode]
        marked = [False] * self.numNodes
        marked[startNode] = True
        while len(goNext) != 0:
            node = goNext.pop(0)
            for child in self.parentOf[node]:
                if not marked[child]:
                    nids.append(child)
                    goNext.append(child)
                    marked[child] = True
            for parent in self.childOf[node]:
                if not marked[parent]:
                    nids.append(parent)
                    goNext.append(parent)
                    marked[parent] = True
        # removing sink node (it does not need timeslots)
        nids.remove(self.sinkid)
        return nids

    def get_neighbors_slots(self, nid):
        # finding the slots used by its parents, siblings and children
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
        

    # Returns (schedule of timeslots, scheduling size, schedule of bandwidths)
    def schedule(self):
        assert (self.numNodes != 0), "No node to schedule"
        assert (len(self.bws) != 0), "No bandwidth available"

        self.factors   = [x / min(self.bws) for x in self.bws]
        self.schedSize = 0
        self.nodeSlots = [[] for x in range(self.numNodes)]
        self.nodeBw    = [ min(self.bws) ] * self.numNodes
        self.__calculate_descendants()
        capacity = max(self.bws) / min(self.bws)

        # nids = [x for x in range(1, self.numNodes)]
        # random.shuffle(nids)
        startNode = random.randint(0, self.numNodes - 1)
        nids = self.__get_node_exploration_order(startNode)
        # print(nids) #TODO: DELETE
        while len(nids) != 0:
            nid = nids.pop(0)
            # print("Node {}".format(nid)) #TODO: DELETE
            workload = self.numDsc[nid] + 1
            # print("\tWorkload {}".format(workload)) #TODO: DELETE
            if workload >= capacity:
                self.nodeBw[nid] = self.bws[-1]
                factor = self.factors[-1]
            else:
                i = 0
                while self.factors[i] < workload:
                    i += 1
                self.nodeBw[nid] = self.bws[i]
                factor = self.factors[i]
            # print("\tFactor {}".format(factor)) #TODO: DELETE
            # finding the number of slots required for the node transmissions
            nTs = math.ceil(workload / factor)
            # print("\nTs {}".format(nTs)) #TODO: DELETE
            neighborsSlots = self.get_neighbors_slots(nid)            
            # print(neighborsSlots) #TODO: DELETE
            # picking the slots
            i = 1
            while len(self.nodeSlots[nid]) != nTs:
                if i not in neighborsSlots:
                    self.nodeSlots[nid].append(i)
                    if i > self.schedSize:
                        # updating the schedule size
                        self.schedSize = i
                i += 1



