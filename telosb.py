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

from node   import Node
from radios import CC2420Radio

class TelosBMode:
    RX    = 0
    TX    = 1
    IDLE  = 2
    SLEEP = 3

class TelosB(Node):
    # basic
    MAX_TXS       = 3
    sinkNodesAddr = [1]
    basicPayload  = []

    def __init__(self, addr, x, y, energy, isSink, clock=None, slotSize=1, 
                 numSlots=1, verbose=False):
        super(TelosB, self).__init__(addr, x, y, energy, clock, slotSize, 
                                     numSlots)
        self.radio = CC2420Radio()
        self.mode = TelosBMode.IDLE

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
        raise NotImplementedError

    def collect_data(self):
        raise NotImplementedError
    
    def recv_msg(self, recvMsg):
        raise NotImplementedError