###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Generates a random tree.                                                 ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
import tools
import sys
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

numNet      = 1
minRange    = 2
minChildren = 1
nrange      = None
outName     = None
numNodes    = None
maxChildren = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-c":
        maxChildren = int(sys.argv[i+1])
    if sys.argv[i] == "-mc":
        minChildren = int(sys.argv[i+1])
    elif sys.argv[i] == "-d":
        nrange = float(sys.argv[i+1])
    elif sys.argv[i] == "-md":
        minRange = float(sys.argv[i+1])
    elif sys.argv[i] == "-o":
        outName = sys.argv[i+1]
    elif sys.argv[i] == "-t":
        numNet = int(sys.argv[i+1])
    elif sys.argv[i] == "-n":
        numNodes = int(sys.argv[i+1])

if numNodes is None:
    print("Missing number of nodes (-n [NUMBER])")
    exit(1)
if maxChildren is None:
    print("Missing number max children (-c [NUMBER])")
    exit(1)
if nrange is None:
    print("Missing nodes max distance (-d [DISTANCE])")
    exit(1)
if outName is None:
    print("Missing output file (-o [FILE])")
    exit(1)

data = {}
data["network"] = []

for i in range(numNet):
    nodes, topo = tools.generate_random_tree_network(numNodes, nrange, 
                                                     maxChildren, minRange, 
                                                     minChildren)
    data["network"].append({
        "nodes"    : nodes,
        "topology" : topo
    })

with open(outName, "w") as outFile:
    json.dump(data, outFile)