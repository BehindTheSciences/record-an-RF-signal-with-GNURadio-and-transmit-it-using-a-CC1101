
#Opens a .wav file 
#Processes it
#Find Pulse Length
#Save it in a txt file
#
# Permission is required, for a charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software")
# Please email contact@behindthesciences.com
# Copyrights www.behindthesciences.com 2019

import wave
import time
import sys
import struct
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
#matplotlib.use('agg')

# Load the data and calculate the time of each sample


#from matplotlib import pyplot as plt
if len(sys.argv) != 3:
   print "Run program as: python OpenWav.py name.wav data.txt"
   print "Replace name and data with your own"



thefile = open(sys.argv[2], 'wb')

spf = wave.open(sys.argv[1], 'rb')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()
print "The median of the signal is:"
print np.median(signal)

signalL = signal.tolist()
#print ((max(signalL)-min(signalL))/2)
toggle = ((max(signalL)-min(signalL))/3)
for i in range (len(signalL)):
	if signalL[i] > toggle:    #####Need to be improved (perhaps using mean or median) replace by 3000 if this doesnt work
		signalL[i] = 1
	else:
		signalL[i] = 0

Time=np.linspace(0, len(signal)/fs, num=len(signal))
TimeL = Time.tolist()
t = 0
stamps = []
level = []
for x in range(len(signalL)-1):
	if signalL[x] != signalL[(x+1)]:
		stamps.append(round((TimeL[x]-t)*1000000)) #converts in us and then save in list
		level.append(signalL[x])
		t = TimeL[x]

for i in range(len(stamps)):
    	   thefile.write("%s\t%s\n" % ((level[i]),(stamps[i])))
thefile.close()

plt.figure(1)
plt.title('Fob')
plt.plot(TimeL,signalL) #Plot received signal.
plt.show()
