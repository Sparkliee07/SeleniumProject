'''
Created on Dec 15, 2012

@author: Peter Reichert
'''

import sioApi as API

# Part numbers of all the SIOs
WD_SIO2_PART_NUMBER = "606-073-50"
WD_SIO4_PART_NUMBER0 = "619-975-50"
WD_SIO4_PART_NUMBER1 = "619-975-51"
WD_SIO5_PART_NUMBER0 = "222-605-21" # TODO: Temporary
WD_SIO5_PART_NUMBER1 = "622-212-50"
GUMSTICK_SIO2_PART_NUMBER = "606-073-60"
SEAGATE_SIO2_PART_NUMBER = "606-073-73"
TOSHIBA_SIO2_PART_NUMBER = "606-073-90"
HITACHI_SIO3_PART_NUMBER0 = "613-249-80"
HITACHI_SIO3_PART_NUMBER1 = "613-593-81"
HITACHI_LC_PART_NUMBER = "622-106-80"
HITACHI_HD_PART_NUMBER0 = "628-488-00"
HITACHI_HD_PART_NUMBER1 = "628-488-01"
QUALCOMM_TITAN_PART_NUMBER = "651-027-00"
QUALCOMM_MAGNUS_PART_NUMBER = "660-746-00"
QUALCOMM_MAGNUS_PART_NUMBER_PCA9554A = "689-241-00"
QUALCOMM_MAGNUS_PART_NUMBER_11 = "111-111-11"
QUALCOMM_MAGNUS_PART_NUMBER_01 = "660-746-01"
QUALCOMM_MAGNUS_PART_NUMBER_02 = "660-746-02"

# Variants
SEAGATE_VARIANT = "Seagate"
GUMSTICK_VARIANT = "Gumstick"
X261_VARIANT = "X261"
WD_VARIANT = "WD"
HITACHI_VARIANT = "Hitachi"
HITACHI_LC_VARIANT = "Hitachi_lc"
HITACHI_HD_VARIANT = "Hitachi_hd"
TOSHIBA_VARIANT = "Toshiba"
QUALCOMM_TITAN_VARIANT = "Qualcomm_Titan"
QUALCOMM_MAGNUS_VARIANT = "Qualcomm_Magnus"
UNKNOWN_VARIANT = "Unknown"

# Hardware
SIO2_BOARD = "SIO2"
SIO3_BOARD = "SIO3"
SIO4_BOARD = "SIO4"
SIO5_BOARD = "SIO5"
SIO6_BOARD = "SIO6"
RM2_BOARD = "RM2"
UNKNOWN_BOARD = "Unknown"

#Value keys.
KEY_PART_NUMBER = "SioPartNumber"
KEY_VARIANT = "SioVariant"
KEY_BOARD_TYPE = "SioBoardType"


FPGA_BASE = -805306368    # The binary representation of this is 0xd0000000
SLOTS_PER_FPGA = 35

FPGA_BLOCK_HDD_DATA = 0
FPGA_BLOCK_HDD_REGISTER = 1
FPGA_BLOCK_DIO_DATA = 2
FPGA_BLOCK_DIO_REGISTER = 3
FPGA_BLOCK_CHIP_LEVEL_REGISTER = 4

_seagateBaudRates = [9615, 19200, 37500, 38400, 57600, 75000, 115200, 375000,\
                   384000, 390000, 230400, 460800, 625000, 921600, 1228000]
_wdBaudRates = [115200, 117028, 208250, 1041000 ]
_toshibaBaudRates = [9600, 57600, 115200]
_hitachiBaudRates = [115200, 460800, 921600, 1843200, 2778000, 3333000, 4167000, 5556000, 8333000, 11111000, 16666000]
_gumstickBaudRates = [9615, 38400, 115200, 1250000]
_hitachiHdBaudRates = [115200,1843200]
_qualcommBaudRates = [115200]



