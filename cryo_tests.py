from tester import Test
import random
import numpy as np

#R1.2
firmware_CCR = 39749

class TestPlutoGatewayConfig(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoGatewayConfig Cryo"
        self.expected_config = [0, 1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 1]


        self.desc = "Check Pluto Gateway configuration registers. Expected:" + str(self.expected_config)

    def test(self):
        config = self.tester.plutoGateway.read_holding_registers(4, 0, 42)
        for i in range(len(self.expected_config)):
            if config[i] != self.expected_config[i]:
                self.step(("Pluto Gateway Config doesn't match expected values.  Config:\t\t%s  Expected config:%s" % (
                    str(config), str(self.expected_config))))
                return False
        self.step(("Pluto Gateway Config match expected values.Config:\t\t%s Expected config:%s" % (
        str(config), str(self.expected_config))))
        return True


class TestPlutoPLCsPresent(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestPlutoPLCsPresent"
        self.desc = "Check Pluto Gateway sees Pluto D45 as node 0."

    def test(self):
        good = True
        for n in [0]:
            plc = self.tester.plutoGateway.read_bit(36, 1, n)

            if plc == 0:
                self.step("Pluto Gateway doens't see PLC %d as node %d" % (n, n))
                good = False

        if not good:
            return False

        self.step(("Pluto Gateway sees Pluto D45 as node 0."))
        return True

class TestCRC(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestCRC"
        self.desc = "Check Pluto PLC firmware CRC."

    def test(self):
        if self.tester.plutoGateway.SR_appCRC.read()==firmware_CCR:
            self.step("Pluto PLC has the right CRC")
            return True
        else:
            self.step("Pluto PLC has the wrong CRC")
            return False




class TestChannelsBootDefault(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestChannelsBootDefault"
        self.desc = "Check if all IOs are as expected when the PLC is powered"

    def test(self):
        self.step(self.desc)

        self.step("Checking PLC IO boot default values.")

        self.setDefault(gateway=False,check=False)

        chs = []
        for ch in self.tester.testBox.plc.channels:
            if ch.boot_value != "":
                chs.append((ch, ch.boot_value))

        try:
            if self.checkChannels(chs):
                self.step("Boot IOs values Ok.")
                return True
        except:
            pass

        self.step("PLC Boot IOs values do not match defaults.")
        return False


class TestPlutoWriteReadback(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestePlutoWriteReadback"
        self.desc = "Test write and rbv Pluto addresses"

    def test(self):
        self.step(self.desc)

        plutoGateway = self.tester.plutoGateway.dict

        for ch in plutoGateway.keys():

            if plutoGateway[ch]["permissions"] == "RW":

                ch_rbv = ch.replace("_w", "")
                sleep = 0.2

                self.step("Testing %s (%s) and %s (%s)." % (
                ch, "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                ch_rbv, "%s:%s.%s" % (
                plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"], plutoGateway[ch_rbv]["bit"])))

                original_write = self.tester.plutoGateway.read_ch(ch)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if original_write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 0
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = 1
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

                write = original_write
                self.tester.plutoGateway.write_ch(ch, write)
                self.sleep(sleep)
                read = self.tester.plutoGateway.read_ch(ch_rbv)
                if write != read:
                    self.step("Failed on %s (%s) and %s (%s)." % (
                        ch,
                        "%s:%s.%s" % (plutoGateway[ch]["unit_id"], plutoGateway[ch]["addr"], plutoGateway[ch]["bit"]),
                        ch_rbv, "%s:%s.%s" % (
                            plutoGateway[ch_rbv]["unit_id"], plutoGateway[ch_rbv]["addr"],
                            plutoGateway[ch_rbv]["bit"])))
                    return False

        self.step("All write adds are connected with the respective readback values addrs")
        return True


P4mA500 = 0
P20mA500 = 500  #psi
Pm500 = (P20mA500 - P4mA500) / (20 - 4)
Pb500 = P4mA500 - (4 * Pm500)
def c2P500(mA):
    psi = mA * Pm500 + Pb500
    return psi
def P2c500(psi):
    mA = (psi - Pb500) / Pm500
    mA = min(mA, 21.5)
    if mA < 3.5:
        mA = 21.5
    return mA

P4mA750 = 0
P20mA750 = 750  #psi
Pm750 = (P20mA750 - P4mA750) / (20 - 4)
Pb750 = P4mA750 - (4 * Pm750)
def c2P750(mA):
    psi = mA * Pm750 + Pb750
    return psi
def P2c750(psi):
    mA = (psi - Pb750) / Pm750
    mA = min(mA, 21.5)
    if mA < 3.5:
        mA = 21.5
    return mA


T2v = -50  #
T10v = 150  #C
Tm = (T10v - T2v) / (10 - 2)
Tb = T2v - (2 * Tm)

def v2C(v):
    C = v * Tm + Tb
    return C
def C2v(C):
    v = (C - Tb) / Tm
    v = min(v, 10.1)
    return v

CurT0v = 0  #A
Cur5v = 25  #A
Curm = (Cur5v - CurT0v) / (5 - 0)
Curb = CurT0v

def v2Cur(v):
    Cur = v * Curm + Curb
    return Cur
def Cur2v(Cur):
    v = (Cur - Curb) / Curm
    v = min(v, 10.1)
    return v


Volt0v = 0  #V
Volt5v = 250  #v
Voltm = (Volt5v - Volt0v) / (5 - 0)
Voltb = Volt0v

def v2Volt(v):
    Volt = v * Voltm + Voltb
    return Volt
def Volt2v(Volt):
    v = (Volt - Voltb) / Voltm
    v = min(v, 10.1)
    return v



def setDefautls(test,reset=True):
        self=test
        self.tester.testBox.plc.cryo_I30.write(1)
        self.tester.testBox.plc.cryo_I31.write(1)
        self.tester.testBox.plc.cryo_I32.write(1)
        self.tester.testBox.plc.cryo_I34.write(1)

        self.tester.testBox.plc.cryo_IA0.write(C2v(120))
        self.tester.testBox.plc.cryo_IA1.write(C2v(-10))
        self.tester.testBox.plc.cryo_IA5.write(2/16.0*10)

        self.tester.testBox.plc.cryo_IA3.write(P2c750(530))
        self.tester.testBox.plc.cryo_IA4.write(P2c500(430))

        self.tester.testBox.plc.cryo_IA7.write(Cur2v(2*3))
        self.tester.testBox.plc.cryo_IA6.write(Volt2v(230))


        self.tester.plutoGateway.CompIntPerm_w.write(1)
        self.tester.plutoGateway.HeaterIntPerm_w.write(1)
        self.tester.plutoGateway.LightsOn_w.write(1)

        if reset:
            self.tester.testBox.plc.cryo_I33.write(1)
            self.tester.plutoGateway.ResetGate_w.write(1)
            self.sleep(0.5)
            self.tester.testBox.plc.cryo_I33.write(0)
            self.tester.plutoGateway.ResetGate_w.write(0)

            self.tester.testBox.plc.cryo_I33.write(1)
            self.tester.plutoGateway.ResetGate_w.write(1)
            self.sleep(0.5)
            self.tester.testBox.plc.cryo_I33.write(0)
            self.tester.plutoGateway.ResetGate_w.write(0)


def checkDefautls(test):
    pass



class TestDigitalInputs(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDigitalInputs"
        self.desc = "TestDigitalInputs"

    def test(self):
        self.step(self.desc)

        setDefautls(self)
        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetModes = [True,False]

        ports = [self.tester.testBox.plc.cryo_I30,self.tester.testBox.plc.cryo_I31,self.tester.testBox.plc.cryo_I34]
        lacthOK =[self.tester.plutoGateway.AfterCoolerOKLatch, self.tester.plutoGateway.ExtPermLatch,self.tester.plutoGateway.SmokeOKLatch]
        lacthStatus = [self.tester.plutoGateway.AfterCoolerOKLatchStatus,self.tester.plutoGateway.ExtPermLatchStatus,self.tester.plutoGateway.SmokeOKLatchStatus]
        latchStatusNeedsReset =[self.tester.plutoGateway.AfterCoolerOKLatchNeedsReset,self.tester.plutoGateway.ExtPermLatchNeedsReset,self.tester.plutoGateway.SmokeOKLatchNeedsReset]

        self.tester.testBox.plc.cryo_IA0v.write(0)
        self.tester.testBox.plc.cryo_IA1v.write(0)
        self.tester.testBox.plc.cryo_IA5v.write(0)
        self.tester.testBox.plc.cryo_IA6v.write(0)
        self.tester.testBox.plc.cryo_IA7v.write(0)


        try:

            for resetMode in resetModes:
                for i, port in enumerate(ports):

                    port.write(0)

                    self.sleep(0.5)

                    self.pressChannels([reset])

                    self.checkChange([(port, 0),
                                      (permit, 0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],1),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)


                    port.write(1)

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],2),
                                      (latchStatusNeedsReset[i],1)
                                      ],
                                     3)

                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])

                    checkDefautls(self)

        except Exception as e:
            self.step("fail." + str(e))
            return False

        ports = [self.tester.testBox.plc.cryo_I32]  # ,self.tester.plutoGateway.CompIntPerm]

        try:

            for i, port in enumerate(ports):

                port.write(0)

                self.sleep(0.5)

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, 0),
                                  (permit, 0),
                                  ],
                                 3)

                port.write(1)
                checkDefautls(self)


        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False


        return True

