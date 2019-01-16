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

def distance(a, b):
    c = list(map(operator.sub, a, b))
    c = map(lambda x: x ** 2, c)
    return sqrt(sum(c))

def estimate_transmission(msg, radio):
    # Estimate the energy and the time required for a transmission to happen.
    assert issubclass(type(radio), Radio)
    time   = len(msg) / radio.txRate
    energy = time * radio.txPowerConsumption
    return time, energy