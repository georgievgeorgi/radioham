#!/usr/bin/python3

import serial
import time
import math
import numpy
import pandas
import matplotlib.pyplot as plt

class yaesu_com:


    def port(slef):
        return self.port

    def __init__(self, port, baudrate=4800):
        self.__connect(port, baudrate)

    def __del__(self):
        self.__disconnect()

    def __connect(self, port, baudrate):
        print("Connect")
        self.port = serial.Serial(port, baudrate=4800, timeout=3.0)

    def __disconnect(self):
        print("Disconnect")
        self.port.close()

    def __sleep(self):
        time.sleep(.2)

    def __sleep_tx(self): time.sleep(.025)
    def __sleep_rx(self): time.sleep(1e-5)

    def __flush(self):
        self.port.flushInput()
        self.port.flushOutput()

    def __write(self,cmd):
        cmd+=';'
        for i in cmd:
            self.__sleep_tx()
            self.port.write(i.encode())

    def _writef(self, cmd):
        self.__flush()
        self.__write(cmd)

    def __read(self):
        in_buff=b''
        self.__sleep()
        while self.port.in_waiting:
            in_buff+=self.port.read_all()    #read the contents of the buffer
            self.__sleep()
        print("READ: %s"%(in_buff))
        return in_buff

    def get_power(self):
        self._writef("PC")
        return int(self.__read()[2:-1])
    def set_power(self,v):
        self._writef("PC%03d"%(v))
    def get_frequency(self):
        self._writef("FA")
        return int(self.__read()[2:-1])
    def set_frequency(self): pass
    def get_swr(self):
        self._writef("RM6")
        return int(self.__read()[3:-1])
    def set_transmit_on(self):
        self._writef("TX1")
    def set_transmit_off(self):
        self._writef("TX0")
    def set_tuner_off(self):
        self._writef("AC000")
    def set_tuner_on(self):
        self._writef("AC001")
    def set_tuner_start_tunning(self):
        self._writef("AC002")
    def set_mode_cwusb(self):
        self._writef("MD03")
    def test(self):
        self.swr_scan( 7010000)
        f=self.get_frequency()
    def swr_measure(self,hertz,power=10):
        swrarr=[]
        self.set_frequency(hertz)
        self.set_mode_cwusb()
        self.set_power(10)
        if(hertz<60000000):self.set_tuner_off()
        self.set_transmit_on()
        for i in range(5):
            #time.sleep(.1)
            swrarr+=[self.get_swr()]
        self.set_transmit_off()
        swrnat=numpy.array(swrarr).mean()
        swr=(math.log(342.483)-math.log(256-swrnat))/0.315294
        f=self.get_frequency()
        return {'freq':f, 'swr':swr, 'swr255':swrnat}

    def swr_scan(self,hertz,power=10):
        if hasattr(hertz,"__len__"):
            return [self.swr_measure(f,power) for f in hertz]
        else:
            return [self.swr_measure(hertz,power)]

    def swr_scan_band_160m(self,npoints= 8,power=10): return self.swr_scan(numpy.linspace(  1810e3,  2000e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_80m (self,npoints=10,power=10): return self.swr_scan(numpy.linspace(  3500e3,  3800e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_40m (self,npoints=10,power=10): return self.swr_scan(numpy.linspace(  7000e3,  7200e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_30m (self,npoints= 8,power=10): return self.swr_scan(numpy.linspace( 10100e3, 10150e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_20m (self,npoints= 5,power=10): return self.swr_scan(numpy.linspace( 14000e3, 14350e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_17m (self,npoints= 5,power=10): return self.swr_scan(numpy.linspace( 18068e3, 18168e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_15m (self,npoints= 8,power=10): return self.swr_scan(numpy.linspace( 21000e3, 21450e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_12m (self,npoints= 4,power=10): return self.swr_scan(numpy.linspace( 24890e3, 24990e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_10m (self,npoints=10,power=10): return self.swr_scan(numpy.linspace( 28000e3, 29700e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_6m  (self,npoints=10,power=10): return self.swr_scan(numpy.linspace( 50050e3, 50200e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_2m  (self,npoints=18,power=10): return self.swr_scan(numpy.linspace(144000e3,146000e3,npoints+2).astype(int)[1:-1],power)
    def swr_scan_band_70cm(self,npoints=28,power=10): return self.swr_scan(numpy.linspace(430000e3,440000e3,npoints+2).astype(int)[1:-1],power)



class ft450d(yaesu_com):
    def set_frequency(self,v):
        super()._writef("FA%08d"%(v))

class ft991a(yaesu_com):
    def set_frequency(self,v):
        super()._writef("FA%09d"%(v))


def swrplot(inp, plotfile='',datafile='',):
    if len(datafile)>0:
        pandas.DataFrame(swr,columns=['freq','swr','swr255']).to_csv(datafile,sep=',')

    if len(plotfile)<1:
        return

    f=[i['freq']/1e6 for i in inp]
    s=[i['swr'] for i in inp]

    plots,subplots=plt.subplots(1,12,sharey=True, facecolor='w')
    plots.set_size_inches(25,8)

    subplots[ 0].set_xlim(  1810e-3,  2000e-3)#160m
    subplots[ 1].set_xlim(  3500e-3,  3800e-3)#80m
    subplots[ 2].set_xlim(  7000e-3,  7200e-3)#40m
    subplots[ 3].set_xlim( 10100e-3, 10150e-3)#30m
    subplots[ 4].set_xlim( 14000e-3, 14350e-3)#20m
    subplots[ 5].set_xlim( 18068e-3, 18168e-3)#17m
    subplots[ 6].set_xlim( 21000e-3, 21450e-3)#15m
    subplots[ 7].set_xlim( 24890e-3, 24990e-3)#12m
    subplots[ 8].set_xlim( 28000e-3, 29700e-3)#10m
    subplots[ 9].set_xlim( 50050e-3, 50200e-3)#6m
    subplots[10].set_xlim(144000e-3,146000e-3)#2m
    subplots[11].set_xlim(430000e-3,440000e-3)#70cm

    subplots[ 0].set_title ("160m")
    subplots[ 1].set_title ("80m ")
    subplots[ 2].set_title ("40m ")
    subplots[ 3].set_title ("30m ")
    subplots[ 4].set_title ("20m ")
    subplots[ 5].set_title ("17m ")
    subplots[ 6].set_title ("15m ")
    subplots[ 7].set_title ("12m ")
    subplots[ 8].set_title ("10m ")
    subplots[ 9].set_title ("6m  ")
    subplots[10].set_title ("2m  ")
    subplots[11].set_title ("70cm")

    for sp in subplots:
        sp.set_yscale('log')
        sp.grid(axis='both')
        ylabels=[1,1.1,1.2,1.5,2,3,4,5,6,7,8,9,10,15,20,30,40,50]
        sp.set_yticks(ylabels)
        sp.set_yticklabels(ylabels)
        sp.set_ylim(0.9,10)
        plt.setp(sp.xaxis.get_majorticklabels(), rotation=60)
        sp.plot(f,s,'r+-')
    plt.savefig(plotfile, bbox_inches='tight')

if __name__ == "__main__":
    #m = ft450d('/dev/ttyUSB0')
    m = ft991a('/dev/ttyUSB0')
    #m.test()
    swr=[]
    #swr+=m.swr_scan_band_160m()
    #swr+=m.swr_scan_band_80m ()
    #swr+=m.swr_scan_band_40m ()
    #swr+=m.swr_scan_band_30m ()
    swr+=m.swr_scan_band_20m ()
    #swr+=m.swr_scan_band_17m ()
    #swr+=m.swr_scan_band_15m ()
    #swr+=m.swr_scan_band_12m ()
    #swr+=m.swr_scan_band_10m ()
    #swr+=m.swr_scan_band_6m  ()
    #swr+=m.swr_scan_band_2m  ()
    #swr+=m.swr_scan_band_70cm()
    #sorted(swr, key=itemgetter('freq'))
    swrplot(swr,plotfile='plot.pdf',datafile='data.csv')

