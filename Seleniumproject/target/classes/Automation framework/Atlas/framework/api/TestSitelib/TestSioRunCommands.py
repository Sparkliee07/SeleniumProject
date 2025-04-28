import sioRunner as sio
import time
import optparse


if __name__ == "__main__":
    startTime = time.time()

    # Get Command Line arguments
    clParser = optparse.OptionParser()
    clParser.add_option("-d", "--debug", action="store_true", default=False, dest="isDebug", \
                        help='Provide addition debug information')
    clParser.add_option("-v", "--verbose", action="store_true", default=False, dest="isVerbose", \
                        help='Provide addition debug information')
    clParser.add_option("-s", "--slot", type="int", dest="slotIdx", default=1, \
                        help="Specify Slot index 1..140")
    clParser.add_option("-i", "--ip-address", default='192.168.1.9', dest="ipAddress", \
                        help='Specify IP address, e.g., 127.0.0.1')
    clParser.add_option("--port", type="int", default=None, dest="port", \
                        help='Specify IP Port, e.g., 13000')
    clParser.add_option("-t", "--timeout", type=int, default=None, dest="timeoutInMs", \
                        help='Specify SIO timeout in milliseconds')
    clParser.add_option("--serverMode", action="store_true", default=False, dest="serverMode", \
                        help='Run in server mode')
    clParser.add_option("--serverIP", default="0.0.0.0", dest="serverIP", \
                        help='Specify IP address to run server on, e.g., 192.168.1.1')
    clParser.add_option("--serverPort", type="int", default=60005, dest="serverPort", \
                        help='Specify IP Port to run server on, e.g., 60005')

    (options, args) = clParser.parse_args()

    commandString ='GetSiteInfo'
    print(commandString)
    
    print(options.slotIdx, options.ipAddress, options.port, options.isDebug, options.isVerbose, options.timeoutInMs)

    result = sio.sioRun( commandString, options.slotIdx, options.ipAddress, options.port, options.isDebug, options.isVerbose, options.timeoutInMs)

    if options.isDebug:
        print("SIO elapsed time: %3.3f ms" % ((time.time() - startTime) * 1.0e3,))
        print(result)