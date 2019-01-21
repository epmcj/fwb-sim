import fwb

topology = [(0,1),
            (0,4),
            (1,2),
            (1,3),
            (4,5),
            (4,6)]

bws      = [4, 2]
numNodes = 7

fwbSchedule = fwb.FWB()
fwbSchedule.set_number_of_nodes(numNodes)
fwbSchedule.set_network_topology(topology)
fwbSchedule.set_sink_id(0)
fwbSchedule.set_available_bandwidths(bws)

fwbSchedule.schedule()

print("Results:", end=" ")
ssize    = fwbSchedule.get_slot_schedule_size()
schedule = fwbSchedule.get_slot_schedule()
bsched   = fwbSchedule.get_bandwidth_schedule()
print("{} slots required".format(ssize))
for i in range(len(schedule)):
    print("Node {}, bw: {}, slots: {}".format(i, bsched[i], schedule[i]))

bws = [8, 4, 2]
fwbSchedule.set_available_bandwidths(bws)
fwbSchedule.schedule()

print("Results:", end=" ")
ssize    = fwbSchedule.get_slot_schedule_size()
schedule = fwbSchedule.get_slot_schedule()
bsched   = fwbSchedule.get_bandwidth_schedule()
print("{} slots required".format(ssize))
for i in range(len(schedule)):
    print("Node {}, bw: {}, slots: {}".format(i, bsched[i], schedule[i]))