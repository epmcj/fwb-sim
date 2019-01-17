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
        # for fwb slot attribution
        self.nodeSlot = []
        self.bws      = []  # bandwidths available
        # application parameters
        self.appStart    = tools.INFINITY
        self.appInterval = tools.INFINITY
        self.appStop     = tools.INFINITY 
        # control
        self.clock   = Clock()
        self.evMngr  = EventManager()
        self.verbose = verbose
        self.channel = None
        # node control
        self.nodes = []
        # transmission control
        self.txs = [] # composed of [tx_id, [src, msg, power], success]
        # statistics
        self.startedTxs  = 0
        self.finishedTxs = 0
        self.failedRxs   = 0
        self.succeedRxs  = 0

    def add_node(self, node):
        #
        assert issubclass(type(node), Node)
        node.set_id(len(self.nodes))
        node.set_clock_src(self.clock)
        node.set_verbose(self.verbose)
        self.nodes.append(node)
    
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def set_slot_size(self, slotSize):
        self.slotSize = slotSize

    def set_channels_info(self, alpha, ambNoise, channelSpeedups):
        self.channel = RFChannel(alpha, ambNoise)

    def set_network_topology(self, relations):
        # relations must be a (parent, child) tuple list 
        # assert self.numNodes is not 0
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


    def set_data_collection(self, appStart, appInterval, appStop=tools.INFINITY):
        self.appStart    = appStart
        self.appInterval = appInterval
        self.appStop     = appStop

    def get_num_nodes(self):
        return len(self.nodes.values())

    def get_num_txs(self):
        return self.finishedTxs()

    def get_num_rxs_successes(self):
        return self.succeedRxs

    def get_num_rxs_failures(self):
        return self.failedRxs

    def do_data_collection(self):
        # Method to feed the routing algorithm with application messages.
        for node in self.nodes.values():
            if node.energy > 0 and node.isSink is False:
                node.collect_data()

    def start(self, stopExec):
        assert (stopExec > 0), "Execution time must be > 0" 
        assert (self.slotSize > 0), "TDMA time slots must be > 0" 
        assert (len(self.nodes) is not 0), "Missing nodes" 
        assert (self.appStart is not tools.INFINITY), "Missing app start time"
        assert (self.appInterval is not tools.INFINITY), "Missing app "+ \
                                                         "interval time"
        assert (self.appStop > self.appStart), "Stop time must be > start time"
        assert (self.channel != None), "Missing transmission channel"

        # initialization
        self.startedTxs  = 0
        self.finishedTxs = 0
        self.failedRxs   = 0
        self.succeedRxs  = 0
        self.clock.reset()
        self.evMngr.reset()

        self.do_schedule()

        # distributing time slots
        self.frameTime = self.schedulingSize * self.slotSize
        for i in range(len(self.nodeSlot)):
            self.nodes[i].set_slot_size(self.slotSize)
            self.nodes[i].set_frame_time(self.frameTime)
            for slot in self.nodeSlot[i]:
                ntime = self.clock.read() + (slot * self.slotSize)
                self.evMngr.insert(EG.create_call_event(ntime, i))
                self.nodes[i].add_slot(ntime)
            self.nodes[i].start_tdma_system()

        # distributing bandwidths [...]

        print("Simulation started")
        while len(self.evMngr) != 0:
            event = self.evMngr.get_next()
            eTime = event[0]
            if eTime > self.clock.read():
                raise Exception("Can not go to the past!")
            self.clock.force_time(eTime) # adjusting time for event
            if eTime >= self.nextFrameStart:
                self.framesExecuted += 1
                self.nextFrameStart += self.frameTime
            ecode = event[1]
            einfo = event[2]
            if ecode is EventCode.NODE_CALL:
                # einfo = node id
                if self.verbose:
                    print("Node " + str(einfo) + " is executing")
                newEvent = self.nodes[einfo].execute()
                if newEvent[1] is EventCode.TX_START:
                    # node will transmit a message
                    msg = newEvent[2]
                    self.__handle_tx_request(einfo, msg)
                elif newEvent[1] is EventCode.NODE_SLEEP:
                    # node will sleep until its next slot
                    ntime = self.nextFrameStart + (self.nodeSlot[i] * \
                            self.slotSize)
                    self.evMngr.insert(EG.create_node_call_event(ntime, einfo))
                else:
                    raise Exception("Bad event {} from node {}".format(
                                        newEvent[1], einfo))
                        
            elif ecode is EventCode.TX_FINISH:
                # einfo = transmission id
                if self.verbose:
                    print("TX " + str(einfo) + " is finishing")
                self.__handle_tx_finish(einfo)
            else:
                raise Exception("Unknown event code " + str(ecode))
        print("Simulation finished")

    def __handle_tx_request(self, src, msg):
        # estimating transmission
        ttime, tenergy = tools.estimate_transmission(msg, self.nodes[src].radio)
        ftime = self.clock.read() + ttime
        # adding call node event (time is multiplied by 1.01 to assure it will 
        # called after the transmission was completed)
        self.evMngr.insert(EG.create_call_event(ftime * 1.01, src))
        # evaluating transmissions
        txid = self.startedTxs
        txInfo = [src, msg, self.nodes[src].radio.txPower]
        self.txs.append([txid, txInfo, True])
        self.startedTxs += 1
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
                    nodes[dst].recv_msg(msg)
                    self.succeedRxs += 1
                else:
                    self.failedRxs += 1
                self.finishedTxs += 1
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
            pos   = nodes[src].position
            power = tinfo[2]
            nodesTxs.append([src, pos, power])
            if tsuccess:
                txsToCheck.append(i)
            i += 1
        # checking the transmissions
        for i in txsToCheck:
            tinfo = self.txs[i][1]
            src   = tinfo[0]
            power = tinfo[2]
            dst   = tinfo[1].dst # from msg
            spos  = nodes[src].position
            dpos  = nodes[dst].position
            # calculating SINR
            dist   = tools.distance(spos, dpos)
            sinr   = power / (dist) ** self.channel.alpha
            # calculating interference
            interf = 0
            for isrc, ipos, ipower in nodesTxs:
                if isrc != src:
                    dist = tools.distance(ipos, dpos)
                    inter += ipower / (dist) ** self.channel.alpha
            # calculating final SINR and checking for zero division (when there 
            # is neither interference nor noise)
            if (inter + self.channel.noise) == 0:
                sinr = floa("inf")
            else:
                sinr = sinr / (self.channel.noise + inter)
            # checking if the data can be decoded
            if sinr >= self.nodes[dst].radio.minSIR:
                self.txs[i][2] = True
            else:
                self.txs[i][2] = False


    # schedule time slots
    def do_schedule(self):
        return None
        
        