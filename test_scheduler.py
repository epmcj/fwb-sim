###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Tests the scheduler implementations.                                     ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################

import sys
import json
from simulator  import Simulator
from radios     import CC2420Radio
from telosb     import TelosB
from tools      import get_possible_interference_info
from fwbi       import FWBI
from math       import sqrt

sinkid  = 0
# noise   = 0
inName  = None
outName = None
bws     = []
coi     = 1         # coefficient of interference

# parameter reading
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-i":
        inName = sys.argv[i+1]
    elif sys.argv[i] == "-o":
        outName = sys.argv[i+1]
    elif sys.argv[i] == "-bw":
        bws = [int(bw) for bw in sys.argv[i+1].split(",")]
    elif sys.argv[i] == "-coi":
        coi = float(sys.argv[i+1])

# parameter checking
if inName is None:
    print("Missing input file (-i [FILE])")
    exit(1)
# if outName is None:
#     print("Missing output file (-o [FILE])")
#     exit(1)
if len(bws) == 0:
    print("Missing bandwidths (-bw [VALUE1,VALUE2,..])")
    exit(1)


odata = {}
odata["results"] = []

# executing
with open(inName, "r") as inFile:
    # reading node positions and network topology from the input file
    idata = json.load(inFile)
    for i in range(len(idata["network"])):
        print("Executing Network {}".format(i + 1))
        nodes    = idata["network"][0]["nodes"]
        topology = idata["network"][0]["topology"]
        # creating node references
        numNodes = len(nodes)
        nodesRef = []
        for nid in range(len(nodes)):
            nodesRef.append(TelosB(nid, nodes[nid][0], nodes[nid][1], 
                            float("inf"), nid == sinkid))
        # getting possible interference information (for the scheduler)
        canInterWith = get_possible_interference_info(nodes, 
                                                      CC2420Radio.txRange * coi)
        # doing schedule for the simulation
        fwbiScheduler = FWBI()
        fwbiScheduler.set_number_of_nodes(numNodes)
        fwbiScheduler.set_network_topology(topology)
        fwbiScheduler.set_interference_info(canInterWith)
        fwbiScheduler.set_sink_id(sinkid)
        fwbiScheduler.set_available_bandwidths(bws)
        fwbiScheduler.schedule()
        # getting schedule results
        nodeBW    = fwbiScheduler.get_bandwidth_schedule()
        tschedule = fwbiScheduler.get_slot_schedule()
        frameSize = fwbiScheduler.get_slot_schedule_size()
        
        odata["results"].append({
            "num_slots" : frameSize
        })

if outName != None:
    with open(outName, "w") as outFile:
        json.dump(odata, outFile)
    