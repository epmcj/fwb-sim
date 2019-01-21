###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Basic Scheduler class definition.                                        ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################

class Scheduler:
    def schedule(self):
        raise NotImplementedError

    def get_slot_schedule(self):
        raise NotImplementedError

    def get_slot_schedule_size(self):
        raise NotImplementedError

    def get_bandwidth_schedule(self):
        raise NotImplementedError