#!/usr/bin/env python

# playbackTextFile.py
# 06-04-2018
# Permission is required, for a charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software")
# Please email contact@behindthesciences.com
# Copyrights www.behindthesciences.com 2019


import os
import sys
import time
import pigpio
import subprocess

from lib_CC1101_Test_100 import CC1101
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev
from time import sleep
import sys
import struct

bashCommand = "sudo pigpiod"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if len(sys.argv) != 3:
   print "Run program as: python playbackTextFileCC.py data.txt Freq"
   print "Replace data.txt with your own data file"
   print "Freq is either 433 or 315"


f = open(sys.argv[1], 'r')
i = 1
stamps = []
level = []
wf=[]
CC = CC1101(spidev.SpiDev())

CC.initCC(1)
PA_TABLE= [0x7E,0x00,0xC0,0x00,0x00,0x00,0x00,0x00,0x00]
CC._PA(PA_TABLE)
#Set Frequency
if sys.argv[2] == "315":
    CC._setFreq("FREQ_315")
if sys.argv[2] == "433":
    CC._setFreq("FREQ_433")
#SIDLE
CC._strobe(0x36)
#STX
CC._strobe(0x35)



GPIO = 5
for line in f:
    
    if line[0] != '#':
     fields = line.split()
     stamp = (int(float(fields[1])))
     levels = int(fields[0])
     print levels
     print stamp
     stamps.append(int(float(fields[1])))
     level.append(int(fields[0]))
     i = i+1
     

if level[0] > level[1]:
    on = 1<<GPIO
    off = 0
    print "True"
else:
    print "False"    
    on = 0
    off = 1<<GPIO
    


for item in stamps:
    wf.append(pigpio.pulse(on, off, (item)))
    last_stamp = item
    print item
    on_off = on
    on = off
    off = on_off


f.close()


pi = pigpio.pi() # Connect to local Pi.

if not pi.connected:
   exit()
pi.set_mode(GPIO, pigpio.OUTPUT) # Need to be outputs for wave to work




pi.wave_clear()
pi.wave_add_generic(wf)
print (pi.wave_add_generic(wf))
wid = pi.wave_create()


if wid >= 0:
   pi.wave_send_repeat(wid)

   while pi.wave_tx_busy():
      time.sleep(0.01)
      spot = raw_input("Enter Q to quit: ")
      if spot == "Q" or spot == "q":
                print "User Stopped"
                CC._strobe(0x36)
                pi.wave_tx_stop()
                pi.wave_delete(wid)
                pi.write(GPIO, 0)
                pi.stop()
                sys.exit(0)

   pi.wave_delete(wid)

pi.stop()


