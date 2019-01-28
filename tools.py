###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Auxiliary Tools. Contains:                                               ##
##  - function to calculate distance between two points                      ##
##  - functions to distribute nodes (generate their positions)               ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################

import operator
import random
from radios import Radio
from math   import floor, sqrt, pi, sin, cos

INFINITY = float("inf")

# Calculates euclidean distance between two points
def distance(a, b):
    c = list(map(operator.sub, a, b))
    c = map(lambda x: x ** 2, c)
    return sqrt(sum(c))

# Estimate the energy and the time required for a transmission to happen.
def estimate_transmission(msg, radio):
    assert issubclass(type(radio), Radio)
    time   = len(msg) / radio.txRate
    energy = time * radio.txPowerConsumption
    return time, energy
    
# Generate a list for each node containing possible interferences (based on 
# protocol model).
def get_possible_interference_info(nodes, interferenceRange):
    canInterWith = [ [] for x in range(len(nodes)) ]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                if distance(nodes[i], nodes[j]) <= interferenceRange:
                    canInterWith[i].append(j)
    return canInterWith

def generate_full_binary_tree_network(numLvls, maxRange, minRange=0, ipos=(0,0)):
    def add_next(nodes, isParentOf, basePos, lvlsRemaining, maxRange):
        pid = len(nodes) - 1
        maxDistance = maxRange - minRange
        # up child
        ua = random.random() * (pi/2)
        ud = minRange + random.random() * maxDistance
        ux = basePos[0] + ud * cos(ua)
        uy = basePos[1] + ud * sin(ua)
        nodes.append((ux, uy))                 # adding node to list
        isParentOf.append([])                  # list for the sons
        isParentOf[pid].append(len(nodes) -1)  # adding topology reference to it
        if lvlsRemaining != 1:
            add_next(nodes, isParentOf, (ux, uy), lvlsRemaining - 1, maxRange)
        # down child
        da = random.random() * (pi/2) * (-1)
        dd = minRange + random.random() * maxDistance
        dx = basePos[0] + dd * cos(da)
        dy = basePos[1] + dd * sin(da)
        nodes.append((dx, dy))                 # adding node to list
        isParentOf.append([])                  # list for the sons
        isParentOf[pid].append(len(nodes) -1)  # adding topology reference to it
        if lvlsRemaining != 1:
            add_next(nodes, isParentOf, (dx, dy), lvlsRemaining - 1, maxRange)

    nodes       = []
    isParentOf  = []
    # adding initial node 
    nodes.append(ipos)
    isParentOf.append([])
    add_next(nodes, isParentOf, ipos, numLvls - 1, maxRange)
    topo = []
    for i in range(len(isParentOf)):
        for j in isParentOf[i]:
            topo.append((i, j))
    return nodes, topo

# generate a network where the sink is connected to the root of a full binary 
# tree network.
#       S ----- (FBT)
def generate_unbalanced_binary_tree_network(numLvls, maxRange, minRange=0, 
                                            ipos=(0,0)):
    # adding initial node
    maxDistance = maxRange - minRange
    na = (pi/2) + (random.random() * pi)
    nd = minRange + random.random() * maxDistance
    nx = 0 + nd * cos(na)
    ny = 0 + nd * sin(na)
    #
    nodes, topo = generate_full_binary_tree_network(numLvls, maxRange, minRange, 
                                                    ipos)
    # adding the first node and updating the network topology
    nodes.insert(0, (nx, ny))
    ntopo = []
    ntopo.append((0,1))
    # updating indexes
    for relation in topo:
        ntopo.append((relation[0] + 1, relation[1] + 1))
    return nodes, ntopo


def generate_random_tree_network(numNodes, maxRange, maxChildren, minRange=0, 
                                 minChildren=1, ipos=(0,0)):
    nodes = []
    topo  = []
    nexts = []
    maxDistance = maxRange - minRange
    # first node
    nodes.append(ipos)
    nid = 0
    nexts.append(nid)
    while len(nodes) < numNodes:
        parent = nexts.pop(0)
        numChild = random.randint(minChildren, maxChildren)
        # limitating the number of children by the remaining number of nodes
        numChild = min(numChild, (numNodes - len(nodes)))
        # generating children positions
        for i in range(numChild):
            na = (-pi/2) + (random.random() * pi)  # from -90 to 90 degrees
            nd = minRange + random.random() * maxDistance
            nx = nodes[parent][0] + nd * cos(na)
            ny = nodes[parent][1] + nd * sin(na)
            nodes.append((nx, ny))
            cid = len(nodes) - 1
            topo.append((parent, cid))
            nexts.append(cid)
    return nodes, topo