class TestDigitalInputsHeater(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDigitalInputsHeater"
        self.desc = "TestDigitalInputsHeater"

    def test(self):
        self.step(self.desc)

        setDefautls(self)
        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        heatPermit = self.tester.testBox.plc.cryo_Q1
        resetModes = [True,False]

        key = self.tester.testBox.plc.cryo_I32

        ports = [self.tester.testBox.plc.cryo_I34]
        lacthOK =[self.tester.plutoGateway.SmokeOKLatch]
        lacthStatus = [self.tester.plutoGateway.SmokeOKLatchStatus]
        latchStatusNeedsReset =[self.tester.plutoGateway.SmokeOKLatchNeedsReset]

        self.tester.testBox.plc.cryo_IA0v.write(0)
        self.tester.testBox.plc.cryo_IA1v.write(0)
        self.tester.testBox.plc.cryo_IA5v.write(0)
        self.tester.testBox.plc.cryo_IA6v.write(0)
        self.tester.testBox.plc.cryo_IA7v.write(0)


        try:

            for resetMode in resetModes:
                for i, port in enumerate(ports):

                    self.tester.plutoGateway.CompIntPerm_w.write(0)

                    port.write(0)

                    self.sleep(0.5)

                    self.pressChannels([reset])

                    self.checkChange([(port, 0),
                                      (permit, 0),
                                      (heatPermit,0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],1),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)


                    port.write(1)

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (heatPermit,0),
                                      (lacthOK[i],0),
                                      (lacthStatus[i],2),
                                      (latchStatusNeedsReset[i],1)
                                      ],
                                     3)
                    self.sleep(2)

                    if resetMode:
                        self.pressChannels([reset], time=1)
                    else:
                        self.pressChannels([soft_reset])

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (heatPermit, 1),
                                      (lacthOK[i],1),
                                      (lacthStatus[i],0),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)

                    key.write(0)

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (heatPermit, 0),
                                      (lacthOK[i],1),
                                      (lacthStatus[i],0),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)
                    key.write(1)

                    self.tester.plutoGateway.CompIntPerm_w.write(1)

                    self.checkChange([(port, 1),
                                      (permit, 1),
                                      (heatPermit, 0),
                                      (lacthOK[i],1),
                                      (lacthStatus[i],0),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)

                    key.write(0)

                    self.checkChange([(port, 1),
                                      (permit, 0),
                                      (heatPermit, 0),
                                      (lacthOK[i],1),
                                      (lacthStatus[i],0),
                                      (latchStatusNeedsReset[i],0)
                                      ],
                                     3)

                    key.write(1)

        except Exception as e:
            self.step("fail." + str(e))
            return False

        ports = [self.tester.testBox.plc.cryo_I32]  # ,self.tester.plutoGateway.CompIntPerm]

        try:

            for i, port in enumerate(ports):

                port.write(0)

                self.sleep(0.5)

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, 0),
                                  (permit, 0),
                                  ],
                                 3)

                port.write(1)
                checkDefautls(self)


        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False


        return True


