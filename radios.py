###############################################################################
##  Laboratorio de Engenharia de Computadores (LECOM)                        ##
##  Departamento de Ciencia da Computacao (DCC)                              ##
##  Universidade Federal de Minas Gerais (UFMG)                              ##
##                                                                           ##
##  [...]                                                                    ##
##                                                                           ##
##  TODO:                                                                    ##
##                                                                           ##
##  Author: Eduardo Pinto (epmcj@dcc.ufmg.br)                                ##
###############################################################################

class CC2420Radio:
    # CC2420 radio 
    # http://www.ti.com/lit/ds/symlink/cc2420.pdf
    txPowerConsumption = 0
    rxPowerConsumption = 0
    maxTxPower         = 0      # dB
    minTxPower         = -24    # dB
    minSIR             = -3     # dB
    txRange            = 30     # m (max indoor)
    txRate             = 250e3  # 250 kbps
    
    def __init__(self):
        self.isOn    = False
        self.txPower = 0

    def turn_on(self):
        self.isOn = True

    def turn_off(self):
        self.isOn = False

    def set_tx_power(self, txPower):
        assert txPower <= CC2420Radio.maxTxPower and \
               txPower >= CC2420Radio.minTxPower, 
               "Radio Power must be between -24 and 0 dB"
        self.txPower = txPower