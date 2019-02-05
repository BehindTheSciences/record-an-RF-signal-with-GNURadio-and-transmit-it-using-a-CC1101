# CC1101 Asynchronous Library    V3 March 2018     Akeel Auckloo
# 
# Permission is required, for a charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software")
# Please email contact@behindthesciences.com
# Copyrights www.behindthesciences.com 2019



import numbers
import time
import textwrap
import spidev

from types import MethodType

# CC1101 registers.
IOCFG2      = 0x00
IOCFG1      = 0x01
IOCFG0     = 0x02
IOCFG0A1    = 0x02
IOCFG0A2    = 0x02
FIFOTHR     = 0x03
PKTLEN      = 0x06
PKTCTRL1    = 0x07
PKTCTRL0    = 0x08
ADDR        = 0x09
CHANNR      = 0x0A
FSCTRL1     = 0x0B
FSCTRL0     = 0x0C
FREQ2       = 0x0D
FREQ1       = 0x0E 
FREQ0       = 0x0F
MDMCFG4     = 0x10
MDMCFG3     = 0x11
MDMCFG2     = 0x12
MDMCFG1     = 0x13
MDMCFG0     = 0x14
DEVIATN     = 0x15
MCSM2       = 0x16
MCSM1       = 0x17 
MCSM0       = 0x18
FOCCFG      = 0x19
BSCFG       = 0x1A 
AGCCTRL2    = 0x1B
AGCCTRL1    = 0x1C
AGCCTRL0    = 0x1D
WOREVT1     = 0x1E
WOREVT0     = 0x1F
WORCTRL     = 0x20
FREND1      = 0x21
FREND0      = 0x22
FSCAL3      = 0x23
FSCAL2      = 0x24 
FSCAL1      = 0x25
FSCAL0      = 0x26
RCCTRL1     = 0x27
RCCTRL0     = 0x28
FSTEST      = 0x29
PTEST       = 0x2A 
AGCTST      = 0x2B
TEST2       = 0x2C
TEST1       = 0x2D
TEST0       = 0x2E





class CC1101():
    def __init__(self, spi):
        self._spi = spi
        
    def _strobe(self, address):
        return self._spi.xfer([address, 0x00])
    
    def _writeSingleByte(self, address, byte_data):
        return self._spi.xfer([address, byte_data])
    def _readSingleByte(self, address):
        return self._spi.xfer([address, 0x00])[1]
        
    def _PA(self,data):
        return self._spi.xfer(data)
        
    def _setFreq(self, CFREQ):
        if CFREQ == "FREQ_433":
            VAL_FREQ2       = 0x10 
            VAL_FREQ1       = 0xB0 
            #VAL_FREQ0       = 0x71
            VAL_FREQ0       = 0xD6
            
        if CFREQ == "FREQ_315":
            #VAL_FREQ2       = 0x0C 
            #VAL_FREQ1       = 0x1D 
            #VAL_FREQ0       = 0x89
            VAL_FREQ2 = 0x0C
            VAL_FREQ1 = 0x1E
            VAL_FREQ0 = 0x2B
            
        if CFREQ == "FREQ_435":
            VAL_FREQ2       = 0x10 
            VAL_FREQ1       = 0xBB 
            VAL_FREQ0       = 0x13
            
            
        self._writeSingleByte(FREQ2   ,VAL_FREQ2)    
        self._writeSingleByte(FREQ1   ,VAL_FREQ1)    
        self._writeSingleByte(FREQ0   ,VAL_FREQ0) 
        
    def _getRSSI(self):    
        RSSI_dec = self._readSingleByte(0xF4)
        if RSSI_dec >= 128:
            RSSI_dBm =(RSSI_dec - 256)/2 - 79
        else:
            RSSI_dBm =(RSSI_dec)/2 - 79
        return RSSI_dBm
        
    def _initCC_RX(self):
        
        self._writeSingleByte(IOCFG2,0x4D)
        self._writeSingleByte(IOCFG0,0x0D)
        
        
        self._writeSingleByte(FIFOTHR,0x57)
        self._writeSingleByte(PKTCTRL0,0x32)
        self._writeSingleByte(FSCTRL1,0x06)
        self._writeSingleByte(MDMCFG4,0xC7)
        self._writeSingleByte(MDMCFG3,0x83)
        self._writeSingleByte(MDMCFG2,0x30)
        self._writeSingleByte(DEVIATN,0x40)
        self._writeSingleByte(MCSM0,0x18)
        self._writeSingleByte(FOCCFG,0x16)
        self._writeSingleByte(WORCTRL,0xFB)
        self._writeSingleByte(FREND1,0x56)
        self._writeSingleByte(FREND0,0x11)
        self._writeSingleByte(FSCAL3,0xE9)
        self._writeSingleByte(FSCAL2,0x2A)
        self._writeSingleByte(FSCAL1,0x00)
        self._writeSingleByte(FSCAL0,0x1F)
        self._writeSingleByte(TEST2,0x81)
        self._writeSingleByte(TEST1,0x35)
        self._writeSingleByte(TEST0,0x09)

        
        
        self._writeSingleByte(AGCCTRL0,0x92)
        #self._writeSingleByte(AGCCTRL0,0x93)
	self._writeSingleByte(AGCCTRL1,0x00)
        self._writeSingleByte(AGCCTRL2,0x06)
	#self._writeSingleByte(AGCCTRL2,0x07)
         
            
        
    def initCC(self, ce=0, spi_speed=2000000):
        
        self._ce = ce
        self._spi_speed=spi_speed
        self._spi.open(1,0)
        self._spi.max_speed_hz=self._spi_speed
        self._initCC_RX()


