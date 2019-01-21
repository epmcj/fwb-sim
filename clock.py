###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  Clock class for time tracking.                                           ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################
from tools import INFINITY

class Clock:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__currTime = 0
        self.nextCall   = INFINITY
        self.lastCall   = INFINITY
        self.interval   = 0
        self.routine    = None

    def run(self, time):
        self.__currTime = self.__currTime + time
        while self.__currTime >= self.nextCall:
            self.routine()
            if self.nextCall >= self.lastCall:
                self.nextCall = INFINITY
            else:
                self.nextCall = self.nextCall + self.interval
    
    def force_time(self, time):
        self.__currTime = time
        while self.__currTime >= self.nextCall:
            self.routine()
            if self.nextCall >= self.lastCall:
                self.nextCall = INFINITY
            else:
                self.nextCall = self.nextCall + self.interval

    def read(self):
        return self.__currTime

    def set_periodic_alarm(self, call, start, interval, stop = INFINITY):
        self.nextCall = start
        self.interval = interval
        self.routine  = call
        self.lastCall = stop
        while self.nextCall < self.__currTime:
            self.nextCall = self.nextCall + self.interval

    # def set_periodic_temp(self, call, interval, stop = INFINITY):
    #     self.interval = interval
    #     self.lastCall = stop
    #     self.routine  = call
    #     self.nextCall = self.__currTime + interval

    def alarm_is_on(self):
        return self.nextCall is not INFINITY