class TestSensorsValid(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestSensorsValid"
        self.desc = "TestSensorsValid"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        heatPermit = self.tester.testBox.plc.cryo_Q1
        resetMode = True

        sensorValidLatch = self.tester.plutoGateway.SensorsValidLatch
        sensorValidLatchStatus = self.tester.plutoGateway.SensorsValidLatchStatus
        sensorValidLatchNeedsReset = self.tester.plutoGateway.SensorsValidLatchNeedsReset

        ports =  [self.tester.testBox.plc.cryo_IA0,self.tester.testBox.plc.cryo_IA1,self.tester.testBox.plc.cryo_IA5,self.tester.testBox.plc.cryo_IA3,self.tester.testBox.plc.cryo_IA6]
        invalidVals=[1,1,0,1,0]
        valids = [self.tester.plutoGateway.DisTempValid,self.tester.plutoGateway.SucTempValid,self.tester.plutoGateway.OilLevelValid,self.tester.plutoGateway.DisPressValid,self.tester.plutoGateway.VoltageValid]
        #notvalids = [self.tester.testBox.plc.cryo_IA0v,self.tester.testBox.plc.cryo_IA1v,self.tester.testBox.plc.cryo_IA5v,None,self.tester.testBox.plc.cryo_IA6v]

        lacthOK =[self.tester.plutoGateway.DisTempOKLatch,self.tester.plutoGateway.SucTempOKLatch,self.tester.plutoGateway.OilLevelOKLatch,self.tester.plutoGateway.DisPressOKLatch,self.tester.plutoGateway.PowerOKLatch]
        lacthStatus = [self.tester.plutoGateway.DisTempOKLatchStatus,self.tester.plutoGateway.SucTempOKLatchStatus,self.tester.plutoGateway.OilLevelOKLatchStatus,self.tester.plutoGateway.DisPressOKLatchStatus,self.tester.plutoGateway.PowerOKLatchStatus]
        latchStatusNeedsReset =[self.tester.plutoGateway.DisTempOKLatchNeedsReset,self.tester.plutoGateway.SucTempOKLatchNeedsReset,self.tester.plutoGateway.OilLevelOKLatchNeedsReset,self.tester.plutoGateway.DisPressOKLatchNeedsReset,self.tester.plutoGateway.PowerOKLatchNeedsReset]

        try:
            for i, port in enumerate(ports):

                port.write(invalidVals[i])

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],0),
                                  (permit, 0),
                                  (heatPermit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,1),
                                  (sensorValidLatchNeedsReset, 0),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 1),
                                  (latchStatusNeedsReset[i], 0),
                                  ],
                                 3)

                self.tester.plutoGateway.CompIntPerm_w.write(0)

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],0),
                                  (permit, 0),
                                  (heatPermit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,1),
                                  (sensorValidLatchNeedsReset, 0),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 1),
                                  (latchStatusNeedsReset[i], 0),
                                  ],
                                 3)

                setDefautls(self,reset=False)

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],1),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,2),
                                  (sensorValidLatchNeedsReset, 1),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 2),
                                  (latchStatusNeedsReset[i], 1),
                                  ],
                                 3)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode

                checkDefautls(self)

                continue #TODO

                if notvalids[i] is None:
                    continue

                notvalids[i].write(1)

                self.pressChannels([reset,soft_reset])

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],0),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,1),
                                  (sensorValidLatchNeedsReset, 0),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 1),
                                  (latchStatusNeedsReset[i], 0),
                                  ],
                                 3)

                notvalids[i].write(0)

                self.checkChange([(port, invalidVals[i]),
                                  (valids[i],1),
                                  (permit, 0),
                                  (sensorValidLatch,0),
                                  (sensorValidLatchStatus,2),
                                  (sensorValidLatchNeedsReset,1),
                                  (lacthOK[i],0),
                                  (lacthStatus[i], 2),
                                  (latchStatusNeedsReset[i], 1),
                                  ],
                                 3)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode=not resetMode

                checkDefautls(self)

        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False

        return True


