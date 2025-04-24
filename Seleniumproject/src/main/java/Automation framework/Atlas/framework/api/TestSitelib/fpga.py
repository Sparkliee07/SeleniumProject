'''
Created on Jul 13, 2016

@author: reichert
'''
import ctypes
import math
import time
from sio import Sio as SIO
import sio as sio
import sioApi as API
import struct
import MRPCProtocol

fpgaBase = -805306368    # The binary representation of this is 0xd0000000
spartanBase = 0xC0000000

MAX_JTAG_CLOCK_DIVIDER = 63
MIN_JTAG_CLOCK_DIVIDER = 2
JTAG_BASE_CLOCK = 50e6

def reverseCharOrder( input ):
    length = len(input)
    output = ""
    for i in range(length):
        output += ( input[(length-1) - i] )
    return output

class Fpga():
    '''
    classdocs
    Interesting shenanigans: The CmdLineClient -s slot option must be a legal
    slot, but the Fpga class may be declared with a different slot.  This supports the
    case where we use different FPGA channels for different functions.
    '''

    themisRegisterBlockDict = {
                              "hdd_urb" :  0 * 0x00200000,
                              "fpUart"  :  3 * 0x00200000,
                              "clrb"     : 4 * 0x00200000,
                              "jtag"     : 5 * 0x00200000,
                              "spi"      : 6 * 0x00200000,
                              "comm_urb" : 0x00200000,  # Not used
                              }

    atlasRegisterBlockDict = {
                              "hdd_urb"  : 0x01000000,
                              "comm_urb" : 0x00000000,
                              "clrb"     : 0x04000000,
                              "jtag"     : 0x05000000,
                              "spi"      : 0x06000000}

    # SIO2 & 3:
    sio2RegisterBlockDict = {
                             "hdd_urb"  : 0x00400000,
                             "comm_urb" : 0x00c00000,
                             "clrb"     : 0x01000000}
        


    def __init__(self, slotid, protocol, boardType=None, isDebug=True):
        '''
        Constructor
        '''
        self.slotid = slotid
        self.protocol = protocol
        self.isDebug = isDebug
        if boardType:
            self.sioBoard = boardType
        else:
            self.sioBoard = self.protocol.sioBoard

        self.api = API.SioApi(self.protocol, 1)   # For FPGA operations, slot index doesn't matter.
        
        if (self.sioBoard == sio.SIO4_BOARD) or (self.sioBoard == sio.SIO5_BOARD):
            self.printDebug ("SIO4 or SIO5")
            self.chipFactor = 0x00000000
            self.slotFactor = 0x00040000
            self.registerFactor = 0x1000
            self.rbDict     = self.atlasRegisterBlockDict
        elif (self.sioBoard == sio.SIO2_BOARD) or (self.sioBoard == sio.SIO3_BOARD):
            self.printDebug("SIO2 or SIO3")
            self.chipFactor = 0x02000000
            self.slotFactor = 0x00010000
            self.registerFactor = 0x1000            
            self.rbDict     = self.sio2RegisterBlockDict
        else:
            self.printDebug("SIO6")
            self.chipFactor = 0x00000000
            self.slotFactor = 0x00040000
            self.registerFactor = 0x1000
            self.rbDict     = self.themisRegisterBlockDict

    def __del__(self):
        del self.protocol

    def printDebug(self, msg0, msg1=None):
        if self.isDebug:
            print (msg0, msg1)

    def buildBaseAddress(self, registerBlock, chipNum=0 ):
        return self.rbDict[registerBlock] + (chipNum * self.chipFactor) + (self.slotid * self.slotFactor)
            

    def buildAddress(self, registerBlock, registerNum, chipNum=0 ):
        return self.buildBaseAddress( registerBlock, chipNum) + (registerNum * self.registerFactor)
    
    def readRegister(self, registerBlock, registerNum, chipNum=0):      
        address = self.buildAddress( registerBlock, registerNum, chipNum)
        result = self.api.TER_ReadFpgaRegisters( (1, fpgaBase + address,) )
        self.printDebug ("read address = 0x%08x = 0x%08x" % (address, result[1] & 0xffffffff))
        return result[1]

    def writeRegister(self, registerBlock, registerNum, value, chipNum=0):      
        address = self.buildAddress( registerBlock, registerNum, chipNum)
        cvalue = ctypes.c_int( value ) 
        self.printDebug( "write address = 0x%08x = 0x%08x" % (address, cvalue.value & 0xffffffff))
        result = self.api.TER_WriteFpgaRegisters( (1, fpgaBase + address, cvalue.value, ) )

    def addressToString(self, address):
        return   "0x%08x" % (address & 0xffffffff)
    
    
    """
    VERSION 2:
    There is a new FPGA image in \\pelican\projects\Atbone\Hardware.  
    It is version 1.1.  I expanded the data length to 4 bits and added the 
    lengths that I think they will require.  The affected registers are below:
    
    I also expanded the data field to 64 bits by using register 3 as the upper half.

    To initiate transactions larger than 32 bits, you should write the upper half 
    of the data to register 3 first and then the lower 32 bits to register 2.
    The write to register 2 will trigger the transaction.  The resulting read data
    from the slave can be retrieved by reading register 2 and 3 in any order.


    
    
      assign spi_config_register_readback[31:0] = {16'h0000,                // bits 31:16
                                               spi_data_length[3:0],    // bits 15:12
                                               loopback,                // bit 11
                                               spi_clock_divider[6:0],  // bits 10:4
                                               2'b00,                   // bits 3:2
                                               spi_cpha,                // bit 1
                                               spi_cpol};               // bit 0
    where the data length is encoded as:

      reg [3:0]      spi_data_length;  // 0 = 8 bits
                                   // 1 = 12 bits
                                   // 2 = 16 bits
                                   // 3 = 24 bits
                                   // 4 = 32 bits
                                   // 5 = 40 bits
                                   // 6 = 48 bits
                                   // 7 = 56 bits
                                   // 8-15 = 64 bits

    
    
    """
    """
    VERSION 1
        All 4 SPI masters are located in register block 6 where:
    
    *                   A12-A10 = Internal block select
    *                             000 = DUT UART block data
    *                             001 = DUT UART block registers
    *                             010 = DIO UART block data
    *                             011 = DIO UART block registers
    *                             100 = Chip level register block registers
    *                             101 = Spare
    *                             110 = SPI block registers
    *                             111 = Interrupt controller registers
    *                   A9-A4  = Slot Select
    *                   A3-A0  = Specific Block/Slot register select
    
    SPI Master 0 is located at slot 8, 1 at slot 9, 2 at slot 10 and 3 at slot 11 so we can use the short connector board
    
    Each SPI master block has the following registers:
    
      assign spi_config_register_readback[31:0] = {21'h000000,              // bits 31:12
                                                   spi_clock_divider[6:0],  // bits 10:4
                                                   spi_data_length[1:0],    // bits 3:2
                                                   spi_cpha,                // bit 1
                                                   spi_cpol};               // bit 0
    
      assign spi_status_register_readback[31:0] = {24'h000000,             // bits 31:8
                                                   spi_debug_state[3:0],   // bits 7:4
                                                   low,                    // bit 3
                                                   spi_mode[1:0],          // bits 2:1
                                                   spi_xfer_in_progress};  // bit 0
    
    // Register read MUX
      always @(*) begin
        case (register_addr[5:0])
    
          6'h00 : register_data_mux[31:0] = spi_config_register_readback[31:0];
          6'h01 : register_data_mux[31:0] = spi_status_register_readback[31:0];
          6'h02 : register_data_mux[31:0] = spi_data_in[31:0];
          default : register_data_mux[31:0] = 32'h00000000;
    
        endcase
      end
    
    // Write registers
      always @(posedge clock100 or posedge reset) begin
        if (reset) begin
          spi_cpol <= low;  // default to idle = 0, active = 1
          spi_cpha <= low;  // default to positive edge triggered
          spi_data_length <= 2'h0;  // default to 8 bits
          spi_clock_divider <= 7'd9;  // Default to 5 MHz
          spi_start_pulse <= low;
          write_2_spare_reg_error <= low;
          write_2_ro_reg_error <= low;
        end
        else begin
          if (register_write) begin
            casex (register_addr[5:0])
    
              6'h00 : begin  // SPI config register
                spi_clock_divider[6:0] <= register_data_in[10:4];
                spi_data_length[1:0] <= register_data_in[3:2];
                spi_cpha <= register_data_in[1];
                spi_cpol <= register_data_in[0];
              end
              6'h01 : write_2_ro_reg_error <= high; // RO SPI status register
              6'h02 : begin // SPI data to be sent
                spi_data_out[31:0] <= register_data_in[31:0];
                spi_start_pulse <= ~spi_xfer_in_progress && chip_enable;  // Start a new transfer assuming one isn't in progress
              end
              6'h03 : write_2_spare_reg_error <= high; // Spare
              6'h04 : write_2_spare_reg_error <= high; // Spare
              6'h05 : write_2_spare_reg_error <= high; // Spare
              6'h06 : write_2_spare_reg_error <= high; // Spare
              6'h07 : write_2_spare_reg_error <= high; // Spare
              6'h08 : write_2_spare_reg_error <= high; // Spare
              6'h09 : write_2_spare_reg_error <= high; // Spare
              6'h0a : write_2_spare_reg_error <= high; // Spare
              6'h0b : write_2_spare_reg_error <= high; // Spare
              6'h0c : write_2_spare_reg_error <= high; // Spare
              6'h0d : write_2_spare_reg_error <= high; // Spare
              6'h0e : write_2_spare_reg_error <= high; // Spare
              6'h0f : write_2_spare_reg_error <= high; // Spare
              6'h1x : write_2_spare_reg_error <= high; // Spare
              6'h2x : write_2_spare_reg_error <= high; // Spare
              6'h3x : write_2_spare_reg_error <= high; // Spare
    
            endcase
          end
          else begin
              spi_start_pulse <= low;
          end
        end
      end
    
      reg [1:0]      spi_data_length;  // 0 = 8 bits
                                       // 1 = 12 bits
                                       // 2 = 16 bits
                                       // 3 = 32 bits
      reg [6:0]      spi_clock_divider;  // Sets the SPI clock rate
                                         // clock rate (in MHz) = 50MHz / (divider + 1)
                                         // For 10MHz, set to 4
                                         // For 5MHz, set to 9
                                         // For 1MHz, set to 49
    
    Note that a write to register 2 starts an IO transfer
    
    In the future, I will add FIFOs but for now only 1 transaction at a time.
    
    Let me know, if there are questions
    
    Dave M.
    """
