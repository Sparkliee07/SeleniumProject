'''
Copyright (c) 2010 Teradyne, Inc. All rights reserved. 
Created on Nov 12, 2010

@author: Peter Reichert
'''


import marshal
import os
import select
import socket
import struct
import sys
import time
import traceback
from threading import Thread
import sioApi as API
import sio

if sys.platform == "win32":
    OUT_FILE_PATH = ""
else:
    # Must have slash at the end so I can have the win32 path
    OUT_FILE_PATH = "/var/tmp/" 



MARSHAL_VERSION = 0
SIZE_SIZE = 4           # Size of size integers in bytes

def CreateMessate(tuple):
    """
    Take a MRPC tuple and convert it to a binary message.
    This works for both command and response messages.  
    """
    #message = marshal.dumps(tuple, MARSHAL_VERSION)
    #msgSize = struct.pack("<I", len(message)  + SIZE_SIZE)
    #message = "".join(msgSize,message,)

    # Serialize the tuple using marshal
    message = marshal.dumps(tuple, MARSHAL_VERSION)
    # Pack the message size (4 bytes, unsigned integer in little-endian format)
    msgSize = struct.pack("<I", len(message) + struct.calcsize("<I"))
    # Concatenate the size and the message
    message = msgSize + message
    return message


def ExtractFromMessage( messageString ):
    """
    Take a MRPC message received over the wire and extract the tuple representing
    the data.
    This works for both command and response.
    """
    messageSize = len(messageString)
    message = messageString[4:]
    _eventTuple = marshal.loads(message)
#     self.msg = "%s bytes, %s, raw: %s" % (self.messageSize, self._eventTuple, repr(self.message))
#     print self.msg
    return _eventTuple

