###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Node base implementation.                                                ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
from clock      import Clock
from node       import Node
from radios     import CC2420Radio
from message    import Message
from sim_events import EventGenerator as EG

class TelosBMode:
    RX    = 0
    TX    = 1
    IDLE  = 2
    SLEEP = 3

class TelosB(Node):
    def __init__(self, id, x, y, energy, isSink, slotSize=1, numSlots=1, 
                 verbose=False):
        super(TelosB, self).__init__(id, x, y, energy, isSink, Clock(), 
                                     slotSize, numSlots)
        # node info
        self.radio = CC2420Radio(CC2420Radio.maxTxPower)
        self.mode  = TelosBMode.IDLE
        # for energy consumption
        self.voltage = 3.0 # V
        self.txPower = self.voltage * CC2420Radio.txCurrent
        self.rxPower = self.voltage * CC2420Radio.rxCurrent
        # routing info
        self.parent   = None
        self.children = []
        # statistics (for sink)
        self.latencies = []

    def set_tx_mode(self):
        self.mode = TelosBMode.TX
        
    def set_rx_mode(self):
        self.mode = TelosBMode.RX

    def set_idle_mode(self):
        self.mode = TelosBMode.IDLE
    
    def set_sleep_mode(self):
        self.mode = TelosBMode.SLEEP

    def set_tx_power(self, txPower):
        self.radio.set_tx_power(txPower)

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.children = children

    def get_mode(self):
        return self.mode

    def execute(self):
        currTime = self.clock.read()
        if currTime == self.get_next_slot():
            # slot ends early because of the guard time
            self.slotEnd = self.get_next_slot() + (self.slotSize * 0.9)
            self.update_next_slot()
        if (currTime < self.slotEnd) and (not self.isSink):
            # send the messages to its parent
            if len(self.outbox) != 0:
                msg = self.outbox.pop(0)
                # # insert timestamp in message that was just collected
                # if msg.time == None:
                #     msg.time = currTime
                self.sentMsgsCounter += 1
                self.set_tx_mode()
                return EG.create_tx_start_event(currTime, msg)
        self.set_rx_mode()
        return EG.create_node_sleep_event(currTime, self.id)            

    def collect_data(self):
        # if the node is not a sink, then it adds a new message to the outbox
        if not self.isSink:
            if self.parent is None:
                raise Exception("Node {} has no parent".format(self.id))
            # msg = Message(self.id, self.parent, None)
            msg = Message(self.id, self.parent, self.dataCollections, 
                          self.clock.read())
            self.outbox.append(msg)
            self.dataCollections += 1
    
    def consume_rx_energy(self, time):
        self.energy -= self.rxPower * time

    def consume_tx_energy(self, time):
        self.energy -= self.txPower * time

    def finish_tx(self, sendTime):
        self.consume_tx_energy(sendTime)

    def recv_msg(self, recvMsg):
        # consume energy for the reception
        # self.consume_rx_energy(recvTime)
        self.recvdMsgsCounter += 1
        if not self.isSink:
            recvMsg.src = self.id
            recvMsg.dst = self.parent
            self.outbox.append(recvMsg)
        else:
            self.latencies.append(self.clock.read() - recvMsg.time)