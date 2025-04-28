#!/usr/bin/python
'''
Copyright (c) 2016, 2017, 2018, 2019 Teradyne, Inc. All rights reserved.

'''
__version__ = "2.1.12"


import time
__startTime__= time.time()
global serversocket

try:
    import _version as sltVersion
    extendedVersionString = sltVersion.__version__
except:
    extendedVersionString = __version__

import json
import optparse
import os
import sys
import traceback
import struct
import socket
import threading
import datetime
import timeit

from terParser import TerParser
from terParser import TerParserError
import sioApi as API
import sio as SIO
from MRPCProtocol import MRPCProtocol
from MRPCProtocol import MRPCError
from stringLibrary import StringLibrary
import fpga
JTAG_IN_SIO=True
MAX_SPI_BUFFER_LENGTH = 512

singleSioSequence = False
totalSioTime = 0

class ClientClosedSocketError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ClientHandler(threading.Thread):
    def __init__(self, sock, isDebug=False):
        self.clientSocket = sock
        self.isDebug = isDebug
        threading.Thread.__init__(self)

    def __recv_N_bytes(self, n):
        data = b''
        while len(data) < n:
            packetLen = 0
            try:
                packet = self.clientSocket.recv(n - len(data))
                packetLen = len(packet)
            except:
                pass

            if packetLen < 1:
                raise ClientClosedSocketError("Client socket closed")
            data += packet
        return data

    def get_byte_array(self):
        self.clientSocket.settimeout(None)
        rawData = self.__recv_N_bytes(4)
        rawData = struct.unpack("L", rawData)[0]
        rawData = socket.ntohl(rawData)
        bytesToReceive = rawData
        receivedMessage = self.__recv_N_bytes(bytesToReceive)
        return receivedMessage

    def send_byte_array(self, message):
        rawData = len(message)
        rawData = socket.htonl(rawData)
        bytesToSend = struct.pack('I', rawData)
        self.clientSocket.sendall(bytesToSend + message.encode())

    def run(self):
        try:
            while 1:
                if self.isDebug:
                    print('Waiting for client message ...')

                receivedMessage = self.get_byte_array()

                if self.isDebug:
                    print('Received message' + receivedMessage + '...')

                reset_timer()

                options_slotIdx = None
                options_ipAddress = None
                options_port = None
                options_isDebug = None
                options_isVerbose = None
                options_timeoutInMs = None
                argsList = receivedMessage.split()
                if argsList[0].lower() == "exit":
                    serversocket.close()
                    os._exit(0)
                    break

                # Look for and remove arguments meant for this python program
                # User may have specified the same argument multiple times. Remove all of them and use the last one

                switch = "-d"
                while switch in argsList:
                    options_isDebug = True
                    argsList.remove(switch)
                switch = "--debug"
                while switch in argsList:
                    options_isDebug = True
                    argsList.remove(switch)

                switch = "-v"
                while switch in argsList:
                    options_isVerbose = True
                    argsList.remove(switch)
                switch = "--verbose"
                while switch in argsList:
                    options_isVerbose = True
                    argsList.remove(switch)

                switch = "-s"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_slotIdx = int(argsList[argsList.index(switch) + 1])
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)
                switch = "--slot"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_slotIdx = int(argsList[argsList.index(switch) + 1])
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)

                switch = "-i"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_ipAddress = argsList[argsList.index(switch) + 1]
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)
                switch = "--ip-address"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_ipAddress = argsList[argsList.index(switch) + 1]
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)

                switch = "--port"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_port = int(argsList[argsList.index(switch) + 1])
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)

                switch = "-t"
                while switch in argsList:
                    if len(argsList) > (argsList.index(switch) + 1):
                        options_timeoutInMs = float(argsList[argsList.index(switch) + 1])
                        argsList.pop(argsList.index(switch) + 1)
                    argsList.remove(switch)

                # The remaining list of strings is the SIO command plus all its arguments
                commandString = argsList.pop(0)
                for string in argsList:
                    commandString += " " + string

                if self.isDebug:
                    print('Executing command'+commandString+'...')

                result = sioRun(commandString, options_slotIdx, options_ipAddress, options_port, options_isDebug, options_isVerbose, options_timeoutInMs)
                sioElapsedTime = time.time() - startTime

                response = ""
                if options_isDebug:
                    response += "SIO elapsed time: " + "{0:.3f}".format(sioElapsedTime * 1.0e3) + " ms\n"
                    response += "Total elapsed time: " + "{0:.3f}".format((time.time() - __startTime__) * 1.0e3) + " ms\n"

                response += result
                if self.isDebug:
                    print('Response:'+ response)

                self.send_byte_array (response)
        except ClientClosedSocketError:
            if self.isDebug:
                print("Client socket was closed")
            self.clientSocket.close()
        except Exception as e:
            #if self.isDebug:
            print(type(e).__name__+"Exception in client thread:")
            print(traceback.format_exc())
            self.clientSocket.close()

def sioRun(commandString, slotIdx=None, ipAddress=None, ipPort=None, isDebug=False, isVerbose=False, timeoutInMs=None ):

    try:
        o = SioRunner( slotIdx, ipAddress, ipPort, isDebug, isVerbose, timeoutInMs)
    except:
        exctype, value = sys.exc_info()[:2]
        tb = traceback.extract_tb(sys.exc_info()[2])
        return "(False, 'ERROR -- constructor unknown exception in: %s,  %s, %s')" % (exctype, value,  repr(tb))
    else:
        o.run(commandString);
        responseMsg = o.getResponseMsg()
        del o   #TODO: Replace this with "with SioRunner()"
        return responseMsg

