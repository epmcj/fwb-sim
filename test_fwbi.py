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
alpha   = None
ssize   = None 
frames  = None
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
    elif sys.argv[i] == "-a":
        alpha = float(sys.argv[i+1])
    elif sys.argv[i] == "-s":
        ssize = float(sys.argv[i+1]) / 1000 # from ms to s
    elif sys.argv[i] == "-f":
        frames = int(sys.argv[i+1])
    elif sys.argv[i] == "-coi":
        coi = float(sys.argv[i+1])

# parameter checking
if inName is None:
    print("Missing input file (-i [FILE])")
    exit(1)
# if outName is None:
#     print("Missing output file (-o [FILE])")
#     exit(1)
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
        print(nodes)
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
        # distributing bandwidths (simulating different bandwidths using 
        # different radio speeds)
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
        # print("{} txs ".format(sim.get_num_txs()), end= ": ")
        # print("{} S,".format(sim.get_num_rxs_successes()), end= " ")
        # print("{} F".format(sim.get_num_rxs_failures()), end= " ")
        # print("+ {} ongoing txs".format(sim.get_ongoing_txs()))
        # for node in sim.nodes:
        #     print("node {}: rcvd {}, sent {}, has {} msgs".format(node.id, 
        #                                                 node.recvdMsgsCounter, 
        #                                                 node.sentMsgsCounter,
        #                                                 node.get_outbox_len()))
        avgLatency = sum(sim.nodes[sinkid].latencies) / \
                        len(sim.nodes[sinkid].latencies)
        errLatency = 1.96 * avgLatency / sqrt(len(sim.nodes[sinkid].latencies))
        print("Latency: {} +- {}".format(avgLatency, errLatency))
        print("Data Collected: {}".format(sim.nodes[sinkid].recvdMsgsCounter))
        
        odata["results"].append({
            "num_slots"         : frameSize,
            "avg_latency"       : avgLatency,
            "err_latency"       : errLatency,
            "txs"               : sim.get_num_txs(),
            "txs_success"       : sim.get_num_rxs_successes(),
            "txs_failures"      : sim.get_num_rxs_failures(),
            "sink_collections"  : sim.nodes[sinkid].recvdMsgsCounter
        })

if outName != None:
    with open(outName, "w") as outFile:
        json.dump(odata, outFile)
    