###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Basic message to use with the simulator. Its structure must be           ##
##  respected.                                                               ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################

class Message:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    # all msgs are 128 bytes (1024 bits) long
    def __len__(self):
        return 1024

    def __str__(self):
        return "Message from: " + str(self.src) + " to " + str(self.dst)