class SioRunnerError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SioRunner(object):
    sioCommandDictionary = \
    {
        "GetSiteInfo"                      : "TER_GetSlotInfo", \
        "GetSiteSettings"                  : "TER_GetSlotSettings", \
        "GetSiteStatus"                    : "TER_GetSlotStatus", \
        "Reset"                            : "TER_Reset",\
        "SioSendBuffer"                    : "TER_SioSendBuffer", \
        "SioReceiveBuffer"                 : "TER_SioReceiveBuffer", \
        "SetPowerEnable"                   : "TER_SetPowerEnable", \
        "SetPowerVoltage"                  : "TER_SetPowerVoltage",\
        "SetPowerVoltageBounds"            : "TER_SetPowerBounds",\
        "ResetPowerAveraging"              : "TER_ResetAveraging",\
        "GetPowerAveragingInfo"            : "TER_GetAveragingInfo",\
        "SetPowerSampleRate"               : "TER_SetSampleRate",\
        "GetFpInfo"                        : "TER_GetFpInfo",\
        "SetFpInfo"                        : "TER_SetFpInfo",\
        "GetSbInfo"                        : "TER_GetSbInfo",\
        "GetSbStatus"                      : "TER_GetSbStatus",\
    }

    localCommandList = \
    {
        "GetSioRunnerInfo",

        "SetUsbVbusEnable",
        "SetUsbSsEnable",
        "SetSerialEnable",

        "SpiSendReceive",
        "SpiWriteFpga",
        "SpiReadFpga",
        "SpiSetConfig",
        "SpiGetConfig",

        "JtagWriteIR",
        "JtagWriteDR",
        "JtagWriteReadIR",
        "JtagWriteReadDR",
        "JtagTapReset",
        "JtagSystemReset",
        "JtagSetFrequency",
        "JtagSetEnable",
        "JtagDebugSelect",
        "SioSendCommand",

        "StartTest",
        "StopTest",
        "GetTestStatus",
        "SetUartReader",
        "SyncFiles",

        "SetTimeout",

        "UnitTestHook",

        "DutConsoleRead",
        "DutConsoleReadLn",
        "DutConsoleStatus",
        "DutConsoleSetReadPos",

        "SetPowerVoltageGoodRange",
        "SetPowerVoltageTripPoint",
        "SetPowerCurrentTripPoint",
        "GetPowerAveragingData",
        "SetPowerAveragingDataStorageMode",
        "FpReset",

        "SetDutUsbChannel",

        "RunSequence",

        "ConnectUsb"
    }

    def __init__(self, slotIdx=None, ipAddress=None, ipPort=None, isDebug=False, isVerbose=False, timeoutInMs=None):
        self.parser = TerParser()

        self.slotIdx = slotIdx
        self.ipAddress = ipAddress
        self.ipPort = ipPort
        self.isDebug = isDebug
        self.isVerbose = isVerbose
        self.responseTuple = ()
        self.responseMsg = ""

        if not self.slotIdx:
            # Use environment variable for slotIdx if available
            try:
                envVal = os.environ["SIOSITEINDEX"]
            except KeyError:
                try:
                    envVal = os.environ["SIOSLOTINDEX"]
                except KeyError:
                    envVal = "1"
            try:
                self.slotIdx = int( envVal )
            except:
                self.slotIdx = 1
        print("slot ID :", self.slotIdx )
        try:
            self.commands = SioCommands( self.slotIdx, ipAddress=self.ipAddress, ipPort=self.ipPort, isVerbose=self.isVerbose, isDebug=self.isDebug, timeoutInMs=timeoutInMs )
        except MRPCError as e:
            self.setErrorMsg(e.msg)
        except:
            raise

    def __del__(self):
        try:
            del self.commands
        except:
            exctype, value = sys.exc_info()[:2]
            tb = traceback.extract_tb(sys.exc_info()[2])
            return "(False, 'ERROR -- destructor unknown exception in: %s,  %s, %s')" % (exctype, value,  repr(tb))


    def getResponseMsg(self):
        """
        This gets the response we are going to send to the user.

        :return: A string representing debug data if any followed by a line containing the response tuple
        """
        elapsedTimeInMicroSeconds =  int((time.time() - __startTime__) * 1e6)
        # time.time() in python 2 has a resolution of 10 ms.
        # For values less than that, instead of returning 0, return 5 ms
        if elapsedTimeInMicroSeconds == 0:
            elapsedTimeInMicroSeconds = 5000
        self.responseTuple += (elapsedTimeInMicroSeconds,)
        return self.responseMsg + repr(self.responseTuple) + "\r"


    def setErrorMsg(self, message):
        if (len(self.responseTuple) > 0): return     # Response tuple is first error
        self.responseTuple = (False, message )

    def setDebugMsg(self, msg0, msg1=None):
        if self.isDebug:
            self.responseMsg += msg0
            if msg1: self.responseMsg += " " + msg1
            self.responseMsg += "\n"

    def run(self, commandString):
        try:
            method,paramTuple = self.parser.parseCommand( commandString )
            # Try local commands first so we can override SIO commands
            if method in self.localCommandList:
                result = self.dispatch( method, paramTuple )
                if result:
                    self.setDebugMsg( self.commands.getDebugMsg() )
                    self.responseTuple = self.commands.setResults( result )
                else: self.setErrorMsg ("Local command not implemented: %s" % (method) )
                return

            # Now try SIO commands if there we didn't match a local command
            if method in self.sioCommandDictionary:
                sioCommand = self.sioCommandDictionary[method]
                result =  self.commands.doSioCommand( sioCommand, paramTuple)
                self.setDebugMsg( self.commands.getDebugMsg() )
                self.responseTuple = self.commands.setResults( result )
                return

            self.setErrorMsg( "Command not implemented: %s" % (commandString) )
        except TerParserError as e:
            self.setErrorMsg( e.msg )
        except SioRunnerError as e:
            self.setErrorMsg( e.msg )
        except MRPCError as e:
            self.setErrorMsg( e.msg )
        except:
            exctype, value = sys.exc_info()[:2]
            tb = traceback.extract_tb(sys.exc_info()[2])
            self.setErrorMsg( "ERROR -- unknown exception: %s,  %s, %s" % (exctype, value,  repr(tb)))
        return

    def dispatch(self, method, params):
        mname = 'do_' + method
        cname = "Command" + method

        # Look for a do_Method method. If found, execute it.
        if hasattr(self.commands, mname):
            method = getattr(self.commands, mname)
            return method( params )

        # Look for a CommandMethod class. If found, initantiate it and call do method.
        elif hasattr(self.commands, cname):
            command = getattr(self.commands, cname)(self.commands)
            return command.do(params)

        # Command not found.
        else:
            return None