class MRPCError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class MRPCProtocol(object):
    LONG_TIMEOUT_TIME = 35.0    # Like all python time, this is in seconds.
    SHORT_TIMEOUT_TIME = 10.0   # Like all python time, this is in seconds.

    def __init__(self, port=None, address=None, debug=False, isProduction=False, dueTime=None, isFP=False):

        self.dueTime = dueTime
        self.startTime = time.time()
        self.isProduction = isProduction
        # Highest priority is to use a specified address. If not specified
        # If not specified:
        if not address:
            try:
                # Use environment variable for IP address if available:
                address = os.environ["SIOIPADDRESS"]
            except KeyError:
                # Finally, if not specified, and no environment variable, use the old standby:
                #address = '192.168.129.101'
                address = '192.168.1.201'

        address = address.replace( " ", "")   # Get rid of leading / trailing space!

        if not port:
            port = 13000
            
        portAddress = (address, port)

        self.portAddress = portAddress  # a (ipaddress, port) tuple
        self.timeStamp = "no time"
        self.debugMode = debug
        self.sendInProgress = False
        self.startTime = 0
        self.debugStr = ""
        self.sioVariant = sio.UNKNOWN_VARIANT
        self.sioBoard = sio.UNKNOWN_BOARD
        self.sioPartNumber = "000-000-00"

        try:
            self.open()
        except:
            if self.debugMode:
                traceback.print_exc()
            raise
    
        self.historyFile = None
        self.sendFile = None
        if self.debugMode:
            timeStr = repr(int(time.time()))
            fileName = OUT_FILE_PATH + 'mrpcCmdHistory' + timeStr
            self.historyFile = file(fileName, 'w')
            fileName = OUT_FILE_PATH + 'mrpcSendHistory' + timeStr
            self.sendFile = file(fileName, 'w')
            
        # Learn some things about the SIO:
        self.__api = API.SioApi(self, 1)
        if not isProduction and not isFP:
            self.getSioInfo()  # TODO: (I don't like things talking to the SIO behind my back, but I like the convenience...)

    def reconnect(self):
        """
        When a connection is dropped or messed up, this will reconnect.
        """
        self.close()
        self.open()
        self.getSioInfo()
        self.sendInProgress = False   # Can't be a send in progress if we close the socket!
        
        
    def open(self):
        try:
            if self.debugMode:
                print ("Opening" , self.portAddress)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(self._shortTimeoutTime())
            self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.s.connect(self.portAddress)
        except Exception:
            #raise MRPCError("Module: %s, could not connect to %s" %(__name__, repr(self.portAddress)) )
            raise MRPCError(f"Module: {__name__}, could not connect to {repr(self.portAddress)}")

    def close(self):
        if hasattr(self, "s"):
            self.s.close()
            del self.s
    
    def __del__(self):
        self.cleanup()

    def _raiseTimeoutError(self):
        if self.dueTime is None:
            msg = "ERROR -- Timeout.  Start time = %2.3f.  Current time = %2.3f.  Elapsed time = %2.3f." % \
                  (self.startTime, time.time(), time.time() - self.startTime)
        else:
            msg = "ERROR -- Timeout.   Start time = %2.3f.  Due Time = %2.3f. Current time = %2.3f." %\
            (self.startTime, time.time(), time.time() - self.startTime)
        raise MRPCError( msg )

    def _shortTimeoutTime(self):
        """
        :return: a timeout that is seconds that is 10 seconds or shorter
        This is for operations like connecting or
        reading received data of a socket.  It is expected that the customer may spec a total timeout that is less
        than 10 seconds, and they understand the risks.
        """
        timeout = self._timeoutTime()
        return min(timeout, self.SHORT_TIMEOUT_TIME)

    def _timeoutTime(self):
        """
        :return: A timeout value in seconds.
        """
        if self.dueTime is None:
            return self.LONG_TIMEOUT_TIME
        else:
            if (self.dueTime <= time.time()):
                self._raiseTimeoutError()
            return self.dueTime - time.time()

    def cleanup(self):
        self.close()
        if hasattr(self, "sioThread"):
            del self.sioThread
        if self.debugMode:
            if hasattr(self, "historyFile"):
                self.historyFile.close()
            if hasattr(self, "sendFile"):
                self.sendFile.close()

    def getSioInfo(self):
        # Default:
        self.sioPartNumber = None
        self.sioVersionNumber = None
        try:
            result = self.__api.TER_GetSioInfo()
            if len(result) >= 1:
                self.sioVersionNumber = result[1]

            # TODO: This really needs help!  Should read 4 and see if it is a part number.  If not (an FPGA version), read 7.
            if len(result) >  7:
                self.sioVersionNumber = result[1]
            if len(result) >  7:
                self.sioPartNumber = result[7]
            elif len(result) > 4:
                self.sioPartNumber = result[4]
                
        except:
            print ("ERROR -- TER_GetSioInfo call failed, TER_Status = %d" % self.__api.getLastStatus())
            traceback.print_exc()
            
        # Set variant and type
        if self.sioPartNumber == sio.QUALCOMM_TITAN_PART_NUMBER:
            self.sioVariant = sio.QUALCOMM_TITAN_VARIANT
            self.sioBoard = sio.SIO6_BOARD

        elif self.sioPartNumber[:8] == sio.QUALCOMM_MAGNUS_PART_NUMBER[:8] or self.sioPartNumber == "111-111-11" or self.sioPartNumber[:8] == sio.QUALCOMM_MAGNUS_PART_NUMBER_PCA9554A[:8]:
            self.sioVariant = sio.QUALCOMM_MAGNUS_VARIANT
            self.sioBoard = sio.SIO6_BOARD

        elif self.sioPartNumber == sio.GUMSTICK_SIO2_PART_NUMBER:
            self.sioVariant = sio.GUMSTICK_VARIANT
            self.sioBoard = sio.SIO2_BOARD

        elif self.sioPartNumber == sio.WD_SIO2_PART_NUMBER:
            self.sioVariant = sio.WD_VARIANT
            self.sioBoard = sio.SIO2_BOARD           

        elif self.sioPartNumber == sio.TOSHIBA_SIO2_PART_NUMBER:
            self.sioVariant = sio.TOSHIBA_VARIANT
            self.sioBoard = sio.SIO2_BOARD           

        elif self.sioPartNumber == sio.HITACHI_SIO3_PART_NUMBER0:
            self.sioVariant = sio.HITACHI_VARIANT
            self.sioBoard = sio.SIO3_BOARD

        elif self.sioPartNumber == sio.HITACHI_SIO3_PART_NUMBER1:
            self.sioVariant = sio.HITACHI_VARIANT
            self.sioBoard = sio.SIO3_BOARD

        elif self.sioPartNumber == sio.WD_SIO4_PART_NUMBER0:
            self.sioVariant = sio.WD_VARIANT
            self.sioBoard = sio.SIO4_BOARD
            
        elif self.sioPartNumber == sio.WD_SIO4_PART_NUMBER1:
            self.sioVariant = sio.WD_VARIANT
            self.sioBoard = sio.SIO4_BOARD
                
        elif self.sioPartNumber == sio.WD_SIO5_PART_NUMBER0:
            self.sioVariant = sio.WD_VARIANT
            self.sioBoard = sio.SIO4_BOARD

        elif self.sioPartNumber == sio.WD_SIO5_PART_NUMBER1:
            self.sioVariant = sio.WD_VARIANT
            self.sioBoard = sio.SIO4_BOARD
                
        elif self.sioPartNumber == sio.HITACHI_LC_PART_NUMBER:
            self.sioVariant = sio.HITACHI_LC_VARIANT
            self.sioBoard = sio.RM2_BOARD

        elif self.sioPartNumber == sio.HITACHI_HD_PART_NUMBER0:
            self.sioVariant = sio.HITACHI_HD_VARIANT
            self.sioBoard = sio.SIO5_BOARD

        elif self.sioPartNumber == sio.HITACHI_HD_PART_NUMBER1:
            self.sioVariant = sio.HITACHI_HD_VARIANT
            self.sioBoard = sio.SIO5_BOARD

        elif self.sioPartNumber == sio.SEAGATE_SIO2_PART_NUMBER:
            self.sioVariant = sio.SEAGATE_VARIANT
            self.sioBoard = sio.SIO2_BOARD

        elif not self.sioPartNumber:
            print ("ERROR -- No SIO Part Number.")
            self.sioVariant = sio.QUALCOMM_TITAN_VARIANT
            self.sioBoard = sio.SIO6_BOARD

        else:
            print ("ERROR -- Unrecognized SIO Part Number: %s" % self.sioPartNumber)
            self.sioVariant = sio.QUALCOMM_TITAN_VARIANT
            self.sioBoard = sio.SIO6_BOARD

        print ("SIO Variant: %s, SIO Board: %s" % (self.sioVariant, self.sioBoard,))

    def _sendMessage(self, cmdIdx, slotIdx, params):
        # Add the timestamp to the message - we'll validate this in the response too.
        # Adding 62135596800 takes us back to year 1, multipling by 1e7 converts to
        # 100ns resolution, which is the .net / Microsoft standard.
        msTime = (time.time() + 62135596800) * 1e7
        newTimeStamp = struct.pack('<Q', int(msTime))