class TestImmediateTrips(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestImmediateTrips"
        self.desc = "TestImmediateTrips"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True


        try:


            port = self.tester.testBox.plc.cryo_IA0
            valid = self.tester.plutoGateway.DisTempValid
            warn = self.tester.plutoGateway.DisTempWarn
            lacthOK = self.tester.plutoGateway.DisTempOKLatch
            lacthStatus = self.tester.plutoGateway.DisTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.DisTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.DisTemp

            vals = np.arange(1.6, 10, 0.3)

            for val in vals:
                if abs(v2C(val) - 130)<0.5 or abs(v2C(val) - 125)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = val > C2v(130)
                warning = val > C2v(125)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (warn, warning),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode


            # discharge pressure is OK (<=540)

            port = self.tester.testBox.plc.cryo_IA3
            valid = self.tester.plutoGateway.DisPressValid
            warn = self.tester.plutoGateway.DisPressWarn
            lacthOK = self.tester.plutoGateway.DisPressOKLatch
            lacthStatus = self.tester.plutoGateway.DisPressOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.DisPressOKLatchNeedsReset
            press = self.tester.plutoGateway.DisPress

            vals = np.arange(4, 20, 0.6)

            for val in vals:
                if abs(c2P750(val) - 540) < 0.5 or abs(c2P750(val)) < 100:
                    continue

                port.write(val)

                print(c2P750(val) * 10)

                pressVal = int(c2P750(val) * 10)
                if pressVal < 0:
                    pressVal = 65535 + pressVal

                print(pressVal)

                trip = val >= P2c750(540)


                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (lacthOK, not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (press, pressVal)], 3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode

            #the suction temperature is OK (>-30C)

            port = self.tester.testBox.plc.cryo_IA1
            valid = self.tester.plutoGateway.SucTempValid
            lacthOK = self.tester.plutoGateway.SucTempOKLatch
            lacthStatus = self.tester.plutoGateway.SucTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.SucTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.SucTemp

            vals = np.arange(1.6, 10, 0.3)


            for val in vals:
                if abs(v2C(val) +13)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = v2C(val) <-13
                print(trip)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode



            # The compressor oil level is OK. (>1/16 full)

            port = self.tester.testBox.plc.cryo_IA5
            valid = self.tester.plutoGateway.OilLevelValid
            lacthOK = self.tester.plutoGateway.OilLevelOKLatch
            lacthStatus = self.tester.plutoGateway.OilLevelOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.OilLevelOKLatchNeedsReset
            level = self.tester.plutoGateway.OilLevel

            vals = np.arange(0.2, 10, 0.3)

            for val in vals:
                if abs((val) -0.6) < 0.1:
                    continue

                port.write(val)


                levelVal = val *1000

                print(levelVal)

                trip = val < 0.6
                print(trip)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (permit, not trip),
                                  (lacthOK, not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (level, levelVal)], 3)

                if trip:
                    setDefautls(self, reset=False)
                    self.checkChange([(permit, not trip),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode


        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True

class TestImmediateTripsHeater(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestImmediateTripsHeater"
        self.desc = "TestImmediateTripsHeater"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        heatPermit = self.tester.testBox.plc.cryo_Q1
        resetMode = True


        try:

            self.tester.plutoGateway.CompIntPerm_w.write(0)


            port = self.tester.testBox.plc.cryo_IA0
            valid = self.tester.plutoGateway.DisTempValid
            warn = self.tester.plutoGateway.DisTempWarn
            lacthOK = self.tester.plutoGateway.DisTempOKLatch
            lacthStatus = self.tester.plutoGateway.DisTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.DisTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.DisTemp

            vals = np.arange(1.6, 10, 0.3)

            for val in vals:
                if abs(v2C(val) - 130)<0.5 or abs(v2C(val) - 125)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = val > C2v(130)
                warning = val > C2v(125)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (heatPermit, not trip),
                                  (permit, 0),
                                  (warn, warning),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.tester.plutoGateway.CompIntPerm_w.write(0)
                    self.checkChange([(heatPermit, not trip),
                                  (permit, 0),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode


            #the suction temperature is OK (>-30C)

            port = self.tester.testBox.plc.cryo_IA1
            valid = self.tester.plutoGateway.SucTempValid
            lacthOK = self.tester.plutoGateway.SucTempOKLatch
            lacthStatus = self.tester.plutoGateway.SucTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.SucTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.SucTemp

            vals = np.arange(1.6, 10, 0.3)


            for val in vals:
                if abs(v2C(val) +13)<0.5 or abs(v2C(val))<10:
                    continue

                port.write(val)

                print(v2C(val)*100)

                tempVal = int(v2C(val)*100)
                if tempVal<0:
                    tempVal = 65535+tempVal

                print(tempVal)

                trip = v2C(val) <-13
                print(trip)

                self.pressChannels([reset, soft_reset])

                self.checkChange([(port, val),
                                  (valid, True),
                                  (heatPermit, not trip),
                                  (permit, 0),
                                  (lacthOK,not trip),
                                  (lacthStatus, trip),
                                  (latchStatusNeedsReset, 0),
                                  (temp, tempVal)],3)

                if trip:
                    setDefautls(self, reset=False)
                    self.tester.plutoGateway.CompIntPerm_w.write(0)
                    self.checkChange([
                                        (heatPermit, not trip),
                                        (permit, 0),
                                      (warn, 0),
                                      (lacthOK, 0),
                                      (lacthStatus, 2),
                                      (latchStatusNeedsReset, 1),
                                      ], 3)
                    if resetMode:
                        self.pressChannels([reset])
                    else:
                        self.pressChannels([soft_reset])
                    resetMode = not resetMode




        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True

voltage_correction = 1.008
voltage_correction = 1.012

class TestImmediatePowerTrips(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestImmediatePowerTrips"
        self.desc = "TestImmediatePowerTrips"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True

        try:


            #the compressor power is OK - (<2500 VA AND <1800 (wait 5 min))

            port = self.tester.testBox.plc.cryo_IA6
            valid = self.tester.plutoGateway.VoltageValid
            warn = self.tester.plutoGateway.PowerBadWarn
            lacthOK = self.tester.plutoGateway.PowerOKLatch
            lacthStatus = self.tester.plutoGateway.PowerOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.PowerOKLatchNeedsReset
            voltage = self.tester.plutoGateway.Voltage

            vals = np.arange(1, 10, 0.6)


            port2 = self.tester.testBox.plc.cryo_IA7
            valid2 = self.tester.plutoGateway.CurrentValid

            curent = self.tester.plutoGateway.Current


            currentVoltage = self.tester.plutoGateway.CurrentVolt
            voltageVoltage = self.tester.plutoGateway.VoltageVolt

            vals2 = np.arange(1, 10, 0.7)




            for val in vals:
                for val2 in vals2:

                    if abs(v2Volt(val) * v2Cur(val2) - 2500) < 100 or abs(v2Volt(val) * v2Cur(val2) - 1800) < 100:
                        continue


                    port.write(val*voltage_correction)
                    port2.write(val2*voltage_correction)
                    
                    self.sleep(.5)

                    print('-------------')
                    print(v2Volt(val),voltage.read()/10, '--', val , voltageVoltage.read())
                    print(v2Cur(val2), curent.read()/100, '--', val2, currentVoltage.read())
                    print(v2Volt(val) * v2Cur(val2),voltage.read()/10 *curent.read()/100 )
                    print('-------------')

                    trip = v2Volt(val) * v2Cur(val2) > 2500
                    warning = v2Volt(val) * v2Cur(val2) > 1800

                    self.pressChannels([reset, soft_reset])

                    self.checkChange([(port, val),
                                      (port2, val2),
                                      (valid, True),
                                      (valid2, True),

                                      (permit, not trip),
                                      (warn, warning),
                                      (lacthOK,not trip),
                                      (lacthStatus, trip),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ],5)

                    if trip:
                        setDefautls(self,reset=False)

                        self.checkChange([(permit, not trip),
                                          (warn, 0),
                                          (lacthOK, 0),
                                          (lacthStatus, 2),
                                          (latchStatusNeedsReset, 1),
                                          ], 5)

                        if resetMode:
                            self.pressChannels([reset])
                        else:
                            self.pressChannels([soft_reset])
                        resetMode = not resetMode

                        print('end')





        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True


class TestCurrentValid(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestCurrentValid"
        self.desc = "Test current valid"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True

        sensorValidLatch = self.tester.plutoGateway.SensorsValidLatch
        sensorValidLatchStatus = self.tester.plutoGateway.SensorsValidLatchStatus
        sensorValidLatchNeedsReset = self.tester.plutoGateway.SensorsValidLatchNeedsReset

        try:

            setDefautls(self)
            self.sleep(1)

            self.tester.testBox.plc.cryo_IA7.write(0)

            self.checkDuring([(permit, 1),(sensorValidLatch,1)], 133 + 15)
            print("passou o tempo")


            self.checkChange([(permit, 0),
                              (sensorValidLatch,0),
                              (sensorValidLatchStatus,1),
                              (sensorValidLatchNeedsReset, 0),
                              (self.tester.plutoGateway.PowerOKLatch,0),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 1),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 0),
                              ],
                             30)

            setDefautls(self,reset=False)

            self.checkChange([(permit, 0),
                              (sensorValidLatch,0),
                              (sensorValidLatchStatus,2),
                              (sensorValidLatchNeedsReset, 1),
                              (self.tester.plutoGateway.PowerOKLatch,0),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 2),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 1),
                              ],
                             3)

            if resetMode:
                self.pressChannels([reset])
            else:
                self.pressChannels([soft_reset])
            resetMode = not resetMode

            checkDefautls(self)

            #no problem

            setDefautls(self)

            self.checkDuring([(permit, 1)], 133+20)

            print("passou o tempo")

            '''self.checkChange([(self.tester.plutoGateway.CurrentValid,1),
                              (permit, 1),
                              (sensorValidLatch,1),
                              (sensorValidLatchStatus,0),
                              (sensorValidLatchNeedsReset, 0),
                              (self.tester.plutoGateway.PowerOKLatch,1),
                              (self.tester.plutoGateway.PowerOKLatchStatus, 0),
                              (self.tester.plutoGateway.PowerOKLatchNeedsReset, 0),
                              ],
                             20)'''

            checkDefautls(self)




        except Exception as e:
            self.step("TestDigitalInputs failed." + str(e))
            return False

        return True


class TestDelayPowerTrip(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelayPowerTrip"
        self.desc = "TestDelayPowerTrip"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True

        try:

            #the compressor power is OK - (<2500 VA AND <1800 (wait 5 min))

            port = self.tester.testBox.plc.cryo_IA6
            valid = self.tester.plutoGateway.VoltageValid
            warn = self.tester.plutoGateway.PowerBadWarn
            lacthOK = self.tester.plutoGateway.PowerOKLatch
            lacthStatus = self.tester.plutoGateway.PowerOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.PowerOKLatchNeedsReset
            voltage = self.tester.plutoGateway.Voltage

            vals = [4.6]


            port2 = self.tester.testBox.plc.cryo_IA7
            valid2 = self.tester.plutoGateway.CurrentValid

            curent = self.tester.plutoGateway.Current

            vals2 = [0.70]




            for val in vals:
                for val2 in vals2:

                    print(v2Volt(val), 'V')
                    print(v2Cur(val2), 'A')

                    print(v2Volt(val) * v2Cur(val2))


                    port.write(val)
                    port2.write(val2)

                    trip = v2Volt(val) * v2Cur(val2) > 2500
                    warning = v2Volt(val) * v2Cur(val2) > 1800

                    self.pressChannels([reset, soft_reset])

                    self.checkChange([(port, val),
                                      (port2, val2),
                                      (valid, True),
                                      (valid2, True),

                                      (permit, not trip),
                                      (warn, warning),
                                      (lacthOK,not trip),
                                      (lacthStatus, trip),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ],3)

                    self.checkDuring([(permit, 1), (lacthOK, 1)], 60*5-10)

                    self.checkChange([(port, val),
                                      (valid, True),
                                      (permit, not warning),
                                      (warn, 0),
                                      (lacthOK, not warning),
                                      (lacthStatus, warning),
                                      (latchStatusNeedsReset, 0),
                                      (voltage, v2Volt(val)*10),
                                      (curent, v2Cur(val2)*100)
                                      ], 30)

                    print('**********************************************************************************************')

                    if warning:
                        setDefautls(self,reset=False)

                        self.checkChange([(permit, 0),
                                          (warn, 0),
                                          (lacthOK, 0),
                                          (lacthStatus, 2),
                                          (latchStatusNeedsReset, 1)], 30)

                        if resetMode:
                            self.pressChannels([reset])
                        else:
                            self.pressChannels([soft_reset])
                        resetMode = not resetMode








        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True

class TestDelayDisTempTrip(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelayDisTempTrip"
        self.desc = "TestDelayDisTempTrip"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True


        try:
            #the discharge temperature is OK (<=130C AND <=125C(wait 30 min) )

            port = self.tester.testBox.plc.cryo_IA0
            valid = self.tester.plutoGateway.DisTempValid
            warn = self.tester.plutoGateway.DisTempWarn
            lacthOK = self.tester.plutoGateway.DisTempOKLatch
            lacthStatus = self.tester.plutoGateway.DisTempOKLatchStatus
            latchStatusNeedsReset =  self.tester.plutoGateway.DisTempOKLatchNeedsReset
            temp = self.tester.plutoGateway.DisTemp

            val = C2v(128)


            port.write(val)

            print(v2C(val)*100)

            tempVal = int(v2C(val)*100)

            trip = val > C2v(130)
            warning = val > C2v(125)


            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not trip),
                              (warn, warning),
                              (lacthOK,not trip),
                              (lacthStatus, trip),
                              (latchStatusNeedsReset, 0),
                              (temp, tempVal)],3)

            self.checkDuring([(permit, 1), (lacthOK, 1)], 60 * 30 - 10)

            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not warning),
                              (warn, 0),
                              (lacthOK,not warning),
                              (lacthStatus, warning),
                              (latchStatusNeedsReset, 0),
                              (temp, tempVal)],30)



            if warning:
                setDefautls(self, reset=False)

                self.checkChange([(permit, 0),
                                  (warn, 0),
                                  (lacthOK, 0),
                                  (lacthStatus, 2),
                                  (latchStatusNeedsReset, 1)], 30)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode





        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True