class SioCommands(object):

    SETTINGS_FILE_NAME = "sioRunnerSettings.json"
    TIMEOUT_SETTING_TAG = "timeoutInSeconds"
    DEFAULT_TIMEOUT_IN_MS = 35000

    def __init__(self, slotIdx=1, ipAddress=None, ipPort=None, isVerbose=False, isDebug=False, timeoutInMs=None):
        """
        We default slotIdx to 1 for those operations that don't care about slotIdx
        """
        self.debugString = ""
        self.slotIdx = slotIdx
        self.isVerbose = isVerbose
        self.isDebug = isDebug
        self.ipAddress = ipAddress
        self.ipPort = ipPort

        self.settings = self._readJSON(self.SETTINGS_FILE_NAME)
        self.setDebugMsg( repr(self.settings))

        # Time by which we must be done.
        if timeoutInMs is None:
            try:
                timeoutInSeconds = self.settings[self.TIMEOUT_SETTING_TAG]
                timeoutInMs = timeoutInSeconds * 1000.0
            except:
                timeoutInMs = self.DEFAULT_TIMEOUT_IN_MS

        self.setDebugMsg( "Timeout in ms:",  repr(timeoutInMs))
        self.dueTime = time.time() + (timeoutInMs / 1000.0)

        self.protocol = MRPCProtocol(address=self.ipAddress, port=self.ipPort, isProduction=not self.isVerbose, dueTime=self.dueTime)
        self.spi = fpga.Spi(self.slotIdx - 1, self.protocol, isDebug=self.isDebug)  # TODO: This is fixed slot....
        self.jtag = fpga.Jtag(self.slotIdx - 1, self.protocol, isDebug=self.isDebug)
        self.radix = "hex"

    def __del__(self):
        try:
            self.protocol.close()  ## Make sure we close the socket! (The deletes below don't get it done...
            del self.protocol
            del self.spi
            del self.jtag
        except:
            exctype, value = sys.exc_info()[:2]
            tb = traceback.extract_tb(sys.exc_info()[2])
            return "(False, 'ERROR -- destructor unknown exception in: %s,  %s, %s')" % (exctype, value,  repr(tb))

    def _extendDueTime(self, commandName, paramTuple):
        if commandName.find("SioReceiveBuffer") > 0:
            timeout = paramTuple[0]
            timeoutTime = timeout / 1000.0
            self.setDebugMsg( "Extending timeout for %s(%s) by %2.3f seconds." % (commandName, repr(paramTuple), timeoutTime))
            self.protocol.extendDueTime(timeoutTime)

    def _readJSON(self, fileName):
        try:
            with open(fileName, "r") as myfile:
                contents= myfile.read()
            fileJson = json.loads(contents)
            return fileJson
        except:
            return {}

    def _writeJson(self, fileName, myDictionary):
        try:
            with open(fileName, "w") as myfile:
                myfile.write(json.dumps(myDictionary))
        except:
            raise

    def getDebugMsg(self):
        return self.debugString

    def setDebugMsg(self, msg0, msg1=None):
        if self.isDebug:
            self.debugString += msg0
            if msg1: self.debugString += " " + msg1
            self.debugString += "\n"

    def doSioCommand(self, commandName, paramTuple):
        self._extendDueTime(commandName, paramTuple)
        cmdIdx = API.cmdNameToIdx(commandName)

        startTime = timeit.default_timer()
        response = self.protocol.sendReceiveMessage(cmdIdx, self.slotIdx, paramTuple)

        global totalSioTime
        totalSioTime += timeit.default_timer() - startTime

        debugStr = self.protocol.getLastDebugStr()
        if len(debugStr):
            self.setDebugMsg( debugStr )
        return response

    def checkBooleanParameter(self, paramTuple, paramIndex):
        if len(paramTuple) < (paramIndex + 1):
            return API.TER_Status_ArgumentCountError
        if not (type( paramTuple[paramIndex] ) is bool ):
            return API.TER_Status_Error_Argument_Invalid
        return API.TER_Status_none

    def setResults(self, sioTuple):
        """
        Note that this function looks at the first element of the tuple to see if it is a number or a
        boolean.   This is because we changed the protocol to return a boolean and a string to convey
        where originally, we simply returned an int representing TER_Status.
        TOOD: Make sure  all callers send a "sioTuple" which matches the SIO behavior of returning
        TER_Status.
        Convert TER_Status to boolean and string here:
        :param sioTuple:
        :return:
        """
        firstValue = sioTuple[0]
        if ( type( firstValue ) is int ):
            newTuple = ( (firstValue == 0),)  # True if success. False otherwise
            if firstValue in API.TER_Status_Meanings:
                newTuple += ( API.TER_Status_Meanings[firstValue], )
            else:
                newTuple += (("%d" ) % (firstValue),)
            newTuple += sioTuple[1:]
        else: newTuple = sioTuple   #TODO: Is this ever called?
        return newTuple

    """
    Command base class

    Commands implemented by derived classes may be used with RunSequence. Commands must execute
    a single SIO command. Support for multiple SIO commands may be added in the future if necessary.

    Derived classes must implement the following:

    params - Get the SIO command parameters given the SIO runner parameters.
    result - Get the SIO runner result given the SIO command result.
    approxTime_us - Approximate time to execute command in microseconds.
    """
    class Command(object):
        def __init__(self, commands, name, approxTime_us):
            self.commands = commands
            self.name = name
            self.approxTime_us = approxTime_us

        def do(self, pt):
            sioResult = self.commands.doSioCommand(self.name, self.params(pt))
            return self.result(sioResult)


    """
    SPI
    """
    def do_SpiWriteFlash(self, pt):
        return (API.TER_Status_NotImplemented, )

    def do_SpiReadFlash(self, pt):
        return (API.TER_Status_NotImplemented, )


    class CommandSpiWriteFpga(Command):

        def __init__(self, commands):
            super(self.__class__, self).__init__(commands, "TER_SpiSendReceive", 30)

        def params(self, pt):
            """
            byte opcode
            byte address
            byte[] data
            """

            if self.commands.isDebug:
                self.commands.setDebugMsg( self.spi.registersToString() )

            paramCnt = len(pt)
            if paramCnt != 3: return (API.TER_Status_Error_Argument_Invalid, )
            message = ""
            message += chr(pt[0])  # Opcode
            message += chr(pt[1])  # Address
            message += StringLibrary.convertAsciiToBinary(pt[2])       # Data expressed as a string
            return (0, 0, message)

        def result(self, retVal):
            return (retVal[0],)    # TER_SpiSendReceive always returns an empty read string. We don't want it on writes.


    class CommandSpiReadFpga(Command):
        def __init__(self, commands):
            super(self.__class__, self).__init__(commands, "TER_SpiSendReceive", 30)

        def params(self, pt):
            """
            byte opcode
            byte address
            int length
            out byte[] data
            """
            if self.commands.isDebug:
                self.commands.setDebugMsg( self.commands.spi.registersToString() )

            paramCnt = len(pt)
            if paramCnt != 3: return (API.TER_Status_Error_Argument_Invalid, )
            message = ""
            message += chr(pt[0])  # Opcode
            message += chr(pt[1])  # Address
            readLengthInBytes = pt[2]
            return (0, readLengthInBytes, message)

        def result(self, retVal):
            return (retVal[0], StringLibrary.convertBinaryToAscii( retVal[1] ), )


    def do_SpiSendReceive(self, pt):
        """
        string: data to send
        byte read count
        """
        self.setDebugMsg( self.spi.registersToString() )
        paramCnt = len(pt)
        if paramCnt != 2: return (API.TER_Status_Error_Argument_Invalid, )
        message = StringLibrary.convertAsciiToBinary(pt[0])
        readLengthInBytes = pt[1]
        retVal = self.doSioCommand("TER_SpiSendReceive",  (0, readLengthInBytes, message))
        return (retVal[0], StringLibrary.convertBinaryToAscii( retVal[1] ), )

    def do_SpiSetConfig(self, pt):
        paramCnt = len(pt)
        if paramCnt != 2: return (API.TER_Status_Error_Argument_Invalid, )
        busWidth = pt[0]
        legalBusWidths = (1, 2, 4)
        if not(busWidth in legalBusWidths): return (API.TER_Status_Error_Argument_Invalid,)
        dummyBytes = pt[1]
        legalDummyBytes = (0, 1)
        if not(dummyBytes in legalDummyBytes): return (API.TER_Status_Error_Argument_Invalid,)

        config = busWidth + (dummyBytes << 4)
        config += (1 << 8)   # CPOL
        config += (1 << 9)   # CPHA
        return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_SpiConfiguration, 1, config))

    def do_SpiGetConfig(self, pt):
        paramCnt = len(pt)
        if paramCnt != 0: return (API.TER_Status_Error_Argument_Invalid, )
        retTuple = self.doSioCommand("TER_GetProperty", (API.TER_PropertyType_SpiConfiguration,))
        if retTuple[0] != API.TER_Status_none: return (retTuple[0], 0, 0)
        if retTuple[1] != 1: return (API.TER_Status_Invalid_Response, 0, 0)
        value = retTuple[2]
        busWidth = value & 0x7
        dummyBytes = (value & 0x10) >> 4
        return (API.TER_Status_none, busWidth, dummyBytes)

    """
    JTAG
    """
    def jtagWait(self, bitCount):
        waitStartTime = time.time()
