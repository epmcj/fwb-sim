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
from node import Node
from event_mngr import EventManager
from sim_events import EventGenerator as EG, EventCode
from message    import *
from modens     import AcousticModem as AM, OpticalModem as OM
from clock      import Clock
from channels   import RFChannel
import tools

class Simulator:
    beta = 0
    def __init__(self, verbose=False):
        self.packetSize   = 0
        self.tdmaSlotSize = 0
        # topology information
        self.parentOf = []
        self.childOf  = []
        # for fwb slot attribution
        self.node_channel = []
        self.slot_node    = []
        # channels
        self.channels = []
        # application parameters
        self.appStart    = tools.INFINITY
        self.appInterval = tools.INFINITY
        self.appStop     = tools.INFINITY 
        # control
        self.clock     = Clock()
        self.evMngr    = EventManager()
        self.verbose   = verbose
        self.firstNode = 0
        # node control
        self.nodesUpdated = True
        self.numNodes     = 0
        self.nodes        = {}
        # statistics
        self.numTxs     = 0
        self.failedRxs  = 0
        self.succeedRxs = 0

    def add_node(self, node):
        #
        assert issubclass(type(node), Node)
        node.set_clock_src(self.clock)
        node.set_verbose(self.verbose)
        self.nodes[node.addr]        = node
        self.node_channel[node.addr] = 0
        self.numNodes += 1
        # self.nodesUpdated = False

    def set_tdma_slot(self, tdmaSlotSize):
        self.tdmaSlotSize = tdmaSlotSize

    def set_packet_size(self, packetSize):
        self.packetSize = packetSize

    def set_channels_info(self, alpha, ambNoise, channelSpeedups):
        self.ambNoise = ambNoise
        self.channels = []
        for speedup in channelSpeedups:
            self.channels.append(RFChannel(alpha, speedup))

    def set_network_topology(self, relations):
        # relations must be a (parent, child) tuple list 
        assert self.numNodes is not 0
        self.parentOf = [ [] for i in range(self.numNodes) ]
        self.childOf  = [ [] for i in range(self.numNodes) ]
        for parent, child in relations:
            self.parentOf[parent].append(child)
            self.childOf[child].append(parent)
        # removing duplicates
        for i in range(self.numNodes):
            self.parentOf[i] = list(set(self.parentOf[i]))
            self.childOf[i]  = list(set(self.childOf[i]))
        if self.verbose:
            for i in range(self.numNodes):
                print("Node {} is parent of nodes {}".format(i, 
                                                             self.parentOf[i]))


    def set_data_collection(self, appStart, appInterval, appStop=tools.INFINITY):
        self.appStart    = appStart
        self.appInterval = appInterval
        self.appStop     = appStop

    def get_num_nodes(self):
        return len(self.nodes.values())

    def get_num_txs(self):
        return self.numTxs

    def get_num_rxs_successes(self):
        return self.succeedRxs

    def get_num_rxs_failures(self):
        return self.failedRxs

    def create_app_msgs(self):
        # Method to feed the routing algorithm with application messages.
        for node in self.nodes.values():
            if node.energy > 0 and node.isSink is False:
                node.collect_data()

    def print_data(self):
        print("Time: {0:.5f}".format(self.clock.read()))
        print("Number of transmissions: " + str(self.atxs))

    def __handle_send_event(self, event):
        # Check if some transmission is successful. In case of success, events
        # for message receptions are created.
        msg          = event[2]
        isAcoustic   = msg.flags & MsgFlags.ACOUSTIC
        destinations = []
        if msg.dst == BROADCAST_ADDR:
            assert isAcoustic, "Optical broadcasts are not allowed"
            destinations = self.aneighbors[msg.src]
        else:
            destinations = [msg.dst]

        if isAcoustic:
            self.atxs += 1
        else:
            self.otxs += 1

        for dst in destinations:
            srcPos = self.nodes[msg.src].position
            dstPos = self.nodes[dst].position
            dist   = tools.distance(srcPos, dstPos)
            if self.verbose:
                print("Message " + str(msg.src) + "->" + str(dst), end=" ")
            if isAcoustic:
                success = self.achannel.use(AM.frequency, AM.txPower, dist, \
                                            len(msg))
                if success:
                    self.asucceedRxs += 1
                    propTime = self.achannel.get_propagation_time(dist)
                    recvTime = self.clock.read() + propTime
                    self.evMngr.insert(EG.create_recv_event(recvTime, dst, msg))
                    if self.verbose:
                        print("was successfull: will arrive " + str(recvTime))
                else:
                    if self.verbose:
                        print("failed")
                    self.afailedRxs  += 1
            else:
                success = self.ochannel.use(OM.txPower, dist, dist, self.beta, \
                                            len(msg))
                if success:
                    self.osucceedRxs += 1
                    propTime = self.ochannel.get_propagation_time(dist)
                    recvTime = self.clock.read() + propTime
                    self.evMngr.insert(EG.create_recv_event(recvTime, dst, msg))
                    if self.verbose:
                        print("was successfull: will arrive " + str(recvTime))
                else:
                    if self.verbose:
                        print("failed")
                    self.ofailedRxs  += 1

    def start(self, stopExec):
        assert (stopExec > 0), "Execution time must be > 0" 
        assert (self.tdmaSlotSize > 0), "TDMA time slots must be > 0" 
        assert (self.packetSize > 0), "Packet size can not be <= 0"
        assert (len(self.nodes) is not 0), "Missing nodes" 
        assert (self.appStart is not tools.INFINITY), "Missing app start time"
        assert (self.appInterval is not tools.INFINITY), "Missing app "+ \
                                                         "interval time"
        assert (self.appStop > self.appStart), "Stop time must be > start time"

        # if it is the first simulation start call
        if not self.clock.alarm_is_on():
            # set alarm to start the data collection process
            self.clock.set_alarm(self.create_app_msgs, self.appStart, \
                                 self.appInterval, self.appStop)
            # Creating a basic payload to avoid large memory usage
            # Removes two header size because of Packet inside Packet 
            # (used for statistics)
            payloadSize = self.packetSize - (2 * Message.headerSize)
            basicPayload = list(0 for x in range(0, payloadSize))
            for node in self.nodes.values():
                node.basicPayload = basicPayload
                node1stSlot       = self.clock.read() + (self.tdmaSlotSize * \
                                    (node.addr - 1))
                self.evMngr.insert(EG.create_call_event(node1stSlot, node.addr))
        
        # Updating node information because some node was recently added
        if not self.nodesUpdated:
            self.__update_nodes_info()

        nodesList = [0] + list(self.nodes.values()) # to align with addresses
        numSlots  = int(stopExec/self.tdmaSlotSize)
        print("Simulation started")
        while len(self.evMngr) != 0:
            event = self.evMngr.get_next()
            eTime = event[0]
            if eTime >= stopExec:
                break
            self.clock.force_time(eTime) # adjusting time for event
            ecode = event[1]
            naddr = event[2]
            if ecode is EventCode.NODE_CALL:
                if self.verbose:
                    print("Node " + str(naddr) + " is executing")
                newEvents = nodesList[naddr].execute()
                for newEvent in newEvents:
                    # msg send events are handled
                    if newEvent[1] is EventCode.MSG_SEND:
                       self.__handle_send_event(newEvent)
                    else:
                        self.evMngr.insert(newEvent)
            elif ecode is EventCode.MSG_RECV:
                msg = event[3]
                if self.verbose:
                    print("Node " + str(naddr) + " is receiving a message")
                newEvents = nodesList[naddr].recv_msg(msg)
                for newEvent in newEvents:
                    # msg send events are handled
                    if newEvent[1] is EventCode.MSG_SEND:
                       self.__handle_send_event(newEvent)
                    else:
                        self.evMngr.insert(newEvent)
            else:
                raise Exception("Unknown event code " + str(ecode))
        print("Simulation finished")

    # simulate transmission
    def do_transmission(msg):
        # getting information for sinr calculation
        src  = msg.src
        dst  = msg.dst
        channel = self.channels[self.node_channel[src]]
        alpha   = channel.alpha # assumes that all channels have the same alpha
        dist    = tools.distance(nodes[src].position, nodes[dst].position)
        # calculating sinr
        sinr  = self.nodes[src].radio.txPower / (dist)**alpha
        inter = 0
        for addr in self.nodes.keys():
            if addr != src and self.nodes[addr].radio.isOn:
                inter += self.nodes[addr].radio.txPower / (dist)**alpha
        if (inter + self.ambNoise) == 0:
            sinr = floa("inf")
        else:
            sinr = sinr / (noise + inter)

        if sinr >= self.nodes[addr].radio.minSIR:
            # transmission was successfull
            self.succeedRxs += 1
        else:
            self.failedRxs  += 1
        