#test key


'''
class TestDelayDisPress(Test):
    def __init__(self, tester, id):
        Test.__init__(self, tester, id)
        self.name = "TestDelayDisPress"
        self.desc = "TestDelayDisPress"

    def test(self):
        self.step(self.desc)

        setDefautls(self)

        reset = self.tester.testBox.plc.cryo_I33
        soft_reset = self.tester.plutoGateway.ResetGate_w
        permit = self.tester.testBox.plc.cryo_Q0
        resetMode = True


        try:


            # discharge pressure is OK (<=465 psia AND, <=440 psia(wait 10 min))

            port = self.tester.testBox.plc.cryo_IA3
            valid = self.tester.plutoGateway.DisPressValid
            warn = self.tester.plutoGateway.DisPressWarn
            lacthOK = self.tester.plutoGateway.DisPressOKLatch
            lacthStatus = self.tester.plutoGateway.DisPressOKLatchStatus
            latchStatusNeedsReset = self.tester.plutoGateway.DisPressOKLatchNeedsReset
            press = self.tester.plutoGateway.DisPress

            val = P2c750(450)

            port.write(val)

            print(c2P750(val) * 10)

            pressVal = int(c2P750(val) * 10)

            print(pressVal)

            trip = val >= P2c750(465)
            warning = val >= P2c750(440)



            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not trip),
                              (warn, warning),
                              (lacthOK,not trip),
                              (lacthStatus, trip),
                              (latchStatusNeedsReset, 0),
                              (press, pressVal)],3)

            self.checkDuring([(permit, 1), (lacthOK, 1)], 60 * 10 - 10)

            self.checkChange([(port, val),
                              (valid, True),
                              (permit, not warning),
                              (warn, 0),
                              (lacthOK,not warning),
                              (lacthStatus, warning),
                              (latchStatusNeedsReset, 0),
                              (press, pressVal)],30)

            if warning:
                setDefautls(self, reset=False)

                self.checkChange([(permit, 0),
                                  (warn, 0),
                                  (lacthOK, 0),
                                  (lacthStatus, 2),
                                  (latchStatusNeedsReset, 1)], 30)

                if resetMode:
                    self.pressChannels([reset])
                else:
                    self.pressChannels([soft_reset])
                resetMode = not resetMode




        except Exception as e:
            self.step("TestImmediateTrips failed." + str(e))
            return False

        return True
'''