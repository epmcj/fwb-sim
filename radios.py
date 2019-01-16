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

class Radio:
    def __init__(self, txPower, txRate, txPowerConsumption, rxPowerConsumption, 
                 isOn=False)
        self.txPowerConsumption = txPowerConsumption
        self.rxPowerConsumption = rxPowerConsumption
        self.txPower = txPower
        self.txRate  = txRate
        self.isOn    = isOn
    
    def turn_on(self):
        self.isOn = True

    def turn_off(self):
        self.isOn = False

class CC2420Radio(Radio):
    # CC2420 radio 
    # http://www.ti.com/lit/ds/symlink/cc2420.pdf
    txPowerConsumption = 0
    rxPowerConsumption = 0
    maxTxPower         = 0      # dB
    minTxPower         = -24    # dB
    minSIR             = -3     # dB
    txRange            = 30     # m (max indoor)
    txRate             = 250e3  # 250 kbps
    
    def __init__(self, txPower):
        super(CC2420Radio, self).__init__(0,
                                          CC2420Radio.txRate,
                                          CC2420Radio.txPowerConsumption, 
                                          CC2420Radio.rxPowerConsumption)
        self.set_tx_power(txPower)

    def set_tx_rate(self, txRate):
        assert txRate <= CC2420Radio.txRate, "CC2420 max tx rate is 250 kbps"
        self.txRate = txRate

    def set_tx_power(self, txPower):
        assert txPower <= CC2420Radio.maxTxPower and \
               txPower >= CC2420Radio.minTxPower, 
               "Radio power must be between -24 and 0 dB"
        self.txPower = txPower