import simulator
import math
from radios import CC2420Radio
from fwb    import FWB
from telosb import TelosB
from random import randint
from tools  import generate_full_binary_tree_network

# nodes = [(-40,3),
#          (1,1),
#          (2,0),
#          (2,2),
#          (1,5),
#          (2,4),
#          (2,6)]

# topology = [(0,1),
#             (0,4),
#             (1,2),
#             (1,3),
#             (4,5),
#             (4,6)]

nodes, topology = generate_full_binary_tree_network(3, CC2420Radio.txRange/2)

sinkid = 0

print("{} nodes".format(len(nodes)))
bandwidths = [2, 4]

slotSize = 0.1 # 100 ms

alpha = 3
noise = 0

sim = simulator.Simulator(verbose=True)
for nid in range(len(nodes)):
    sim.add_node(TelosB(nid, nodes[nid][0], nodes[nid][1], float("inf"), 
                        nid == 0))

sim.set_network_topology(topology)

sim.set_channel_info(alpha, noise)

sim.set_available_bws(bandwidths)

sim.set_slot_size(slotSize)

sim.set_data_collection(0, 0)

scheduler = FWB()
scheduler.set_number_of_nodes(len(nodes))
scheduler.set_network_topology(topology)
scheduler.set_sink_id(sinkid)
scheduler.set_available_bandwidths(bandwidths)

sim.set_scheduler(scheduler)

sim.run(20)

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