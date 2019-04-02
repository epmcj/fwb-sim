###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Tests nodes behaviour.                                                   ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
class Teste:
    def __init__(self):
        self.slots     = []
        self.sloti     = None
        self.slotSize  = 0
        self.slotEnd   = 0
        self.frameTime = 0

    def add_slot(self, newSlot):
        if self.sloti is None:
            self.sloti = 0
        self.slots.append(newSlot)
        self.slots.sort()

    def get_outbox_len(self):
        return len(self.outbox)

    def get_next_slot(self):
        # should verify for slots?
        return self.slots[self.sloti]

    def start_tdma_system(self):
        self.sloti = 0

    def update_next_slot(self):
        self.slots[self.sloti] += self.frameTime
        self.sloti = (self.sloti + 1) % len(self.slots)

    def set_frame_time(self, frameTime):
        self.frameTime = frameTime

    def set_slot_size(self, slotSize):
        assert (slotSize > 0), "Time slot can not be <= 0"
        self.slotSize = slotSize

bob = Teste()
bob.add_slot(10)
# bob.add_slot(40)
bob.set_slot_size(10)
bob.set_frame_time(50)
bob.start_tdma_system()

print("next slot = {}".format(bob.get_next_slot()))
bob.update_next_slot()
print("next slot = {}".format(bob.get_next_slot()))
bob.update_next_slot()
print("next slot = {}".format(bob.get_next_slot()))
bob.update_next_slot()
print("next slot = {}".format(bob.get_next_slot()))