class Spi(object):
    '''
    classdocs
    '''

    def __init__(self, slotid, protocol, boardType=None, isDebug=False):
        '''
        SPI
        Constructor
        '''
        self.fpga = Fpga(slotid, protocol, boardType, isDebug)
        self.slotid = slotid
        self.baseConfiRegister = 0x90       # SPI Clock divider = 9
        self.baseConfiRegister |= 0x03   # CPOL = 1, CPHA = 1
#        self.baseConfiRegister |= 0x800      #0x800 loopback

    def __del__(self):
        del self.fpga
        
    def registersToString(self):
        retString = ""
        registers=[0, 1, 2]
        for register in registers:
            value = self.fpga.readRegister( "spi", register )
            retString += "SPI Register %02d: %s\n" % (register, self.fpga.addressToString(value) )
        return retString
    
    def setOutputEnable(self, enable):
        config = self.fpga.readRegister("spi", 0)
        if enable:
            config &= ~(1 << 2)
        else:
            config |= (1 << 2)
        self.setConfigRegister(config)
    
    
    def setConfigRegister(self, value):
        self.fpga.writeRegister("spi", 0, value)

    def __prepareForSend(self, byteCount):
        # Clear buffers by toggling clear bits
        CLEAR_BITS = 0x3 << 26
        lengthBits = ((byteCount * 8) - 1) << 12  # TODO: error checking
        self.setConfigRegister( self.baseConfiRegister + CLEAR_BITS )
        
        self.setConfigRegister( self.baseConfiRegister + lengthBits )   # note CLEAR bits are off


    def __stringToWords(self, string):
        if ( len(string) == 0 ): return []
        # Make it a multiple of 4:
        remainder = len(string) % 4
        for i in range( (4 - remainder) % 4 ):
            string += '\x00'
        wordCount = (len(string) / 4)
        words = []
        for i in range(wordCount): 
            valueTuple = struct.unpack_from(">I", string, i * 4 )    # interpret string as big endian integer for SPI
            words.append( valueTuple[0]  )
        return words

    def __loadSendBuffer(self, messageIn ):
        # Frankenslot SPI implementation is weird.  To deal with it first swap all the bytes around:
        #message = reverseCharOrder( messageIn )
        words = self.__stringToWords( messageIn )
        for word in words:
            self.fpga.writeRegister("spi", 4, word)

            
    def sendBuffer(self, messageIn):
        self.byteCount = len(messageIn)
        self.__prepareForSend( self.byteCount )
        self.__loadSendBuffer( messageIn )
        self.fpga.writeRegister("spi", 2, 0)   # Start transfer
        return (0,)
        
            
    def readBuffer(self, readByteCount):
        
        time.sleep(0.250)  # TODO: This can be refined!
        
        wordCount = ( (self.byteCount - 1) / 4) + 1
        remainder = self.byteCount % 4
        
        words = []
        for i in range(wordCount):
            words.append(self.fpga.readRegister("spi", 4))
        
        self.fpga.printDebug("SPI Readback words: " , repr(words))
        
        #Convert to string
        message = ""
        for i in range(wordCount - 1):
            message += struct.pack(">I", words[i] & 0xffffffff)                     # Remember to be big-endian 
        lastWordAsString = struct.pack(">I", words[wordCount - 1] & 0xffffffff)     # Remember to be big-endian 
        message += lastWordAsString[0:remainder]
        return message[self.byteCount - readByteCount:]
        

         
    
    def toString(self):
        return "SPI - slot %d" % self.slotid
    

