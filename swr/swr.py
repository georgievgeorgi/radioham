#!/usr/bin/python2
import serial
import time
import math
import numpy


power=5; ## watt


port = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=3.0)
#port = serial.Serial("/dev/pts/7", baudrate=4800, timeout=3.0)

rcv = port.read(999)

b160=numpy.linspace(  1810,  2000,10).astype(int)[1:-1]
b80 =numpy.linspace(  3500,  3800,12).astype(int)[1:-1]
b40 =numpy.linspace(  7000,  7200,10).astype(int)[1:-1]
b30 =numpy.linspace( 10100, 10150,10).astype(int)[1:-1]
b20 =numpy.linspace( 14000, 14350, 7).astype(int)[1:-1]
b17 =numpy.linspace( 18068, 18168, 7).astype(int)[1:-1]
b15 =numpy.linspace( 21000, 21450,10).astype(int)[1:-1]
b12 =numpy.linspace( 24890, 24990, 6).astype(int)[1:-1]
b10 =numpy.linspace( 28000, 29700,12).astype(int)[1:-1]
b6  =numpy.linspace( 50050, 50200,12).astype(int)[1:-1]
b2  =numpy.linspace(144000,146000,20).astype(int)[1:-1]
b_70=numpy.linspace(430000,440000,30).astype(int)[1:-1]
btest=numpy.linspace(1850,1860,1).astype(int)

for band_i in [b80]:
#for band_i in [[1850,3600,7100,10120,14150,18100,21200,24900,29000,50100]]:
#for band_i in [b2,b_70]:
    print("")
    for freq_i in band_i:
        cmd="FA%09d;" % (freq_i*1000)  ## Set Frequency in Hz
        #print("#freq   "+str(freq_i)+"kHz"+"   "+cmd)
        port.write(cmd)
        port.write("MD03;")   ## set mode to 3:cw-usb 5:AM
        port.write("PC%03d;" % (power))  ## set power to 5w
        if(freq_i<144000):port.write("AC000;")  ## switch off antenna tuner
        port.write("FA;") # get freq
        rcv = port.read(12)
        #print(rcv)
        freqkhz=float(rcv[2:11])/1000
        time.sleep(.3)
        swrarr=[]
        port.write("TX1;") ## TX ON
        for i in range(5):
            time.sleep(.1)
            port.write("RM6;") ## read SWR
            rcv = port.read(7)
            swrarr.append(float(rcv[3:6]))
        port.write("TX0;") ## TX OFF
        swrnat=numpy.array(swrarr).mean()
        swr=(math.log(342.483)-math.log(256-swrnat))/0.315294
        #swr=-math.log((256-swrnat)/359.232)/0.338092
        print(str(freqkhz)+"    "+"%.2f"%(swr)+"     "+str(swrnat))



print("#END");
port.close()