#         bitTime = 0.002      # TODO: base off of clock speed 1MHz clock would be 1ms.  Margin factor of 2
#         time.sleep( bitTime * bitCount)

        while self.jtag.isBusy():
            # In SIO Application, put a sched_yield() here.  Best to have a timer.
            elapsedTime = time.time() - waitStartTime
            if (elapsedTime > 0.050): break
        elapsedTime = time.time() - waitStartTime
        if self.isDebug:
            self.debugString += "JTAG shift took  %f seconds.\n" % elapsedTime

    def _sioJtagWrite(self, registerType, tdiString, bitCount):
        tdiData =  StringLibrary.convertAsciiToBinary(tdiString)
        tdiData = fpga.reverseCharOrder(tdiData)
        message = ""
        message += tdiData    # Data expressed as a string
        retVal = self.doSioCommand("TER_JtagSendReceive", (registerType, bitCount, message))

        return  (retVal[0],  self._processJtagDataNoReverse( retVal[1]) , )

    def _jtagWrite(self, registerType, tdiString, bitCount):
        tdiData =  StringLibrary.convertAsciiToBinary(tdiString)
        tdiData = fpga.reverseCharOrder(tdiData)

        if not self.jtag.canDoTransaction():
            raise SioRunnerError("JTAG Transaction: JTAG is disabeled or in reset")
        if registerType == "DR":
            self.jtag.doTransaction("", 0, tdiData, bitCount)
        elif registerType == "IR":
            self.jtag.doTransaction(tdiData, bitCount, "", 0)
        else:
            raise SioRunnerError("JTAG Write: Unknown register type: %s.  Must be DR or IR" %(registerType))
        self.jtagWait( bitCount )
        return

    def _processJtagData(self, data):
        data = fpga.reverseCharOrder(data)
        dataStr = self._processJtagDataNoReverse(data)
        return dataStr
    def _processJtagDataNoReverse(self, data):
        dataStr = StringLibrary.convertBinaryToAscii(data, self.radix)
        dataStr = StringLibrary.stripLeadingCharacters(dataStr, self.radix)
        return dataStr

    def _setRadix(self, expectValue ):
        if expectValue[0] == '0':
            if expectValue[1] == 'b':
                self.radix="bin"
                return API.TER_Status_none
            elif expectValue[1] == 'x':
                self.radix="hex"
                return API.TER_Status_none
            else:
                return API.TER_Status_Error_Argument_Invalid
        else:
            return API.TER_Status_Error_Argument_Invalid

    def _jtagApplyExpectValue(self, readRvTuple, expectValue):
        if (readRvTuple[0] == API.TER_Status_none):
            actualValue =  readRvTuple[1]
            if not StringLibrary.compareStrings(actualValue, expectValue, self.radix):
                return (False, "JTAG expect value mis-match", actualValue)
        return readRvTuple;    #Either if failed:  readRv was broken, or all is good.

    def _jtagReadIR(self, bitCount):
        data = self.jtag.readInstructionBuffer(bitCount)
        return (API.TER_Status_none, self._processJtagData(data) )

    def _jtagReadDR(self, bitCount):
        data = self.jtag.readDataBuffer(bitCount)
        return (API.TER_Status_none, self._processJtagData(data) )

    def do_JtagSetEnable(self, paramTuple ):
        status = self.checkBooleanParameter(paramTuple, 0)
        if status != API.TER_Status_none: return (status, )
        if False == JTAG_IN_SIO:
            self.jtag.setEnable( paramTuple[0] )
        else:
            enable =int(paramTuple[0] == True)
            return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_JtagEnable, 1, enable))
        return (0,)

    def do_JtagDebugSelect(self, paramTuple ):
        status = self.checkBooleanParameter(paramTuple, 0)
        if status != API.TER_Status_none: return (status, )
        if True==paramTuple[0]:
            value = 1
        else:
            value = 0
        return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_JtagDebugSelect, 1, value))


    class CommandJtagWrite(Command):
        def __init__(self, commands, type):
            SioCommands.Command.__init__(self, commands, "TER_JtagSendReceive", 30)
            self.type = type

        def params(self, pt):
            tdiString = pt[0]
            tdiData =  StringLibrary.convertAsciiToBinary(tdiString)
            tdiData = fpga.reverseCharOrder(tdiData)
            message = ""
            message += tdiData    # Data expressed as a string
            bitCount = pt[1]
            return (self.type, bitCount, message)

        def result(self, retVal):
            if len(retVal) > 1:
                return  (retVal[0],  self.commands._processJtagDataNoReverse( retVal[1]) , )
            elif retVal[0] == API.TER_Status_none:
                return (API.TER_Status_JtagGeneralFailure,)
            else:
                return (retVal[0],)


    class CommandJtagWriteIR(CommandJtagWrite):
        def __init__(self, commands):
            SioCommands.CommandJtagWrite.__init__(self, commands, API.JtagType_Instruction)


    class CommandJtagWriteDR(CommandJtagWrite):
        def __init__(self, commands):
            SioCommands.CommandJtagWrite.__init__(self, commands, API.JtagType_Data)


    def do_JtagWriteIR(self, pt):
        if False == JTAG_IN_SIO:
            if len(pt) != 2: return (API.TER_Status_ArgumentCountError,)
            writeData = pt[0]
            bitCount = pt[1]
            self._jtagWrite( "IR", writeData, bitCount )
            readRvTuple = self._jtagReadIR(bitCount)
        else:
            readRvTuple = self.CommandJtagWriteIR(self).do(pt)
        return readRvTuple


    def do_JtagWriteDR(self, pt):
        if False == JTAG_IN_SIO:
            if len(pt) != 2: return (API.TER_Status_ArgumentCountError,)
            writeData = pt[0]
            bitCount = pt[1]
            self._jtagWrite( "DR", writeData, bitCount )
            readRvTuple = self._jtagReadDR(bitCount)
        else:
            readRvTuple = self.CommandJtagWriteDR(self).do(pt)
        return readRvTuple


    def do_JtagWriteReadIR(self, pt):
        if len(pt) != 3: return (API.TER_Status_ArgumentCountError,)
        writeData = pt[0]
        bitCount = pt[1]
        expectValue = pt[2]
        result = self._setRadix(expectValue)        # Expect value dictates the radix
        if result != API.TER_Status_none: return (result,)
        self._jtagWrite( "IR", writeData, bitCount )
        readRvTuple = self._jtagReadIR(bitCount)
        return self._jtagApplyExpectValue( readRvTuple, expectValue)

    def do_JtagWriteReadDR(self, pt):
        if len(pt) != 3: return (API.TER_Status_ArgumentCountError,)
        writeData = pt[0]
        bitCount = pt[1]
        expectValue = pt[2]
        result = self._setRadix(expectValue)        # Expect value dictates the radix
        if result != API.TER_Status_none: return (result,)
        self._jtagWrite( "DR", writeData, bitCount )
        readRvTuple = self._jtagReadDR(bitCount)
        return self._jtagApplyExpectValue( readRvTuple, expectValue)

    def do_JtagTapReset(self, pt):
            if len(pt) == 0:
                if False == JTAG_IN_SIO:
                    self.jtag.tapReset("tms", 0)
                    return (0,)
                else:
                    return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_JtagReset, 2, API.TER_JtagResetType_Tms, 0 ))
            if len(pt) == 2:
                if False == JTAG_IN_SIO:
                    self.jtag.tapReset( pt[0], pt[1] )
                    return (0, )
                else:
                    resetType=API.TER_JtagResetType_Tms
                    if "trst" == pt[0]:
                        resetType=API.TER_JtagResetType_Trst
                    return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_JtagReset, 2, resetType, pt[1]  ))
            return (API.TER_Status_ArgumentCountError,)


    def do_JtagSystemReset(self, pt):
        if len(pt) != 1: return (API.TER_Status_ArgumentCountError,)
        if False == JTAG_IN_SIO:
            self.jtag.systemReset( pt[0] )
        else:
            return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_JtagReset, 2, API.TER_JtagResetType_System, pt[0] ))
        pass

        return (0,) # Not much to say!

    def do_JtagSetFrequency(self, pt):
        if len(pt) != 1: return (API.TER_Status_ArgumentCountError,)
        return self.jtag.setFrequency( pt[0])

    def do_FpReset(self, pt):
        return self.doSioCommand("TER_SioReboot",(self.slotIdx,))
        pass

    def do_SetUsbSsEnable(self, paramTuple):
        status = self.checkBooleanParameter(paramTuple, 0)
        if status != API.TER_Status_none: return (status, )
        if paramTuple[0]:  setSignalParamTuple = ( 0x200, 0x200)
        else: setSignalParamTuple = ( 0x200, 0x00)
        return self.doSioCommand( "TER_SetSignal", setSignalParamTuple)

    def do_SetUsbVbusEnable(self, paramTuple):
        status = self.checkBooleanParameter(paramTuple, 0)
        if status != API.TER_Status_none: return (status, )
        if paramTuple[0]:  setSignalParamTuple = (0x100, 0x100)
        else: setSignalParamTuple = (0x100, 0x00)
        return self.doSioCommand( "TER_SetSignal", setSignalParamTuple)

    def do_SetSerialEnable(self, paramTuple):
        status = self.checkBooleanParameter(paramTuple, 0)
        if status != API.TER_Status_none: return (status, )
        return self.doSioCommand( "TER_SetSerialEnable", paramTuple)

    def do_GetSioRunnerInfo(self, paramTuple):
        return (0, "Version %s" % extendedVersionString)

    def do_SioSendCommand(self, paramTuple):
        numParams = len(paramTuple)
        if (numParams < 1) or (numParams > 2): return (API.TER_Status_ArgumentCountError,)
        if len(paramTuple) == 2:
            timeoutInSeconds = paramTuple[1] / 1000.0
        else:
            timeoutInSeconds = 0
        command = paramTuple[0] + '\r'
        rv = self.doSioCommand("TER_SioSendBuffer", ( command, ))
        if rv[0] != API.TER_Status_none: return rv
        # at 115,200 baud, we can overflow a 2048 buffer in 177ms.   So lets read ever  20 ms:
        response = ""
        isTimeout = False
        startTime = time.time()
        while not isTimeout :
            rv = self.ter("TER_SioReceiveBuffer", (20, 2048,))
            if rv[0] != API.TER_Status_none: return rv
            response += rv[1]
            isOverflow = rv[2]
            # if we are still getting data, and we haven't timed out, keep going
            # aka: If we have stopped getting data, or we have timed out , then stop:
            if (len(rv[1]) == 0) or  ((time.time() - startTime) > timeoutInSeconds):
                isTimeout = True

        return (0, response)

    def do_StartTest(self, paramTuple):
        if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError)
        return self.doSioCommand("TER_StartTest", (0, 0, 0, True, 4, "",))

    def do_StopTest(self, paramTuple):
        if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError)
        return self.doSioCommand("TER_StopTest", ())

    def do_GetTestStatus(self, paramTuple):
        if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError)
        response = self.doSioCommand("TER_GetTestStatus", ())
        return response

    def do_SetUartReader(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError,)
        readerName = paramTuple[0]

        if readerName == "sio": reader = API.SerialReaderSio
        elif readerName == "api": reader = API.SerialReaderApi
        else: return (False, "Expected parameter of either 'sio' or 'api', not %s" % readerName, )

        return self.doSioCommand("TER_SetProperty", (API.TER_PropertyType_SerialReaderSelect, 1, reader))

    def do_SyncFiles(self, paramTuple):
        if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError,)
        return self.doSioCommand("TER_Sync", ())

    def do_SetTimeout(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError,)
        timeoutInMs = paramTuple[0]
        # TODO: Actually do something with this.
        self.settings = { self.TIMEOUT_SETTING_TAG : timeoutInMs / 1000.0 }
        self._writeJson( self.SETTINGS_FILE_NAME, self.settings)
        return (0,)

    def do_UnitTestHook(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError,)
        mname = paramTuple[0]
        if hasattr(self, mname):
            method = getattr(self, mname)
            if mname == "convertAsciiToBinary": return repr(method( paramTuple[1] ))
            if mname == "convertBinaryToAscii": return repr(method( paramTuple[1] ))
        else:
            print("Local command %s not implemented" % (mname))

    def do_DutConsoleRead(self, paramTuple):
        if len(paramTuple) != 2: return (API.TER_Status_ArgumentCountError,)
        returnTuple = self.doSioCommand("TER_UartReceive", (1, paramTuple[0], paramTuple[1],))
        if len(returnTuple) == 3: return (returnTuple[0], returnTuple[2], returnTuple[1],)
        return returnTuple

    def do_DutConsoleReadLn(self, paramTuple):
        if len(paramTuple) != 2: return (API.TER_Status_ArgumentCountError,)
        timeoutMsecs = paramTuple[0]                           # Timeout passed in will define the "master" timeout across all calls to TER_UartReceiveLn()
        lowLevelTimeoutMsecs = min(timeoutMsecs,2000)          # Timeout passed to TER_UartReceiveLn() is clipped at 2 sec to avoid an invalid-parameter error
        requestedLines = paramTuple[1]
        linesRead = 0
        elapsedMsecs = 0
        tempBuf = ""
        unexpectedResponse = False
        startTime = datetime.datetime.now()
        while linesRead < requestedLines and elapsedMsecs < timeoutMsecs and not unexpectedResponse:
            linesToRead = requestedLines - linesRead           # Remaining lines to read is requested lines - lines read so far
            #print "Request: Lines = " + str(linesToRead) + "   Timeout  = " + str(lowLevelTimeoutMsecs)
            returnTuple = self.doSioCommand("TER_UartReceiveLn", (1, lowLevelTimeoutMsecs, linesToRead,))
            if len(returnTuple) == 3:
                if returnTuple[1] > 0:
                    linesRead += returnTuple[1]                # Add line count from latest read to total line count
                    tempBuf += returnTuple[2]                  # Append data from latest read to previous data
                elapsedMsecs = int((datetime.datetime.now() - startTime).total_seconds() * 1000)
                #print "Response: Lines = " + str(returnTuple[1]) + "  Elapsed msecs = " + str(elapsedMsecs)
            else:
                #print "Unexpected response:  Len of returnTuple = " + str(len(returnTuple))
                unexpectedResponse = True                      # Invalid returnTuple - bail out
        return (returnTuple[0], tempBuf, linesRead,)

    def do_DutConsoleStatus(self, paramTuple):
        if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError,)
        return self.doSioCommand("TER_UartGetStatus", (1,))

    # def do_DutConsoleLnStatus(self, paramTuple):
    #    if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError,)
    #    return self.doSioCommand("TER_UartGetStatus", (1,))

    # def do_DutConsoleSetReadLnPos(self, paramTuple):
    #     if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError,)
    #     return self.doSioCommand("TER_UartSetLnPosition", (1, paramTuple[0],))

    # def do_DutConsoleFillFromFile(self, paramTuple):
    #     if len(paramTuple) != 0: return (API.TER_Status_ArgumentCountError,)
    #     return self.doSioCommand("TER_UartFillFromFile", (1,))

    #working on these -Peter Emidy
    def do_DutConsoleSetReadPos(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError,)
        return self.doSioCommand("TER_UartSetPosition", (1, paramTuple[0],))



    def do_SetPowerVoltageTripPoint(self, paramTuple):
        paramTuple = paramTuple[:1] + (1,) + paramTuple[1:] + (0,)
        return self.doSioCommand("TER_SetPowerTripPoint", paramTuple)


    def do_SetPowerCurrentTripPoint(self, paramTuple):
        paramTuple = paramTuple[:1] + (2,) + paramTuple[1:]
        return self.doSioCommand("TER_SetPowerTripPoint", paramTuple)

    def do_SetPowerVoltageGoodRange(self, paramTuple):
        paramTuple = paramTuple[:1] + (4,) + paramTuple[1:]
        return self.doSioCommand("TER_SetPowerTripPoint", paramTuple)

    def do_GetPowerAveragingData(self, paramTuple):
        if len(paramTuple) != 4: return (API.TER_Status_ArgumentCountError)

        supply = paramTuple[0]
        units = paramTuple[1].lower()
        offset = paramTuple[2]
        count = paramTuple[3]

        if units == "mv": measurement = API.TER_PowerMeasurement_Volts
        elif units == "ma": measurement = API.TER_PowerMeasurement_Amps
        elif units == "mw": measurement = API.TER_PowerMeasurement_Watts
        else: return (False, "Expected parameter of 'mV', 'mA', or 'mW', not '%s'" % units, )

        retTuple = self.doSioCommand("TER_GetAveragingData", (supply, measurement, offset, count))
        if len(retTuple) != 3: return (API.TER_Status_Invalid_Response, 0)

        count = retTuple[1]

        try:
            data = struct.unpack("!%dl" % count, retTuple[2])
        except:
            return (API.TER_Status_Invalid_Response, 0)

        return (retTuple[0], count, data)


    def do_SetPowerAveragingDataStorageMode(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError)

        mode = paramTuple[0].lower()

        if mode == "wrap": mode = API.TER_StorageMode_Wrap
        elif mode == "stop": mode = API.TER_StorageMode_Stop
        else: return (False, "Expected parameter of 'wrap' or 'stop', not '%s'" % mode, )

        return self.doSioCommand("TER_SetStorageMode", (mode, ))

    def do_SetDutUsbChannel(self, paramTuple):
        if len(paramTuple) != 1: return (API.TER_Status_ArgumentCountError)

        channel = paramTuple[0].lower()
        if channel == "ap": setSignalParamTuple = (0x400, 0x400)
        elif channel == "fp": setSignalParamTuple = (0x400, 0x000)
        else: return (False, "Expected parameter of 'ap' or 'fp', not '%s'" % channel, )
        return self.doSioCommand( "TER_SetSignal", setSignalParamTuple)

    def do_RunSequence(self, paramTuple):

        MAX_SEQ_TIME = 10000

        #
        # Build the RunSequence parameter list.
        #
        commands = []
        sioParams = []

        cmdIndex = 0
        cmdCount = 0
        approxTime = 0
        status = API.TER_Status_none
        results = []

        for cmdTuple in paramTuple:

            cmdIndex += 1
            cmdCount += 1

            # Look up command.
            try:
                cmd = getattr(self, "Command" +  cmdTuple[0])(self)
            except:
                return (False, "Command %s not supported in RunSequence." % cmdTuple[0])

            commands.append(cmd)

            # Add command to RunSequence paramters.
            sioParams.append(API.cmdNameToIdx(cmd.name))

            # Add parameters to RunSequence parameters.
            for param in cmd.params(cmdTuple[1:]):
                sioParams.append(param)

            approxTime += cmd.approxTime_us

            if (not singleSioSequence and approxTime > MAX_SEQ_TIME) or cmdIndex == len(paramTuple):

                #
                # Run the sequence.
                #
                sioParams.insert(0, cmdCount)
                startTime = time.time()
                sioResult = self.doSioCommand("TER_RunSequence", tuple(sioParams))
                self.sequenceDuration = time.time() - startTime

                #
                # Process the results.
                #

                # Add the overall status.
                if status == API.TER_Status_none and sioResult[0] != API.TER_Status_none:
                    status = API.TER_Status_none

                sioIndex = 1

                # Add results for each command.
                for cmd in commands:
                    if sioIndex >= len(sioResult):
                        break

                    # Add the command status.
                    count = sioResult[sioIndex]
                    sioIndex += 1

                    # Add the command return values.
                    result = cmd.result(sioResult[sioIndex : sioIndex + count])
                    results.append(self.setResults(result))
                    sioIndex += count

                # Reset command.
                commands = []
                cmdCount = 0
                sioParams = []
                approxTime = 0


        # Return as a tuple.
        results.insert(0, status)
        return tuple(results)



    def do_ConnectUsb(self, paramTuple):
        if paramTuple[0] == "Appl":
            setSignalParamTuple = ( 0x400, 0x000)
        elif paramTuple[0] == "FP":
            setSignalParamTuple = ( 0x400, 0x400)
        else:
            return API.TER_Status_Error_Argument_Invalid

        return self.doSioCommand( "TER_SetSignal", setSignalParamTuple)


    def dispatch(self, method, params):
        mname = 'do_' + method