BIT_MASK_DICT = \
    { 
      1: 0x00000001,
      2: 0x00000003,
      3: 0x00000007,
      4: 0x0000000f,
     
      5: 0x0000001f,
      6: 0x0000003f,
      7: 0x0000007f,
      8: 0x000000ff,

      9: 0x000001ff,
     10: 0x000003ff,
     11: 0x000007ff,
     12: 0x00000fff,

     13: 0x00001fff,
     14: 0x00003fff,
     15: 0x00007fff,
     16: 0x0000ffff,

     17: 0x0001ffff,
     18: 0x0003ffff,
     19: 0x0007ffff,
     20: 0x000fffff,

     21: 0x001fffff,
     22: 0x003fffff,
     23: 0x007fffff,
     24: 0x00ffffff,

     25: 0x01ffffff,
     26: 0x03ffffff,
     27: 0x07ffffff,
     28: 0x0fffffff,

     29: 0x1fffffff,
     30: 0x3fffffff,
     31: 0x7fffffff,
}

class Jtag(object):
    '''
    classdocs
    '''

    def __init__(self, slotid, protocol, boardType=None, isDebug=False):
        '''
        JTAG
        Constructor
        '''
        self.slotid = slotid
        self.fpga = Fpga(slotid, protocol, boardType, isDebug )
        self.isLoopback = False
        self.clockDividerReal = 5      # Default is 10MHz.  50MHz / 5

    def __del__(self):
        del self.fpga
        
    def registersToString(self):
        retString = ""
        registers=[0, 1, 2,  5, 6]  # Don't read 3 and 4 as that has side effects
        for register in registers:
            value = self.fpga.readRegister( "jtag", register )
            retString += "JTAG Register %02d: %s\n" % (register, self.fpga.addressToString(value) )
        return retString
    
    
    def setOutputEnable(self, enable):
        config = self.readConfigRegister()
        if enable:
            config &= ~(1 << 2)
        else:
            config |= (1 << 2)
        self.writeConfigRegister( config )
            
    def setEnable(self, isEnable):
        """
        When disabled, also assert TRST to hold TAP contorller in reset
        """ 
        config = self.readConfigRegister()
        if isEnable:
            config |= (1 << 0)      # Set bit 0 to enable
            config &= ~(1 << 18)    # Clear bit 18 to de-assert TRST
        else:
            config &= ~(1 << 0)     # Clear bit 0 to disable
            config |= (1 << 18)     # Set bit 18 to assert TRST
        self.writeConfigRegister( config )
        
    def writeConfigRegister(self, value):
        self.fpga.writeRegister("jtag", 0, value)

    def readConfigRegister(self):
        return self.fpga.readRegister("jtag", 0)

    def readStatusRegister(self):
        return self.fpga.readRegister("jtag", 1)

    def writeTransactionRegister(self, value):
        self.fpga.writeRegister("jtag", 2, value)

    def stringToWords(self, string):
        if ( len(string) == 0 ): return []
        # Make it a multiple of 4:
        remainder = len(string) % 4
        for i in range( (4 - remainder) % 4 ):
            string += '\x00'
        wordCount = (len(string) / 4)
        words = []
        for i in range(wordCount): 
            valueTuple = struct.unpack_from("<I", string, i * 4 )    # interpret string as little endian integer
            words.append( valueTuple[0]  )
            
        return words
    
    def canDoTransaction(self):
        config = self.readConfigRegister()
        trst = config & (1<<18);
        enable = config & (1<<0);

        if 0 == enable or 1 == trst:
            return False;
        return True
        
    def readTransactionRegister(self):
        return self.fpga.readRegister("jtag", 2)

    def writeInstructionBufferStr(self, dataString):
        arrayOfWords = self.stringToWords(dataString)
        self.writeInstructionBuffer( arrayOfWords )

    def writeDataBufferStr(self, dataString):
        arrayOfWords = self.stringToWords(dataString)
        self.writeDataBuffer(arrayOfWords)
            
    def writeInstructionBuffer(self, arrayOfValues):
        for value in arrayOfValues:
            self.fpga.writeRegister("jtag", 4, value)
                
    def writeDataBuffer(self, arrayOfValues):
        for value in arrayOfValues:
            self.fpga.writeRegister("jtag", 3, value)


    def _readJtagWords(self, wordRegister, wordCount, bitCount):
        """
        Specify bit count of 0 to blindly read all bits.  This always results in a return
        value that is a multiple of 32 bits.
        """
        stringOfValues =""
        if bitCount == 0:  bitCount = wordCount * 32
        for i in range(wordCount):
            try:
                if (bitCount >= 32):  mask = 0xffffffff
                else: mask = BIT_MASK_DICT[bitCount]
            except:
                mask = 0xffffffff       # Ideally should raise this as an error
            data = self.fpga.readRegister("jtag", wordRegister)
            dataString = struct.pack("<I", data & mask)
            stringOfValues += dataString
            bitCount -= 32         
        return stringOfValues
    
    def readInstructionBuffer(self, bitCount):
        """
        Specify bit count of 0 to blindly read all bits.  This always results in a return
        value that is a multiple of 32 bits.
        """        
        wordCount = self._getInstructionRecvFifoCount()
        return self._readJtagWords( 4, wordCount, bitCount)

    def readDataBuffer(self, bitCount):
        """
        Specify bit count of 0 to blindly read all bits.  This always results in a return
        value that is a multiple of 32 bits.
        """        
        wordCount = self._getDataRecvFifoCount()
        return self._readJtagWords( 3, wordCount, bitCount)

    def clearTdoBuffers(self):
        self.readInstructionBuffer(0)
        self.readDataBuffer(0)

    def _getInstructionRecvFifoCount(self):
        count = self.fpga.readRegister("jtag", 6) & 0x7f
        return count
    
    def _getDataRecvFifoCount(self):
        count = self.fpga.readRegister("jtag", 5) & 0x7f
        return count

    def getInstructionSendFifoCount(self):
        count = self.fpga.readRegister("jtag", 6) & 0x3f0000
        count = count >> 16
        return count * 32

    def getDataSendFifoCount(self):
        count = self.fpga.readRegister("jtag", 5) & 0x3f0000
        count = count >> 16
        return count * 32


    def calculateClockDivider(self, frequencyInHz):
        '''
        Returns clock divider for Titan.   
        Titan base clock is 50Mz.   Frequency = 50Mhz / (divider + 1)
        '''
        roughDivider = (JTAG_BASE_CLOCK / frequencyInHz)
        divider = int(math.floor(roughDivider));
        if roughDivider != divider: divider = divider + 1   # Contorted way of rounding up!
        if divider > MAX_JTAG_CLOCK_DIVIDER:      # Lowest Frequency
            divider = MAX_JTAG_CLOCK_DIVIDER
            nextHigherFrequencyInHz = JTAG_BASE_CLOCK / (divider - 1)
        elif divider <= MIN_JTAG_CLOCK_DIVIDER:      # Highest Frequency
            divider = MIN_JTAG_CLOCK_DIVIDER
            nextHigherFrequencyInHz = JTAG_BASE_CLOCK / (divider)
        else:
            nextHigherFrequencyInHz = JTAG_BASE_CLOCK / (divider - 1)
        
        actualFrequencyInHz = JTAG_BASE_CLOCK / divider    
        return divider, actualFrequencyInHz, nextHigherFrequencyInHz

    def setFrequency(self, requestedFreqInHz ):
        '''
        '''
        realDivider, actualFreqInHz, nextHigherFreqInHz = self.calculateClockDivider(requestedFreqInHz)
        self.clockDividerReal = realDivider

        infoString =  "Requested: %sHz, Actual: %sHz, Next higher: %sHz" % \
            ( "{:,}".format(requestedFreqInHz), "{:,.3f}".format(actualFreqInHz), "{:,.3f}".format(nextHigherFreqInHz) )
        return ( 0, infoString )        

    def tapReset(self, type="tms", durationInMs=0):
        # toggle jtag enable
        config = self.readConfigRegister()
        config &= ~0x40ffe  # Turn off  force TRST (0x40000), loop-back (0x800), clock bits (0x7f0), force SRST and use TRST (0xa0) and output_disable (0x4)

        # TODO: Remove if/when we implement JtagSetFrequency
        clockDivider = (self.clockDividerReal - 1) << 4
        config |= clockDivider
        config &= ~1            # Clear enable bit for either reset.

        if type == "trst" : 
            self.writeConfigRegister( config | ( 1 << 18 ))
        else:
            self.writeConfigRegister( config )  # Turn off JTAG ENABLE to do TMS or TRST reset

        time.sleep( durationInMs / 1000.0)
        # No data
        if self.isLoopback:
            self.writeConfigRegister(config | 0x801)   # 0x800 for loopback of JTAG
        else:
            self.writeConfigRegister(config | 0x01)
            
        self.clearTdoBuffers()
        
    def systemReset(self, durationInMs = 1):
        config = self.readConfigRegister()
        self.writeConfigRegister(config | (1 << 3)) 
        time.sleep(durationInMs / 1000.0)
        self.writeConfigRegister(config) 
        pass

    def doTransaction(self, instruction, iBitLength, data, dBitLength):
        #Load FIFOs
        self.writeInstructionBufferStr(instruction)
        self.writeDataBufferStr(data)
        
        # Write transaction register to start send:
        transaction = self.buildTransaction(iBitLength, dBitLength)
        self.writeTransactionRegister(transaction)
        
    def buildTransaction(self, iBitLength, dBitLength):
        transaction = 0
        isInstruction = (iBitLength > 0)
        
        if isInstruction: 
            transaction |= iBitLength
            transaction |= (1 << 27)
        else:
            transaction |= (1 << 31)
            transaction |= (1 << 30)
            transaction |= (dBitLength << 16)
        
        return transaction

    def isBusy(self):
        status = self.readStatusRegister()
        return  (status & 0x1) == 0x1
    
    def toString(self):
        return "JTAG - slot %d" % self.slotid
    

