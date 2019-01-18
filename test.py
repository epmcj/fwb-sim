import simulator
from node import Node
from telosb import TelosB
from random import randint

nodes = [(-40,3),
         (1,1),
         (2,0),
         (2,2),
         (1,5),
         (2,4),
         (2,6)]

topology = [(0,1),
            (0,4),
            (1,2),
            (1,3),
            (4,5),
            (4,6)]

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

sim.run(2)

print("{} txs ".format(sim.get_num_txs()), end= ": ")
print("{} V ".format(sim.get_num_rxs_successes()), end= " ")
print("{} X ".format(sim.get_num_rxs_failures()))

for node in sim.nodes:
    print("node {}: rcvd {}, sent {} msgs".format(node.id, 
                                                  node.recvdMsgsCounter, 
                                                  node.sentMsgsCounter))