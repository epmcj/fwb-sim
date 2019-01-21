import fwbi
from tools import get_possible_interference_info
from radios import CC2420Radio

numNodes = 7

nodes = [
    (0, 0), 
    (3.64352845036025, 1.7690077527624617), 
    (28.510529398514997, 16.299784000720564), 
    (10.440710028084133, -17.540830369273294), 
    (18.29046925478562, -15.911204436641512), 
    (43.51978926747693, -3.9379665287790218), 
    (40.20079539228393, -19.19139379052926)
]

topology = [
    (0,1),    
    (0,4),
    (1,2),
    (1,3),
    (4,5),
    (4,6)
]

# # no interference
# canInterWith = [ [] for x in range(numNodes) ]
# # maximum interference
# canInterWith = [ [y for y in range(numNodes) ] for x in range(numNodes) ]

canInterWith = get_possible_interference_info(nodes, CC2420Radio.txRange)
for i in range(len(canInterWith)):
    print("{} can interfere with {}".format(i, canInterWith[i]))
bws = [4, 2]

fwbiSchedule = fwbi.FWBI()

fwbiSchedule.set_number_of_nodes(numNodes)
fwbiSchedule.set_network_topology(topology)
fwbiSchedule.set_interference_info(canInterWith)
fwbiSchedule.set_sink_id(0)
fwbiSchedule.set_available_bandwidths(bws)

fwbiSchedule.schedule()

print("Results:", end=" ")
ssize    = fwbiSchedule.get_slot_schedule_size()
schedule = fwbiSchedule.get_slot_schedule()
bsched   = fwbiSchedule.get_bandwidth_schedule()
print("{} slots required".format(ssize))
for i in range(len(schedule)):
    print("Node {}, bw: {}, slots: {}".format(i, bsched[i], schedule[i]))