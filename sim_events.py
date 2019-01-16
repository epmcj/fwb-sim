###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Events for the actions of the simulator. It defines codes for message    ##
##  receive, message send and node call (for execution) events. It also      ##
##  contains an Event Generator to create the events for the simulator.      ##
##  Events are represented by tuples for performance reasons.                ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
class EventCode:
    TX_START   = 0
    TX_FINISH  = 1
    NODE_CALL  = 2
    NODE_SLEEP = 3

class EventGenerator:
    def create_node_call_event(time, nodeid):
        return (time, EventCode.NODE_CALL, nodeid)

    def create_node_sleep_event(time, nodeid):
        return (time, EventCode.NODE_SLEEP, nodeid)

    def create_tx_start_event(time, msg):
        return (time, EventCode.TX_START, msg)

    def create_tx_finish_event(time, txid):
        return (time, EventCode.TX_FINISH, txid)