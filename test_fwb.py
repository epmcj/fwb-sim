import fwb

parentOf = [[1,4],
            [2,3],
            [],
            [],
            [5,6],
            [],
            []]

bws = [2, 4, 8]

fwbSchedule = fwb.FWB()

fwbSchedule.set_number_of_nodes(7)
fwbSchedule.set_parent_info(parentOf)
fwbSchedule.set_sink_id(0)
fwbSchedule.set_available_bandwidths(bws)

fwbSchedule.schedule()

print("Results")
ssize    = fwbSchedule.get_slot_schedule_size()
schedule = fwbSchedule.get_slot_schedule()
bsched   = fwbSchedule.get_bandwidth_schedule()
print("{} slots required".format(ssize))
for i in range(len(schedule)):
    print("Node {}, bw: {}, slots: {}".format(i, bsched[i], schedule[i]))