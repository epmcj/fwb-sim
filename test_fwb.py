###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Tests the FWB implementation.                                            ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
import sys
import math
import json
from simulator  import Simulator
from radios     import CC2420Radio
from telosb     import TelosB
from tools      import get_possible_interference_info
from fwb        import FWB

sinkid  = 0
# noise   = 0
inName  = None
outName = None
alpha   = None
ssize   = None 
frames  = None
bws     = []

# parameter reading
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-i":
        inName = sys.argv[i+1]
    elif sys.argv[i] == "-o":
        outName = sys.argv[i+1]
    elif sys.argv[i] == "-bw":
        bws = [int(bw) for bw in sys.argv[i+1].split(",")]
    elif sys.argv[i] == "-a":
        alpha = float(sys.argv[i+1])
    elif sys.argv[i] == "-s":
        ssize = float(sys.argv[i+1]) / 1000 # from ms to s
    elif sys.argv[i] == "-f":
        frames = int(sys.argv[i+1])

# parameter checking
if inName is None:
    print("Missing input file (-i [FILE])")
    exit(1)
if outName is None:
    print("Missing output file (-o [FILE])")
    exit(1)
if alpha is None:
    print("Missing channel alpha (-a [VALUE])")
    exit(1)
if len(bws) == 0:
    print("Missing bandwidths (-bw [VALUE1,VALUE2,..])")
    exit(1)
if ssize is None:
    print("Missing timeslot size (-s [VALUE] in ms)")
    exit(1)
if frames is None:
    print("Missing number of frames to execute (-f [VALUE])")
    exit(1)

# based on "Local Broadcasting in the Physical Interference Model"
noise = CC2420Radio.maxTxPower / (2 * CC2420Radio.minSIR * 
                                    (2 * CC2420Radio.txRange)**alpha)

# executing
with open(inName) as inFile:
    # reading node positions and network topology from the input file
    data     = json.load(inFile)
    nodes    = data["network"][0]["nodes"]
    topology = data["network"][0]["topology"]
    # creating node references
    numNodes = len(nodes)
    nodesRef = []
    for nid in range(len(nodes)):
        nodesRef.append(TelosB(nid, nodes[nid][0], nodes[nid][1], float("inf"), 
                        nid == sinkid))
    # doing schedule for the simulation
    fwbScheduler = FWB()
    fwbScheduler.set_number_of_nodes(numNodes)
    fwbScheduler.set_network_topology(topology)
    fwbScheduler.set_sink_id(sinkid)
    fwbScheduler.set_available_bandwidths(bws)
    fwbScheduler.schedule()
    # getting schedule results
    nodeBW    = fwbScheduler.get_bandwidth_schedule()
    tschedule = fwbScheduler.get_slot_schedule()
    frameSize = fwbScheduler.get_slot_schedule_size()
    print("ft (sch): {}".format(frameSize))
    # distributing bandwidths (simulating different bandwidths using different
    # radio speeds)
    minBw = min(bws)
    for i in range(len(nodeBW)):
        speedUpFactor = nodeBW[i] / minBw
        nodesRef[i].radio.set_tx_rate(speedUpFactor * CC2420Radio.txRate)
    # creating simulator
    sim = Simulator()
    sim.add_nodes(nodesRef)
    sim.set_network_topology(topology)
    sim.set_channel_info(alpha, noise)
    sim.set_slot_size(ssize)
    sim.set_data_collection(0, frameSize * ssize)
    sim.set_timeslot_schedule(tschedule)
    # running simulator
    sim.run(frames)
    # printing results
    print("{} txs ".format(sim.get_num_txs()), end= ": ")
    print("{} S,".format(sim.get_num_rxs_successes()), end= " ")
    print("{} F".format(sim.get_num_rxs_failures()), end= " ")
    print("+ {} ongoing txs".format(sim.get_ongoing_txs()))
    # for node in sim.nodes:
    #     print("node {}: rcvd {}, sent {}, has {} msgs".format(node.id, 
    #                                                 node.recvdMsgsCounter, 
    #                                                 node.sentMsgsCounter,
    #                                                 node.get_outbox_len()))
    avgLatency = sum(sim.nodes[sinkid].latencies) / \
                    len(sim.nodes[sinkid].latencies)
    errLatency = 1.96 * avgLatency / math.sqrt(len(sim.nodes[sinkid].latencies))
    print("Latency: {} +- {}".format(avgLatency, errLatency))
    print("Data Collected: {}".format(sim.nodes[sinkid].recvdMsgsCounter))