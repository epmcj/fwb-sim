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
    def __init__(self, id, x, y, energy, isSink, clock=None, slotSize=1, 
                 numSlots=1, verbose=False):
        super(TelosB, self).__init__(id, x, y, energy, clock, slotSize, 
                                     numSlots)
        # node info
        self.radio = CC2420Radio()
        self.mode  = TelosBMode.IDLE
        # routing info
        self.parent   = None
        self.children = []

    def set_tx_mode(self):
        self.mode = TelosBMode.TX
        
    def set_rx_mode(self):
        self.mode = TelosBMode.RX

    def set_idle_mode(self):
        self.mode = TelosBMode.IDLE
    
    def set_sleep_mode(self):
        self.mode = TelosBMode.SLEEP

    def get_mode(self):
        return self.mode

    def execute(self):
        currTime = self.clock.read()
        if currTime == self.nextSlot:
            self.slotEnd = self.nextSlot + self.slotSize
            self.update_next_slot()
    # VERIFICAR FIM DO SLOT
        if not self.isSink:
            # if the node has received new messages, then it put them in the 
            # outbox to send them
            if len(self.outbox) != 0:
                msg = self.outbox.pop(0)
                self.sentMsgsCounter += 1
                return EG.create_tx_start_event(currTime, msg)
        return EG.create_node_sleep_event(currTime, self.id)

            

    def collect_data(self):
        # if the node is not a sink, then it adds a new message to the outbox
        if not self.isSink:
            if self.parent is None:
                raise Exception("Node {} has no parent".format(self.id))
            msg = Message(self.id, self.parent)
            self.outbox.append(msg)
    
    def recv_msg(self, recvMsg):
        self.recvdMsgsCounter += 1
        if not self.isSink:
            recvMsg.src = self.id
            recvMsg.dst = self.parent
            self.outbox.append(recvMsg)