#        print "msTime = 0x%016x, timestamp = %s" % (int(msTime), repr(newTimeStamp)) 
        if sys.platform != 'win32':  # Windows does not like the following line:
            if newTimeStamp==self.timeStamp: raise Exception("Duplicate timestamp")
        self.timeStamp = newTimeStamp
        if self.debugMode:
            cmdName = API.cmdIdxToName(cmdIdx)
            self.debugStr += '\n' + cmdName + repr(params)
            if cmdName == "TER_SioSendBuffer":
                self.sendStr += 'SEND ' + repr(len(params[0])) + ' bytes ---> ' + repr(params[0])+ '--->\n'
        messageTuple = (cmdIdx,slotIdx,self.timeStamp,) + params
        message = CreateMessate(messageTuple)
        if self.debugMode:
            self.debugStr += '\n\tSent: %s\n' % repr(messageTuple)
            self.debugStr += '\n\tSent: %s\n' % repr(message)
        response = self.s.sendall(message)
        self.lastSendTuple = messageTuple
        self.lastSendMsg = message
        if response:
            if self.debugMode:
                self.debugStr += '\nERROR -- sendall() returned other than None: %s' % repr(response)

    #   R E C E I V E
    #   A copy of Stuart's receive
    def _receive(self, sock, responseSize, flags=0):
        sizeLeft = responseSize
        response = ''
        sock.settimeout(self._timeoutTime())
        while sizeLeft:
            timeout = self._timeoutTime()
            r, w, x = select.select([sock], [], [], timeout)
            if sock in r:  
                try:
                    dataIn = sock.recv(sizeLeft,flags)
                except:
                    print('Exception on API method')
                    print("Size Left", sizeLeft)
                    traceback.print_exc()
            else:
                raise MRPCError("ClientSocketTimeout sock: %s  responseSize: %s  timeout: %2.3f  sizeLeft: %s  response: %s  %s" % (sock,responseSize,timeout,sizeLeft,response,self.s.getsockname(),))
            if not dataIn:
                raise Exception("ClientNoDataIn  %s" % (self.s.getsockname(),))
            response += dataIn
            sizeLeft = responseSize - len(response)
        
        if self.debugMode:
            self.debugStr += '\n\tRecv: %s\n' % repr(response)
            
        return response          

    def _logLastCommand(self):
        logStr = "Last command:\n\t\t%s:%s\n\t\t%s\n" %\
         (API.cmdIdxToName(self.lastSendTuple[0]), self.lastSendTuple, repr(self.lastSendMsg))
        print(logStr)
        

    def _readDataFromSocket(self):
        dataIn = self._receive(self.s, SIZE_SIZE)
        numBytes, = struct.unpack("<I", dataIn) # Interpret as little endian integer.
        #if numBytes > 70000L:
        if numBytes > 70000:
            print ("WARNING Large sizeIn (%d) in MRPCProtocol.py  %s" % (numBytes, self.s.getsockname()))
            print ("\tDataIn = %s" % repr(dataIn))
            self._logLastCommand()
            messageString = "\x04\x00\x00\x00"
        else:
            messageString = dataIn
            dataIn = self._receive(self.s, numBytes - SIZE_SIZE)    # TODO: I used to use "shortTimeout" here.  That no longer works with new timeout scheme. May be moot as new scheme tyically allows shorter timeouts
            messageString += dataIn # TODO: Need to drain the receive buffer....
        return messageString

    def _checkDataFromSocket(self, dataIn ):
        # TODO: Shouldn't this throw an exception?
        numBytes, = struct.unpack("<I", dataIn[0:4]) # Interpret as little endian integer.
        if len(dataIn) != (numBytes):
            self._logLastCommand()
            msg = "Module: %s: Response data size error.  size: %d, actual size: %d" %(__name__, numBytes, len(dataIn)) 
            raise MRPCError( msg )
        
    def _checkResponseFromServer(self, responseTuple ):
        """
        The slotIdx, commandIdx and time stamp must match
        """
        for i in range(3):
            if (responseTuple[i+1] != self.lastSendTuple[i]):
                msg = "Response doesn't match send:  response(%d) = %s but send(%d) = %s" % \
                (i+1, repr(responseTuple[i+1]), i, repr(self.lastSendTuple[i]))
                raise MRPCError(msg)


    def _receiveMessage(self):
        # TODO:  This is a quick and dirty receive.  Better to wait on socket with a select?
        #dataIn = self.s.recv(SIZE_SIZE)
        messageString = self._readDataFromSocket()
        self._checkDataFromSocket(messageString)
        try:
            response = ExtractFromMessage( messageString )
        except EOFError:
            msg = "ERROR -- EOFError in marshal.loads.  dataIn = %s" % (repr(messageString),)
            self._logLastCommand()
            raise MRPCError(msg)
        except:
            msg = "ERROR -- marshal.loads.  dataIn = %s" % (repr(messageString),)
            self._logLastCommand()
            raise MRPCError(msg)
        if self.debugMode:
            self.debugStr += '\tReceived:' + repr(response) + '\n'
            if response[1] == API.cmdNameToIdx("TER_SioReceiveBuffer"):
                self.sendStr = 'RECV ' + repr(len(response[5])) + ' bytes <--- ' + repr(response[5]) + '<---\n'
        return response

    def clientReceiveMessage(self):
        """
        Read the socket and process the data as if we are a MRPC client.
        We check and filter out the first 4 items in the response tuple:
        OK, cmdIndes, SlotIndex, Timestamp.
        
        """
        responseTuple = self._receiveMessage()
        if responseTuple[0] != "OK":
            msg = "MRPC ERROR -- Non-OK response = %s" %  (responseTuple,)
            self._logLastCommand()
            raise MRPCError(msg)
        
        self._checkResponseFromServer( responseTuple )
        return responseTuple[4:]   # Skip OK, cmdIdx, slotIdx, timestamp)

    def serverReceiveMessage(self):
        """
        Read the socket and process the data as if we are a MRPC server.
        """
        responseTuple = self._receiveMessage()
        return responseTuple

    def sendMessage(self, cmdIdx, slotIdx, params):
        if self.debugMode:
            self.debugStr = ""
            self.sendStr = ""
            self.startTime = time.time()
        self._sendMessage(cmdIdx, slotIdx, params)
        return
        
    def receiveMessage(self):
        result = self.clientReceiveMessage()
        if self.debugMode:
            endTime = time.time()
            elapsedTime = endTime-self.startTime
            self.debugStr += "\t" + repr(elapsedTime)
            if hasattr( self, "historyFile"):
                self.historyFile.write(self.debugStr)
            if hasattr( self, "sendFile"):
                self.sendFile.write(self.sendStr)
                
        return result

    def sendReceiveMessageThread(self):
        while self.sendInProgress:
            time.sleep(0.5)

        self.sendInProgress = True
        self.sendMessage(self.cmdIdx, self.slotIdx, self.cmdParams)
        self.result = self.receiveMessage()
        self.sendInProgress = False
        
    def sendReceiveMessage(self, cmdIdx, slotIdx, params):
        """
        Use a thread to talk to the SIO to make it atomic.  I don't
        want the send/receive sequence to ever be interrupted.
        
        Looks like I commented out the actual thread bit, but we need 
        too keep track of the sendInProgress flag!
        """
        while hasattr(self, "sioThread"):
            print("WARNING: Deleting thread  ",)
            del self.sioThread
        if self.sendInProgress:
            print("WARNING: sendInProgress = ", self.sendInProgress)
            return
        self.result = (-1,)
        self.cmdIdx = cmdIdx
        self.slotIdx = slotIdx
        self.cmdParams = params
        
        # Actually do the send / receive:
        self.sendReceiveMessageThread()
