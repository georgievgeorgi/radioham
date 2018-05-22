#!/usr/bin/python2
import serial
import time
import math
import numpy


port = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=3.0)

port.close()