class FP(object):
    def __init__(self, slotid, protocol, boardType=None, isDebug=False):
        '''
        FP
        Constructor
        '''
        self.fpga = Fpga(slotid, protocol, boardType, isDebug)
        self.slotid = slotid
        
    def doSoftReset(self):
        data = self.fpga.readRegister("fpUart", 6)
        resetData = (1<< 7) | data
        self.fpga.writeRegister("fpUart", 6, resetData)
        self.fpga.writeRegister("fpUart", 6, data)
        
        

    def __del__(self):
        del self.fpga
    
    
    
if __name__ == "__main__":
#     print "Running Main"
#     o = Fpga(8, sio.SIO5_BOARD)
#     print "Drive UART address = " , o.addressToString( o.buildAddress( "spi", 2 ) )

    if False:
        protocol = MRPCProtocol.MRPCProtocol()
            
        spies = []
        spies.append(Spi( 8, protocol, sio.SIO5_BOARD ))
        spies.append(Spi( 9, protocol, sio.SIO5_BOARD ))
        spies.append(Spi( 10, protocol, sio.SIO5_BOARD ))
        spies.append(Spi( 11, protocol, sio.SIO5_BOARD ))
        print("Registers: ")
        
        for spi in spies:
            spi.setConfigRegister(0x890)
            print("slot %s registers" % (spi.toString()))
            print(spi.registersToString())
            print()
            spi.sendBuffer("\x01\x0b\x10")
            print ("Spi Read: " , repr(spi.readBuffer(3)))
        
    #     spies[0].sendBuffer("\xab")
    #     print "Spi Read: " , repr(spies[0].readBuffer(1))
    # 
    #     spies[0].sendBuffer("ab")
    #     print "Spi Read: " , repr(spies[0].readBuffer(2))
    
    
    
    
    #    spies[0].sendBuffer("\x10\x0b\x01")
        
        # TODO: Byte order is backwards
    
    
    #     while True:
    #         for spi in spies:
    #             print  "slot %s registers" % (spi.toString()) 
    #             spi.sendBuffer("\xab")
    #             print "Spi Read: " , repr(spi.readBuffer(1))
        
    if False:
        print ("JTAG")
        protocol = MRPCProtocol.MRPCProtocol()
        
        jtag = Jtag(0, protocol, sio.SIO5_BOARD)
        
        print (jtag.toString())
        print (jtag.registersToString())
        
        instruction = [0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555]
        testData = [0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555,0xaaaaaaaa, 0x55555555]
        
        jtag.doTransaction(instruction, 0, testData, 64)
        
    if True:
        print ("Testing reversCharOrder")
        output = reverseCharOrder( "\x01\x02\x03")
        print (repr(output))
        output = reverseCharOrder( "\x01\x02\x03abc")
        print (repr(output))
        output = reverseCharOrder( "")
        print (repr(output))