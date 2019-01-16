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

from clock import Clock

class Node:
    # basic
    # MAX_TXS       = 3
    # sinkNodesAddr = [1]
    # basicPayload  = []

    def __init__(self, id, x, y, energy, isSink=False, clock=None, radio=None,
                 verbose=False):
        assert type(clock) is Clock or clock is None, "Need a clock object"
        self.verbose  = verbose
        self.id       = id
        self.isSink   = isSink
        self.position = [x, y] 
        self.clock    = clock
        self.radio    = radio
        # for TDMA
        self.slots     = []
        self.sloti     = 0
        self.slotSize  = 0
        self.nextSlot  = 0
        self.slotEnd   = 0
        self.frameTime = 0
        # energy related
        self.maxEnergy = energy
        self.energy    = energy
        # for messages
        self.inbox         = []
        self.outbox        = []
        self.msgsLostCount = 0
        self.msgsLostLimit = 5
        # for statistics
        self.recvdMsgsCounter = 0
        self.dropdMsgsCounter = 0
        self.dataCollections  = 0
        self.sentMsgsCounter  = 0
        self.avgNumHops       = 0
        self.maxNumHops       = 0 
        self.avgTimeSpent     = 0
        self.maxTimeSpent     = 0

    def move(self, newX, newY, newDepth=0):
        # Move node to new position.
        self.position[0] = newX
        self.position[1] = newY

    def set_id(self, newid):
        self.id = newid

    def set_clock_src(self, clock):
        self.clock = clock

    def set_frame_time(self, frameTime):
        self.frameTime = frameTime

    def set_slot_size(self, slotSize):
        assert (slotSize > 0), "Time slot can not be <= 0"
        self.slotSize = slotSize

    def set_verbose(self, verbose):
        self.verbose = verbose

    def add_slot(self, newSlot):
        self.slots.append(newSlot)
        self.slots.sort()

    def update_next_slot(self):
        self.nextSlot = self.slots[self.sloti]
        self.sloti = (self.sloti + 1) % len(self.slots)

    def recharge(self, energy):
        self.energy += energy
        self.energy = min(self.energy, self.maxEnergy)

    def get_outbox_len(self):
        return len(self.outbox)

    def execute(self):
        raise NotImplementedError

    def collect_data(self):
        raise NotImplementedError
    
    def recv_msg(self, recvMsg):
        raise NotImplementedError