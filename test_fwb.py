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
    data     = json.load(inFile)
    nodes    = data["network"][0]["nodes"]
    topology = data["network"][0]["topology"]
    
    numNodes = len(nodes)

    sim = Simulator()
    for nid in range(len(nodes)):
        sim.add_node(TelosB(nid, nodes[nid][0], nodes[nid][1], float("inf"), 
                            nid == sinkid))
    sim.set_network_topology(topology)
    sim.set_channel_info(alpha, noise)
    sim.set_available_bws(bws)
    sim.set_slot_size(ssize)
    sim.set_data_collection_start(0)

    fwbScheduler = FWB()
    fwbScheduler.set_number_of_nodes(numNodes)
    fwbScheduler.set_network_topology(topology)
    fwbScheduler.set_sink_id(sinkid)
    fwbScheduler.set_available_bandwidths(bws)

    sim.set_scheduler(fwbScheduler)

    sim.run(frames)

    print("{} txs ".format(sim.get_num_txs()), end= ": ")
    print("{} V ".format(sim.get_num_rxs_successes()), end= " ")
    print("{} X ".format(sim.get_num_rxs_failures()))
    print("+ {} ongoing txs".format(sim.get_ongoing_txs()))
    for node in sim.nodes:
        print("node {}: rcvd {}, sent {} msgs".format(node.id, 
                                                    node.recvdMsgsCounter, 
                                                    node.sentMsgsCounter))
    avgLatency = sum(sim.nodes[0].latencies) / len(sim.nodes[0].latencies)
    errLatency = 1.96 * avgLatency / math.sqrt(len(sim.nodes[0].latencies))
    print("Latency: {} +- {}".format(avgLatency, errLatency))