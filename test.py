import simulator
from node import Node

nodes = [(0,3),
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

sim = simulator.Simulator(verbose=True)
for addr in range(len(nodes)):
    sim.add_node(Node(addr, nodes[addr][0], nodes[addr][1], float("inf")))

sim.set_network_topology(topology)