class Sio(object):
    '''
    classdocs
    '''
    def __init__(self, protocol):
        '''
        Constructor
        '''
        self._protocol = protocol
        self.api = API.SioApi(self._protocol, 1)
        
    def __del__(self):
        '''
        Destructor
        '''

    def cleanup(self):
        if self.isDebug:
            print ("Deleting sio " , self._slotIdx)
        if hasattr(self, "log"):
            self.log.cleanup()
            del self.log
        if hasattr(self, "_protocol"):
            self._protocol.cleanup()
            del self._protocol
        
    

    def getValue(self, name):
        """
        This is brute force, meant to be analogous to the slot.getValue
        """
        if name == KEY_PART_NUMBER:
            return self._protocol.sioPartNumber
        
        elif name == KEY_VARIANT:
            return self._protocol.sioVariant

        elif name == KEY_BOARD_TYPE:
            return self._protocol.sioBoard
        
        else:
            return "Unknown"

    def isGumstickSio2(self):
        return (self._protocol.sioVariant == GUMSTICK_VARIANT) and (self._protocol.sioBoard == SIO2_BOARD)

    def isGumstickSio3(self):
        return (self._protocol.sioVariant == GUMSTICK_VARIANT) and (self._protocol.sioBoard == SIO3_BOARD)

    def isX261Sio2(self):
        return (self._protocol.sioVariant == X261_VARIANT) and (self._protocol.sioBoard == SIO2_BOARD)
        
    """
    Read back the variable "name" and compare it against value.
    If tolerance is specified, 'name' is tested to be within +/- tolerance 
    of 'value'
    """
    def testValue(self, name, value, result, tolerance=None):
        fail = False
        actual = self.getValue(name)
        if tolerance:
            if (actual > (value + tolerance)) or (actual < (value - tolerance)):
                fail = True
        else: 
            if value != actual: fail = True
        if fail:
            errString = 'Expect: %s, Actual: %s' % (value, str(actual))
            errLine = [name, errString]
            result.append(errLine)
        return result
        
        
            
    def getUpTime(self):
        result = self.api.TER_Debug(0)
        return result[1]
    

    def getFpgaAddress(self, block, slotIdx, register ):
        
        address = FPGA_BASE # Start with 0xd0000000
        
        if (slotIdx < 1) or (slotIdx > 140):
            return 0;

        # SIO2 or SIO3
        fpga = (slotIdx - 1) / SLOTS_PER_FPGA
        slotInFpga = (slotIdx - 1) % SLOTS_PER_FPGA
        
        if (block == FPGA_BLOCK_HDD_DATA) or (block == FPGA_BLOCK_DIO_DATA):
            register = 0
            
        if (block == FPGA_BLOCK_CHIP_LEVEL_REGISTER):
            slotInFpga = 0;    
        
        if self.getValue(KEY_BOARD_TYPE) == SIO4_BOARD:
            #SIO4
            return 0;
        else:
            
            address = address + (fpga * 0x2000000) + (block * 0x400000) + (slotInFpga * 0x10000) + (register * 0x1000)  
        
            return address
        
    def getBaudRates(self):
        variant = self._protocol.sioVariant
        
        if SEAGATE_VARIANT == variant:    
            return _seagateBaudRates
        elif HITACHI_VARIANT == variant:
            return _hitachiBaudRates
        elif WD_VARIANT == variant:
            return _wdBaudRates
        elif TOSHIBA_VARIANT == variant:
            return _toshibaBaudRates
        elif GUMSTICK_VARIANT == variant:
            return _gumstickBaudRates
        elif HITACHI_HD_VARIANT == variant:
            return _hitachiHdBaudRates
        elif QUALCOMM_TITAN_VARIANT == variant:
            return _qualcommBaudRates
        elif QUALCOMM_MAGNUS_VARIANT == variant:
            return _qualcommBaudRates
        else:
            print ("Unknown variant ", variant)
            return []
            
            

if __name__ == "__main__":
    #from Teradyne.cmLib.MRPCProtocol import MRPCProtocol
    from MRPCProtocol import MRPCProtocol
    protocol = MRPCProtocol()
    o = Sio(protocol)
    print ("Uptime = ", o.getUpTime())
    print ("SIO Part Number: ", o.getValue("SioPartNumber"))
    print ("SIO Variant: ", o.getValue("SioVariant"))
    print ("SIO Board Type: ", o.getValue("SioBoardType"))
    
    print ("HDD Data address slot 1: 0x%08x" % (o.getFpgaAddress(FPGA_BLOCK_HDD_DATA, 1, 17) & 0xffffffff,))
    print ("HDD Data address slot 35: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_DATA, 35, 17) & 0xffffffff,))
    print ("HDD Data address slot 36: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_DATA, 36, 17) & 0xffffffff,))
    print ("HDD Data address slot 140: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_DATA, 140, 17) & 0xffffffff,))
    print ("HDD Register, slot 1, register 2: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_REGISTER, 1, 2) & 0xffffffff,))
    print ("HDD Register, slot 35, register 2: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_REGISTER, 35, 2) & 0xffffffff,))
    print ("HDD Register, slot 36, register 2: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_REGISTER, 36, 2) & 0xffffffff,))
    print ("HDD Register, slot 140, register 2: 0x%08x" % ( o.getFpgaAddress(FPGA_BLOCK_HDD_REGISTER, 140, 2) & 0xffffffff,))
    
    print ("HDD Chip Level block register 2: 0x%08x" % (o.getFpgaAddress(FPGA_BLOCK_CHIP_LEVEL_REGISTER, 33, 2) & 0xffffffff,))
    print ("HDD Chip Level block register 2: 0x%08x" % (o.getFpgaAddress(FPGA_BLOCK_CHIP_LEVEL_REGISTER, 1, 2) & 0xffffffff,))
    
