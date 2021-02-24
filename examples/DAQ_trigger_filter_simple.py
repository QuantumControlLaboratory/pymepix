import pymepix
from pymepix.processing import MessageType
import numpy as np
import time
from enum import Enum,IntEnum

#Connect to SPIDR
timepix = pymepix.Pymepix(('192.168.100.10',50000), src_ip_port=('192.168.100.1', 0))

# # #Set bias voltage
timepix.biasVoltage = 40


timepix[0].loadConfig('configfile.spx')

TDC1_RE = 0x6f
TDC1_FE = 0x6a
TDC2_RE = 0x6e
TDC2_FE = 0x6b

spi = timepix._spidr

datasx = []
datasy = []
toas = []
trgs = []


num_triggers = 0
max_number_triggers = 20

current_max_time = 0
trigger_after_pixel = 0

trigger_sens = [TDC1_RE, TDC2_RE]
gate_times = [5e-3, 10e-3]

trigger_counter = TDC1_RE # trigger used for counting
triggers = []

#Define callback
def my_callback(data_type,data):
    global num_triggers, current_max_time, trigger_after_pixel

    if data_type is MessageType.RawData:
        pass
        ## somwhere the TDC2 triggers are not sens to MessageType.RawData: but the TDC1 are
    elif data_type is MessageType.TriggerData:
        #print("trigger: ", data)
        trgs.append(data)
        ttypes, trigs = data

        if min(trigs) < current_max_time:
            trigger_after_pixel += 1


        for typ, tim in zip(ttypes, trigs):
            if typ in trigger_sens:
                triggers.append([typ, tim])

        ## Just count trigger_counter Rising Edge
        num_triggers += len(ttypes[ttypes==trigger_counter])


    #Handle Pixels
    elif data_type is MessageType.PixelData:
        x,y,toa,tot = data
        
        mt = max(toa)
        if current_max_time < mt:
            current_max_time = mt

        #Filter pixel by trigger and gatetime
        idx = np.array([])
        for typ, trig in triggers:
            gate_time = gate_times[trigger_sens.index(typ)]

            i = np.where(np.logical_and(toa>=trig, toa<=trig+gate_time))
            idx = np.append(idx, [i])

        idx = np.uint64(np.unique(idx))
        if len(idx) > 0:
            datasx.extend(x[idx])
            datasy.extend(y[idx])
            toas.extend(toa[idx])

#Set callback
timepix.dataCallback = my_callback
timepix.start()

while num_triggers < max_number_triggers:
    time.sleep(0.1)
    print("Trigger: ", num_triggers, len(datasx), end="\r")
     


print("\n Finised ", num_triggers, trigger_after_pixel)

#Stop
timepix.stop()


print("Len ", len(toas))
x = np.array(datasx)
y = np.array(datasy)
t = np.array(toas)

print("sort")
inds = t.argsort()
t = t[inds]
x = x[inds]
y = y[inds]

trgdatas = []
for tdata in trgs:
    ttypes, trigs = tdata
    for trig, tty in zip(trigs, ttypes):
        if tty in trigger_sens:
            gate_time = gate_times[trigger_sens.index(tty)]
            idx = np.where(np.logical_and(t>=trig, t<=trig+gate_time))
            trgdatas.append([tty, trig, t[idx]-trig, x[idx], y[idx]])



print("pickle_data")

import pickle

pickle.dump(trgdatas, open( "datas_triggered.p", "wb" ) )

print("Wait for Exit...")
time.sleep(1)
print("Exit")
