#!/usr/bin/python2
import serial
import time
import math
import numpy


port = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=3.0)
rcv = port.read(999)

port.write("PC005;")  ## set power to 5w
port.write("MD03;")   ## set mode to 3:cw-usb 5:AM

b80=range(3500000,3800000,30000)
b40=range(7000000,7200000,20000)
b30=range(10100000,10150000,10000)
b20=range(14000000,14350000,30000)
b17=range(18068000,18168000,10000)
b15=range(21000000,21450000,50000)
b12=range(24890000,24990000,50000)
b10=range(28000000,29700000,100000)

for i in (b80+b40+b20+b17+b15+b12+b10):
    port.write("PC005;")  ## set power to 5w
    port.write("MD03;")   ## set mode to 3:cw-usb 5:AM
    cmd="FA%09d;" % (i)  ## Set Frequency in Hz
    #print("#freq   "+str(i/1000)+"kHz")
    port.write(cmd)
    port.write("FA;") # get freq
    rcv = port.read(12)
    #print(rcv)
    freqkhz=float(rcv[2:11])/1000

    time.sleep(.3)
    port.write("TX1;") ## TX ON
    swrarr=[]

    for i in range(5):
        time.sleep(.1)
        port.write("RM6;") ## read SWR
        rcv = port.read(7)
        swrarr.append((math.log(342.483)-math.log(255-float(rcv[3:6])))/0.315294)

    port.write("TX0;") ## TX OFF
    swr=numpy.array(swrarr).mean()

    print(str(freqkhz)+"    "+str(swr))



print("#END");
port.close()