#        self.sioThread = Thread(target=self.sendReceiveMessageThread)
#        self.sioThread.start()
#        self.sioThread.join(timeout=60)  #TODO Rationalize with MRPC timeout
#        if self.sendInProgress:
#            print "WARNING: sendReceiveMessageThread() timed out. Reopen socket"
#            self.close()
#            time.sleep(10) # Give the SIO some time
##            self.open()
#            self.sendInProgress = False
#        del self.sioThread
#        print "sendInProgress = ", self.sendInProgress
#        print "Has sioThread =" , hasattr(self, "sioThread")
        return self.result 

    def getLastDebugStr(self):
        return self.debugStr
    
    def getIpAddress(self):
        return self.portAddress[0]
    
    def getIpPort(self):
        return self.portAddress[1]

    def extendDueTime(self, extensionTime):
        """
        If this class was initiated with a dueTime, we are running against a clock.  Typically this is done for
        a single command.  There are some commands, well one, which have thier own timeout.  We want to extend
        the dueTime for such commands.  This method provides a way for those commands to do this.

        :param extensionTime:  Number of seconds to exted the dueTime of MPRC operations
        :return:
        """
        if self.dueTime is not None:
            self.dueTime += extensionTime


if __name__ == "__main__":
    t = (0, "timeStamp", 1)
    print("Send: ", t)
    message = CreateMessate( t )
    tuple = ExtractFromMessage(message)
    
    print ("Message: ", repr(message))
    print ("Tuple: ", repr(tuple))
    if t == tuple:
        print ("PASS")
    else:
        print ("FAIL")
    