def reset_timer():
    global __startTime__
    __startTime__= time.time()


if __name__ == "__main__":
    startTime = time.time()

    # Get Command Line arguments
    clParser = optparse.OptionParser()
    clParser.add_option("-d", "--debug", action="store_true", default=False, dest="isDebug",\
                        help='Provide addition debug information')
    clParser.add_option("-v", "--verbose", action="store_true", default=False, dest="isVerbose", \
                        help='Provide addition debug information')
    clParser.add_option("-s", "--slot", type="int", dest="slotIdx", default=None,\
                        help="Specify Slot index 1..140")
    clParser.add_option("-i", "--ip-address", default=None, dest="ipAddress", \
                        help='Specify IP address, e.g., 127.0.0.1')
    clParser.add_option("--port", type="int", default=None, dest="port", \
                        help='Specify IP Port, e.g., 13000')
    clParser.add_option("-t", "--timeout", type = int, default=None, dest="timeoutInMs", \
                        help='Specify SIO timeout in milliseconds')
    clParser.add_option("--serverMode", action="store_true", default=False, dest="serverMode",\
                        help='Run in server mode')
    clParser.add_option("--serverIP", default="0.0.0.0", dest="serverIP", \
                        help='Specify IP address to run server on, e.g., 192.168.1.1')
    clParser.add_option("--serverPort", type="int", default=60005, dest="serverPort", \
                        help='Specify IP Port to run server on, e.g., 60005')

    (options,args) = clParser.parse_args()

    if options.serverMode:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((options.serverIP, options.serverPort))
        serversocket.setblocking(1)
        serversocket.listen(5)
        if options.isDebug:
            print('Server has started at' +options.serverIP+':'+options.serverPort+'\n')

        while 1:
            try:
                #if options.isDebug:
                #    print 'Waiting for client connection at', options.serverIP,':',options.serverPort,'...'
                clientsocket, address = serversocket.accept()
                __startTime__= time.time()
            except Exception as e:
                #if options.isDebug:
                print(type(e).__name__+"Exception in server thread:")
                print(traceback.format_exc())
                serversocket.close()
                break
            else:
                newClientTread = ClientHandler(clientsocket, options.isDebug)
                newClientTread.start();
    else:
        commandString = "GetSiteInfo"

        for string in args:
            commandString += string + " "
        
        print("cmd :",commandString, options.ipAddress)
        result = sioRun( commandString, options.slotIdx, options.ipAddress, options.port, options.isDebug, options.isVerbose, options.timeoutInMs)

        if options.isDebug:
            print("SIO elapsed time: %3.3f ms" % ((time.time() - startTime) * 1.0e3,))
            print("Total elapsed time: %3.3f ms" % ((time.time() - __startTime__) * 1.0e3,))

        print(result)
