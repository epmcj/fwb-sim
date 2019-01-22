###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Simulator for underwater optical-acoustic networks.                      ##
##                                                                           ##
##  TODO:                                                                    ##
##  - insert verifications in set_topology                                   ##
##  - implement fwb algorithm                                                ##
##  - change timeslots attribution scheme                                    ##
##  - implement how to simulate tranmsission w/ interference                 ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
from node       import Node
from event_mngr import EventManager
from sim_events import EventGenerator as EG, EventCode
from clock      import Clock
from channels   import RFChannel
import tools
# import math

class Simulator:
    beta = 0
    def __init__(self, verbose=False):
        self.slotSize       = 0
        self.schedulingSize = 0
        self.framesExecuted = 0
        self.nextFrameStart = 0
        # topology information
        self.parentOf = []
        self.childOf  = []
        # for timeslot and bandwidth attribution
        self.nodeSlots = None
        # application parameters
        self.dcStart    = tools.INFINITY
        self.dcInterval = tools.INFINITY
        self.dcStop     = tools.INFINITY 
        # control
        self.verbose   = verbose
        self.channel   = None
        self.clock     = Clock()
        self.evMngr    = EventManager()
        # node control
        self.nodes  = []
        self.sinkid = None  # only one sink node in the network
        # transmission control
        self.txs = [] # composed of [tx_id, [src, msg, power], success]
        # statistics
        self.ongoingTxs  = 0
        self.finishedTxs = 0
        self.failedRxs   = 0
        self.succeedRxs  = 0
        self.numDCollect = 0 # number of data collections

    def add_node(self, node):
        assert issubclass(type(node), Node)
        node.set_id(len(self.nodes))
        node.set_clock_src(self.clock)
        node.set_verbose(self.verbose)
        self.nodes.append(node)
        if node.isSink:
            self.sinkid = node.id
    
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def set_slot_size(self, slotSize):
        self.slotSize = slotSize

    def set_channel_info(self, alpha, ambNoise):
        self.channel = RFChannel(alpha, ambNoise)

    # tschedule must be a list of slots for each node in the network. Slots must
    # be numbered from 1 to n.
    def set_timeslot_schedule(self, tschedule):
        assert len(tschedule) == len(self.nodes)
        self.nodeSlots = tschedule
        slotsUsed = set()
        for nodeSlots in tschedule:
            for slot in nodeSlots:
                slotsUsed.add(slot)
        self.frameSize = len(slotsUsed)

    def set_network_topology(self, relations):
        # relations must be a (parent, child) tuple list for each node in the 
        # network
        assert len(self.nodes) is not 0, "No nodes yet"
        numNodes = len(self.nodes)
        self.parentOf = [ [] for i in range(numNodes) ]
        self.childOf  = [ [] for i in range(numNodes) ]
        for parent, child in relations:
            self.parentOf[parent].append(child)
            self.childOf[child].append(parent)
        # removing duplicates
        for i in range(numNodes):
            self.parentOf[i] = list(set(self.parentOf[i]))
            self.childOf[i]  = list(set(self.childOf[i]))
        if self.verbose:
            for i in range(numNodes):
                print("Node {} is parent of ".format(i) + \
                      "nodes {}".format(self.parentOf[i]))

    def set_data_collection_start(self, dcStart):
        assert (dcStart >= 0), "Start time must be >= 0"
        self.dcStart = dcStart

    def set_data_collection(self, dcStart, dcInterval, dcStop=tools.INFINITY):
        self.dcStart    = dcStart
        self.dcInterval = dcInterval
        self.dcStop     = dcStop

    def get_num_nodes(self):
        return len(self.nodes.values())

    def get_ongoing_txs(self):
        return self.ongoingTxs

    def get_num_txs(self):
        return self.finishedTxs

    def get_num_rxs_successes(self):
        return self.succeedRxs

    def get_num_rxs_failures(self):
        return self.failedRxs

    def do_data_collection(self):
        # Method to generate new messages for the nodes.
        for node in self.nodes:
            if node.energy > 0 and node.isSink is False:
                node.collect_data()
        self.numDCollect += 1

    def run(self, framesToSim):
        assert (framesToSim > 0), "Execution time must be > 0" 
        assert (self.slotSize > 0), "TDMA time slots must be > 0" 
        assert (len(self.nodes) is not 0), "Missing nodes" 
        assert (self.dcStart is not tools.INFINITY), "Missing app start time"
        assert (self.dcInterval is not tools.INFINITY), "Missing app "+ \
                                                        "interval time"
        assert (self.dcStop > self.dcStart), "Stop time must be > start time"
        assert (self.channel != None), "Missing transmission channel"

        # initialization
        self.ongoingTxs  = 0
        self.finishedTxs = 0
        self.failedRxs   = 0
        self.succeedRxs  = 0
        self.clock.reset()
        self.evMngr.reset()

        # distributing topology information
        for nid in range(len(self.nodes)):
            if len(self.childOf[nid]) != 0:
                self.nodes[nid].set_parent(self.childOf[nid][0])
            self.nodes[nid].set_children(self.parentOf[nid])

        # distributing time slots
        self.frameTime = self.frameSize * self.slotSize
        for i in range(len(self.nodeSlots)):
            self.nodes[i].set_slot_size(self.slotSize)
            self.nodes[i].set_frame_time(self.frameTime)
            for slot in self.nodeSlots[i]:
                # slots are numbered from 1 to n
                ntime = self.clock.read() + ((slot - 1) * self.slotSize)
                self.evMngr.insert(EG.create_node_call_event(ntime, i))
                self.nodes[i].add_slot(ntime)
            self.nodes[i].start_tdma_system()

        # setting alarm to start the data collection process
        # self.dcInterval = self.frameTime
        self.clock.set_periodic_alarm(self.do_data_collection, self.dcStart, \
                                      self.dcInterval, self.dcStop)

        simTime = framesToSim * self.frameTime
        self.evMngr.insert(EG.create_stop_simulation_event(simTime))

        print("========= Simulation started =========")
        while len(self.evMngr) != 0:
            event = self.evMngr.get_next()
            etime = event[0]
            if etime < self.clock.read():
                raise Exception("Can not go to the past ({} < {})".format(
                                                    self.clock.read(), etime))
            self.clock.force_time(etime) # adjusting time for event
            if self.verbose:
                print("{0:.5f}: ".format(self.clock.read()), end = "")
            if etime >= self.nextFrameStart:
                self.framesExecuted += 1
                self.nextFrameStart += self.frameTime
            ecode = event[1]
            einfo = event[2]

            if ecode is EventCode.NODE_CALL or ecode is EventCode.NODE_RESUME:
                # einfo := node id
                if ecode is EventCode.NODE_CALL:
                    # updating for the next frame
                    ntime = etime + self.frameTime
                    self.evMngr.insert(EG.change_event(event, newTime=ntime))
                    if self.verbose:
                        print("Node {} new slot".format(einfo))
                else:
                    if self.verbose:
                        print("Node {} resuming exec".format(einfo))

                newEvent = self.nodes[einfo].execute()
                if newEvent[1] is EventCode.TX_START:
                    # node will transmit a message
                    msg = newEvent[2]
                    self.__handle_tx_request(einfo, msg)
                elif newEvent[1] is EventCode.NODE_SLEEP:
                    if self.verbose:
                        print("\tNode {} finishing exec".format(einfo))
                    continue
                else:
                    raise Exception("Bad event {} from node {}".format(
                                        newEvent[1], einfo))   
            
            elif ecode is EventCode.TX_FINISH:
                # einfo = transmission id
                if self.verbose:
                    print("TX {} is finishing".format(einfo))
                self.__handle_tx_finish(einfo)
            
            elif ecode is EventCode.STOP_SIM:
                break

            else:
                raise Exception("Unknown event code " + str(ecode))
        print("========= Simulation finished =========")

    def __handle_tx_request(self, src, msg):
        # estimating transmission
        ttime, tenergy = tools.estimate_transmission(msg, self.nodes[src].radio)
        ftime = self.clock.read() + ttime
        if self.verbose:
            print("\tNode {0:d} tx: {1:.4f} to {2:.4f}".format(src,  
                                                            self.clock.read(),
                                                            ftime))
        # adding call node event (adding 0.00001 to assure it will called after
        # the transmission was completed)
        self.evMngr.insert(EG.create_node_resume_event(ftime + 0.00001, src))
        # evaluating transmissions
        txid   = self.ongoingTxs
        txInfo = [src, msg, self.nodes[src].radio.txPower]
        self.txs.append([txid, txInfo, True])
        self.ongoingTxs += 1
        self.__evaluate_txs()
        # adding event to check if the transmission was successful
        self.evMngr.insert(EG.create_tx_finish_event(ftime, txid))

    def __handle_tx_finish(self, txid):
        # find the transmission in the list and checks whether it was successful
        # or not. When it was, the message is delivered to the destination node.
        for i in range(len(self.txs)):
            if self.txs[i][0] == txid:
                tid, tinfo, tsuccess = self.txs.pop(i)
                # if the transmission was successful
                if tsuccess:
                    msg = tinfo[1]
                    dst = msg.dst
                    self.nodes[dst].recv_msg(msg)
                    self.succeedRxs += 1
                else:
                    self.failedRxs += 1
                self.finishedTxs += 1
                self.ongoingTxs  -= 1
                break

    def __evaluate_txs(self):
        # check for interferences between the current transmissions
        nodesTxs   = []
        txsToCheck = [] # indices of transmissions that must be checked (the 
                        # ones that are currently been successful)
        # gathering information to start the evaluation
        i = 0
        for tid, tinfo, tsuccess in self.txs:
            src   = tinfo[0]
            pos   = self.nodes[src].position
            power = tinfo[2]
            nodesTxs.append([src, pos, power])
            if tsuccess:
                txsToCheck.append(i)
            i += 1
        # checking the transmissions that have not yet failed.
        for i in txsToCheck:
            if self.verbose:
                print("\t- Evaluating tx {}".format(self.txs[i][0]))
            tinfo = self.txs[i][1]
            src   = tinfo[0]
            power = tinfo[2]
            dst   = tinfo[1].dst # from msg
            spos  = self.nodes[src].position
            dpos  = self.nodes[dst].position
            # calculating SINR
            dist   = tools.distance(spos, dpos)
            sinr   = power / (dist ** self.channel.alpha)
            # calculating interference
            inter = 0
            for isrc, ipos, ipower in nodesTxs:
                if isrc != src:
                    dist = tools.distance(ipos, dpos)
                    inter += ipower / (dist ** self.channel.alpha)
            # calculating final SINR and checking for zero division (when there 
            # is neither interference nor noise)
            if (inter + self.channel.noise) == 0:
                sinr = float("inf")
            else:
                sinr = sinr / (self.channel.noise + inter)
                # sinr = 10 * math.log10(sinr) # to dB
            if self.verbose:
                print("\tSINR = {0:.2f} ({1:d}->{2:d})".format(sinr, src, dst))
            # checking if the data can be decoded
            if sinr >= self.nodes[dst].radio.minSIR:
                self.txs[i][2] = True
            else:
                self.txs[i][2] = False

        return None
        
        