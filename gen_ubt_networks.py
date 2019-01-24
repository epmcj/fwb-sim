import tools
import sys
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

numNet   = 1
minRange = 2
nrange   = None
nlevels  = None
outName  = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-l":
        nlevels = int(sys.argv[i+1])
    elif sys.argv[i] == "-d":
        nrange = float(sys.argv[i+1])
    elif sys.argv[i] == "-m":
        minRange = float(sys.argv[i+1])
    elif sys.argv[i] == "-o":
        outName = sys.argv[i+1]
    elif sys.argv[i] == "-t":
        numNet = int(sys.argv[i+1])

if nlevels is None:
    print("Missing number of levels (-l [NUMBER])")
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
    nodes, topo = tools.generate_unbalanced_binary_tree_network(nlevels, nrange,
                                                                minRange)
    data["network"].append({
        "nodes"    : nodes,
        "topology" : topo
    })

with open(outName, "w") as outFile:
    json.dump(data, outFile)