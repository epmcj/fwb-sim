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

# (!) Event Code value is used as event priority by the scheduler
class EventCode:
    STOP_SIM     = 0
    TX_START     = 1
    TX_FINISH    = 2
    COLLECT_DATA = 3
    NODE_CALL    = 4
    NODE_RESUME  = 5
    NODE_SLEEP   = 6

class EventGenerator:
    # Events are composed by (time, event code, event info)
    def create_node_call_event(time, nodeid):
        return [time, EventCode.NODE_CALL, nodeid]

    def create_node_resume_event(time, nodeid):
        return [time, EventCode.NODE_RESUME, nodeid]

    def create_node_sleep_event(time, nodeid):
        return [time, EventCode.NODE_SLEEP, nodeid]

    def create_tx_start_event(time, msg):
        return [time, EventCode.TX_START, msg]

    def create_tx_finish_event(time, txid):
        return [time, EventCode.TX_FINISH, txid]

    def create_data_collection_event(time):
        return [time, EventCode.COLLECT_DATA, None] # no information

    def create_stop_simulation_event(time):
        return [time, EventCode.STOP_SIM, None] # no information

    
    # changes event object to reduce memory usage. only fields != None are 
    # changed
    def change_event(event, newTime=None, newCode=None, newInfo=None):
        if newTime != None:
            event[0] = newTime
        if newCode != None:
            event[1] = newCode
        if newInfo != None:
            event[2] = newInfo
        return event