###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Auxiliary Tools. Contains:                                               ##
##  - function to calculate distance between two points                      ##
##  - functions to distribute nodes (generate their 3d positions)            ##
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

def generate_full_binary_tree_network(numLvls, maxRange, ipos=(0,0)):
    def add_next(nodes, isParentOf, basePos, lvlsRemaining, maxRange):
        pid = len(nodes) - 1
        # up child
        ua = random.random() * (pi/2)
        ud = random.random() * maxRange
        ux = basePos[0] + ud * cos(ua)
        uy = basePos[1] + ud * sin(ua)
        nodes.append((ux, uy))                 # adding node to list
        isParentOf.append([])                  # list for the sons
        isParentOf[pid].append(len(nodes) -1)  # adding topology reference to it
        if lvlsRemaining != 1:
            add_next(nodes, isParentOf, (ux, uy), lvlsRemaining - 1, maxRange)
        # down child
        da = random.random() * (pi/2) * (-1)
        dd = random.random() * maxRange
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
            topo.append( (i, j) )
    return nodes, topo