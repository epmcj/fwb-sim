import fwb
import fwbi

parentOf = [[1,4],
            [2,3],
            [],
            [],
            [5,6],
            [],
            []]

bws = [4, 2]

fwbSchedule = fwb.FWB()
# fwbSchedule = fwbi.FWBI()

fwbSchedule.set_number_of_nodes(len(parentOf))
fwbSchedule.set_parent_info(parentOf)
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