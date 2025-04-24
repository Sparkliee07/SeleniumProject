'''
Created on Nov 13, 2010

@author: reichert
'''
try:
    import dioCommand
except:
    pass


_cmdNameToIdxDict = {
               # basic commands:
              'TER_Reset'                       : 1001,
              'TER_SetPowerEnable'              : 1002,
              'TER_SetSerialParameters'         : 1003,
              'TER_SetSerialEnable'             : 1004,
              'TER_SioSendBuffer'               : 1005,
              'TER_SioReceiveBuffer'            : 1006,

               # Slot status / health:
              'TER_IsSlotThere'                 : 1007,
              'TER_GetSlotInfo'                 : 1008,
              'TER_GetSlotSettings'             : 1009,
              'TER_GetSlotStatus'               : 1010,
              'TER_GetUserString'               : 1011,
              'TER_SetUserString'               : 1012,

               # More elaborate commands:
              'TER_SetTempControlEnable'        : 1013,
              'TER_SetTargetTemperature'        : 1014,
              'TER_SetPowerVoltage'             : 1015,
              'TER_SetSerialLevels'             : 1016,
              'TER_SetSerialSelect'             : 1017,
              'TER_SetSignal'                   : 1018,
              'TER_PulseSignal'                 : 1019,
              'TER_SioSendReceiveBuffer'        : 1020,
              'TER_GetSerialSelect'             : 1021,
              'TER_Debug'                       : 1024,
              'TER_Measure'                     : 1025,
              'TER_GetSioInfo'                  : 1026,
              'TER_GetCachedSlotInfo'           : 1027,
              'TER_SetSerialPinout'             : 1028,  
              'TER_SetThermalType'              : 1029,
              'TER_UserDiag'                    : 1030,
              'TER_GetCachedPackInfo'           : 1032,
              'TER_GetCarrierInfo'              : 1033,
              'TER_GetDutInfo'                  : 1034,
              'TER_Sync'                        : 1035,
              'TER_GetFpInfo'                  : 1044,
              # Extended DUT communications.
              'TER_SpiSendReceive'              : 1036,
              'TER_JtagSendReceive'             : 1037,
              'TER_UartSendBuffer'              : 1038,
              'TER_UartReceiveBuffer'           : 1039,

              # Titan DUT communications.
              'TER_UartReceiveLn'               : 1040,
              'TER_UartGetStatus'               : 1041,
              'TER_UartSetPosition'             : 1042,
              'TER_UartReceive'                 : 1043,

              # Magnus Power APIs
              'TER_SetPowerBounds'              : 1045,
              'TER_SetPowerTripPoint'           : 1046,
              'TER_ResetAveraging'              : 1047,
              'TER_GetAveragingInfo'            : 1048,
              'TER_GetAveragingData'            : 1049,
              'TER_SetStorageMode'              : 1050,
              'TER_SetFpInfo'                   : 1051,
              'TER_SetSampleRate'               : 1052,

              # Magnus manufacturing info
              'TER_GetMfgInfo'                  : 1053,
              'TER_ReadEeprom'                  : 1054,
              'TER_WriteEeprom'                 : 1055,

              # Switch board info
              'TER_GetSbStatus'                 : 1056,
              'TER_GetSbInfo'                   : 1057,

              # Sequences
              'TER_RunSequence'                 : 1061,


              # Appliance info & status

              'TER_GetApplBiosInfo'				: 1202,
              'TER_GetApplOsInfo'				: 1203,
              'TER_GetApplHwInfo'				: 1204,
              'TER_GetApplNvmeDriveInfo'		: 1205,
              'TER_GetApplNvmeDriveStatus'		: 1206,
              'TER_GetApplSwitchBoardStatus'	: 1207,
              'TER_GetApplUsbStatus'			: 1208,
              'TER_ApplianceSltDownloaderStart'	: 1209,
              'TER_ApplianceSltDownloaderStart'	: 1210,

              'TER_ApplianceReset'			    : 2001,
              'TER_ApplianceStartSession'	    : 2003,
              'TER_ApplianceEndSession'		    : 2004,
              'TER_ApplianceGetTestStatus'	    : 2006,
              'TER_ApplianceRunPatternTest'	    : 2007,
              'TER_ApplianceRunPatternTestList'	: 2008,



              # Private Teradyne Commands:
              'TER_DioCmd'                      : 0x01000000,
              'TER_DioMultiCmd'                 : 0x01000001,
              'TER_WriteFpgaRegisters'          : 0x01000002,
              'TER_ReadFpgaRegisters'           : 0x01000003,
              'TER_SioPing'                     : 0x01000004,
              'TER_SioReboot'                   : 0x01000005,
              'TER_WriteFpgaField'              : 0x01000006,
              'TER_SetProperty'                 : 0x01000007,
              'TER_StartTest'                   : 0x01000008,
              'TER_StopTest'                    : 0x01000009,
              'TER_GetTestStatus'               : 0x01000010,
              'TER_GetSlotUpgradeStatus'        : 0x01000011,
              'TER_UpgradeSlot'                 : 0x01000012,
              'TER_SliceCmd'                    : 0x01000013,
              'TER_SetSafeHandlingEnable'       : 0x01000014,
              'TER_SetTargetPort'               : 0x01000015,
              'TER_AdjustTartgetTemperature'    : 0x01000016,
              'TER_GetRawSio4Info'              : 0x01000017,
              'TER_GetProperty'                 : 0x01000018,
              'TER_Do'                          : 0x01000019,
              'TER_InitializeCarrier'           : 0x01000020,
              'TER_SlicePing'                   : 0x01000021,
              'TER_StartRxTxTest'               : 0x01000022,
              'TER_WriteFpga'                   : 0x01000023,
              'TER_ReadFpga'                    : 0x01000024,
              'TER_ReadMemory'                  : 0x01000025,
              'TER_WriteMemory'                 : 0x01000026,
              'TER_PexRegisterRead'             : 0x01000027,
              'TER_PexRegisterWrite'            : 0x01000028,
              'TER_WriteConsole'                : 0x01000029,

              'CalGetCameraPose'                : 2002,
              'GetLastError'                    : 1,

    'AcqLiveMode' : 1001,
    'AcqImage' : 1002,
    'AcqGetDevices' : 1003,
    'AcqOpenDevice' : 1004,
    'AcqCloseDevice' : 1005,
}

_cmdIdxToNameDict = {}

for name in _cmdNameToIdxDict.keys():
    _cmdIdxToNameDict[_cmdNameToIdxDict[name]] = name


def getCommandNames():
    return _cmdNameToIdxDict.keys()

def cmdIdxToName(cmdIdx):
    return _cmdIdxToNameDict[cmdIdx]

def cmdNameToIdx(cmdName):
    return _cmdNameToIdxDict[cmdName]

TER_Status_none = 0
TER_Status_dio_timeout = 1
TER_Status_no_client_connection = 2
TER_Status_slotid_error = 3
TER_Status_InvalidMode = 4
TER_Status_Error_Argument_Invalid = 5
TER_Status_receive_packet_len_err = 6
TER_Status_HW_Timeout_Error = 7
TER_Status_OvertempError = 8
TER_Status_Send_Receive_Error = 9
TER_Status_I2cError                     = 10
TER_Status_CarrierNotPresent            = 11
TER_Status_CarrierInfoNotAvailable      = 12
TER_Status_file_not_found = 13
TER_Status_ucode_update_errors = 16
TER_Status_Buffer_Overflow = 18
TER_Status_ArgumentCountError= 19
TER_Status_rpc_fail = 22
TER_Status_Timeout = 23
TER_Status_NotImplemented = 24
TER_Status_Read_Only_Value = 25
TER_Status_Unknown_Pseudo_Addr = 26
TER_Status_Invalid_Baud_Rate = 27
TER_Status_Invalid_Stop_Bits = 28
TER_Status_ucode_upgrade_busy = 31
TER_Status_SlotNeedsUpgrade = 32
TER_Status_ucode_file_too_big = 33
TER_Status_UpgradeInfoMissing = 34
TER_Status_high_ucode_ugrade_cnt = 35
TER_Status_DIO_STATUS_timed_out = TER_Status_dio_timeout
TER_Status_DIO_STATUS_no_dio  = 38
TER_Status_DIO_STATUS_slotid_out_of_range = TER_Status_slotid_error
TER_Status_DIO_STATUS_retrys_exhausted = 41
TER_Status_DIO_STATUS_command_drained = 43
TER_Status_DIO_STATUS_response_out_of_seq = 44
TER_Status_DIO_STATUS_dio_reported_error = 45
TER_Status_DIO_STATUS_command_mismatch = 46
TER_Status_DIO_STATUS_dio_rx_cksum_error = 47
TER_Status_DIO_STATUS_force_25msec_error = 48
TER_Status_64k_count_exceeded = 49
TER_Status_transmitter_is_halted = 50
TER_Status_HTemp_Sled_Temperature_Fault = 51
TER_Status_HTemp_Max_Adjustment_Reached = 52
TER_Status_HTemp_Min_Adjustment_Reached = 53
TER_Status_DctNotReadyToStart = 54
TER_Status_DctAlreadyStarted = 55
TER_Status_DctNotStarted = 56

TER_Status_Send_Receive_Timeout = 57
TER_Status_Invalid_Response = 58

# Slice Stuff
TER_Status_SliceNotReady = 59
TER_Status_SliceTimout = 60
TER_Status_SliceSendMessageError = 61
TER_Status_SliceMessageQueueFull = 62
TER_Status_RefuseToStart = 64


TER_Status_JtagGeneralFailure	 = 67
TER_Status_PowerSetupIncomplete	 = 68
TER_Status_Faulted               = 69
TER_Status_NoData                = 70
TER_Status_I2cBusy               = 71
TER_Status_AggregateError        = 72


#TODO: Build reverse dictionary.
_TER_NotifierDict = {
    'TER_Status_none'               : TER_Status_none,
    'TER_Status_ucode_upgrade_busy' : TER_Status_ucode_upgrade_busy,
    "TER_Status_dio_timeout"        : TER_Status_dio_timeout,
    "TER_Status_slotid_error"       : TER_Status_slotid_error,
}

_statusStrings = {
    TER_Status_none                 : "TER_Status_none",
    TER_Status_ucode_upgrade_busy   : "TER_Status_ucode_upgrade_busy"
}


TER_Status_Meanings = {
    TER_Status_none                             : "",    # Qualcomm requires that success be an empty string
    TER_Status_dio_timeout                      : "DIO time out",
    TER_Status_slotid_error                     : "Illegal Slot Index value",
    TER_Status_Error_Argument_Invalid           : "Bad argument",
    TER_Status_file_not_found                   : "File not found",
    TER_Status_Buffer_Overflow                  : "Buffer Overflow",
    TER_Status_ArgumentCountError               : "Wrong number of arguments",
    TER_Status_rpc_fail                         : "RPC failure",
    TER_Status_Timeout                          : "SIO Timeout",
    TER_Status_NotImplemented                   : "Command Not Implemented",
    TER_Status_Read_Only_Value                  : "Internal: Read only register",
    TER_Status_Unknown_Pseudo_Addr              : "Internal: Unknown register",
    TER_Status_Invalid_Baud_Rate                : "Invalid Baud Rate",
    TER_Status_Invalid_Stop_Bits                : "Invalid Number of Stop Bits",
    TER_Status_ucode_upgrade_busy               : "Upgrade busy",
    TER_Status_SlotNeedsUpgrade                 : "Internal unrecognized DIO command",  # ???
    TER_Status_ucode_file_too_big               : "Upgrade file too big",
    TER_Status_high_ucode_ugrade_cnt            : "Too many failed upgrade attempts",
    TER_Status_DIO_STATUS_retrys_exhausted      : "DIO retries exhausted",
    TER_Status_DIO_STATUS_response_out_of_seq   : "DIO response is out of sequence",
    TER_Status_DIO_STATUS_dio_reported_error    : "DIO reported error",
    TER_Status_DIO_STATUS_command_mismatch      : "DIO command mismatch",
    TER_Status_DIO_STATUS_dio_rx_cksum_error    : "DIO checksum error",
    TER_Status_JtagGeneralFailure               : "JTAG failure",
    TER_Status_PowerSetupIncomplete             : "Power setup incomplete",
    TER_Status_Faulted                          : "Faulted",
    TER_Status_NoData                           : "No data",
    TER_Status_I2cBusy                          : "Internal: I2C bus busy",
    TER_Status_AggregateError                   : "Aggregate error"
}





TER_Notifier_Cleared                    = 0x00000000
TER_Notifier_SledHeaterFaultShort       = 0x00000001
TER_Notifier_SledHeaterFaultOpen        = 0x00000002
TER_Notifier_BlowerFault                = 0x00000004
TER_Notifier_SlotCircuitOverTemp        = 0x00000008
TER_Notifier_DriveRemoved               = 0x00000010
TER_Notifier_3_3OverCurrent             = 0x00000020
TER_Notifier_DriveOverCurrent           = 0x00000040
TER_Notifier_SlotCircuitFault           = 0x00000100
TER_Notifier_LatchedSledOverTemp        = 0x00000400
TER_Notifier_LatchedSledUnderTemp       = 0x00000800
TER_Notifier_SledOverTemp               = 0x00001000
TER_Notifier_SledTemperatureFault       = 0x00002000
TER_Notifier_SledDiodeFault             = 0x00010000
TER_Notifier_TempEnvelopeFault          = 0x01000000
TER_Notifier_TempRampNotCompleted       = 0x02000000

DCT_WaitToStart             = 2
DCT_LogOnlyRunning          = 150
DCT_TempTarget              = 300
DCT_TempControlEnOn         = 301
DCT_PowerOn                 = 302
DCT_SerialEnable            = 322
DCT_WaitForDutHeader        = 303
DCT_ProcessTestHeaders      = 304
DCT_StopTest                = 305
DCT_Failure                 = 306
DCT_TempControlEnOff        = 307
DCT_WaitForDutToFinish      = 308
DCT_DutPowerOff             = 309
DCT_WaitForSafeTemperature  = 380
DCT_AnnounceTaskEnded       = 390
DCT_WaitForRemoveDut        = 407
DCT_Unknown                 = 99

DCT_CR_None                    = 0    # Reset state
DCT_CR_Completed_Normally      = 1    # Success.  Exit Code is valid
DCT_CR_Timeout                 = 2    # The test failed to finish in expected time.
DCT_CR_Canceled                = 3    # The Test was stopped with TER_StopTest()
DCT_CR_DutFault                = 4    # The DUT failed in a way the prevented the test to complete
DCT_CR_CancelledBySio          = 11   # The SIO canceled the test, e.g., to upgrade the pack.'
DCT_CR_SlotVanished            = 12
DCT_CR_DutVanished             = 13
DCT_CR_DutPowerSupplyFault     = 14
DCT_CR_TemperatureControlFault = 15
DCT_CR_IllegalTestType         = 16
DCT_CR_ProcessStartFailed      = 17
DCT_CR_CanceledByReset         = 18   # TER_Reset(4) canceled this test.
DCT_CR_UnexpectedSlotStatus    = 19
DCT_CR_SlotReportedErrors      = 20




ALL_ON = -1     # 32 bits of 1  TODO: This is dicey as python freely changes type sizes
ALL_OFF = 0
SELECT_DUT = 0  # For TER_SetSerialSelect
SELECT_FID = 1  # For TER_SetSerialSelect
DUT_POWER_BITS = 0x4   #TODO: Derive from MRPC, but really part of DUT?  Enterprise s/b 6!
POWER_BITS_FID = 0x01
POWER_BITS_12V = 0x02
POWER_BITS_5V = 0x04
POWER_BITS_3V = 0x08
POWER_BITS_VBAT = 0x08      # SLT, this is 3.7 volts or so
POWER_BITS_VBULK = 0x02     # SLT, this is typically 24V

#TER_SetSignal() / TER_PulseSignal() parameters
SIGNAL_NONE             = 0
SIGNAL_FID_RESET        = 0x01
SIGNAL_BOOT_EN          = 0x02
SIGNAL_PM2              = 0x04
SIGNAL_PSV              = 0x08  # // PSV line - Sidecar pin 4
SIGNAL_DEV_SLEEP        = 0x10
SIGNAL_SR_EN            = 0x20
SIGNAL_POWER_EN         = 0x40
SIGNAL_POWER_BUTTON     = 0x80

SIGNAL_VUBS_EN          = 0x100,
SIGNAL_SS_EN            = 0x200,
SIGNAL_SBUSB_MUXSEL     = 0x400,   #'H' to switch to "DUT-Appliance", 'L' to switch to "DUT-FP"

# TER_Reset() parameters
RESET_NONE = 0
RESET_SEND_BUFFER = 1
RESET_RECEIVE_BUFFER = 2
RESET_SLOT = 4
RESET_AUTOMATION_SAFE = 0x1001

# TER_Debug() parameters
TER_DEBUG_LOOPBACKOFF = 0x102
TER_DEBUG_LOOPBACKON = 0x103
# TER_Measure() parameters
MEASURE_TYPE_HEATER = 1
MEASURE_TYPE_FPGA_TEMP = 2

FPGA_BASE = -805306368    # The binary representation of this is 0xd0000000


USER_STRING_SIZE = 156

SlotStatusBits_IsSlotPresent = 0x00000001 # True = present, False = missing
SlotStatusBits_IsSledPresent = 0x00000002 # True = present, False = missing
SlotStatusBits_IsDrivePresent = 0x00000004 # True = present, False = missing
SlotStatusBits_IsDutPresent = 0x00000008   # True = present, False = missing



#enum TER_PropertyType = {\
TER_PropertyType_None               = 0  # Take no action
TER_PropertyType_TxEnableDelay      = 1  # Set the delay until Transmit is enabled
TER_PropertyType_SpewAckCharacter   = 2  # Set the Spew acknowledgment character
TER_PropertyType_SpewCharacter      = 3  # Set the Spew Character
TER_PropertyType_BurstSpewMode      = 4  # Set Burst Spew Mode
TER_PropertyType_BurstSpewDelay     = 5  # Set Burst Spew Delay
TER_PropertyType_BurstSpewLength    = 6  # Set Burst Spew Length
TER_PropertyType_UartTxMode         = 7  # Set the Uart Transmit Mode
TER_PropertyType_DutTemperature     = 8  # Get only the DUT's temperature if available
TER_PropertyType_ITempCorrectionEn  = 9  # Enable internal temperature correction
TER_PropertyType_DctMaxTemperature  = 10 # Maximum DUT temperature before throwing and error
TER_PropertyType_DctBaudRate        = 11 # Baud rate used by DCT
TER_PropertyType_DctSlotStatusBitMask  = 12 # What slot status bits should we check for?
TER_PropertyType_DctSlotErrorMask   = 13 # What slot error bits should we check for?
TER_PropertyType_MaxNumberPreTests  = 14 # How many pre-tests can we run locally
TER_PropertyType_MaxNumberPostTests = 15 # How many post-tests can we run locally
TER_PropertyType_ITempSensorSelect  = 16 # Which of the customer sensors is used for i-temp.  0-based.
TER_PropertyType_SerialReaderSelect = 17 # Who is reading the serial port?
TER_PropertyType_LogEnableMask      = 18 # Who is writing to the log file
TER_PropertyType_InterCharacterDelay        = 20  # Set/Get the delay between characters
TER_PropertyType_InterPacketDelay           = 21  # Set/Get the delay between packets
TER_PropertyType_AckTimeout                 = 22  # Set/Get the HDD Acknowledgment timeout
TER_PropertyType_TwoByteOneByteMode         = 23  # Enable/Disable 2Byte-1Byte Protocol
TER_PropertyType_PowerOnDelayMfgMode        = 24  # Set/Get MFG Mode Initial Delay
TER_PropertyType_InterCharacterDelayMfgMode = 25  # Set/Get MFG Mode Inter-character Gap
TER_PropertyType_ImplulseCodeMfgMode        = 26  # Set/Get hex character to send in MFG Mode
TER_PropertyType_ImplulseCountMfgMode       = 27  # Set/Get the number of bytes to send in MFG Mode
TER_PropertyType_PowerOnEnableMfgMode       = 28  # Enable/Disable MFG Mode
TER_PropertyType_LedEnableMask              = 29  # Enable/Disable Led, Bit 1 is Yellow
TER_PropertyType_JtagEnable                 = 30  # Enable/Disable JTAG
TER_PropertyType_SpiConfiguration           = 31  # Set/Get SPI configuration
TER_PropertyType_JtagDebugSelect            = 32  # Enable/Disable JTAG Debug Port to Specific Site
TER_PropertyType_FpBootMode                 = 33  # Set/Get FP to boot from PXe or SSD
TER_PropertyType_FpBootFlash                = 34  #Set/Get FP to boot from Internal Flash or Carrier Flash
TER_PropertyType_JtagReset                  = 35  #System Rest, Trst, or TMS Reset
TER_PropertyType_MaxFPGA                    = 1000# Max FPGA Properties type

# DIO Operations (must wait)
TER_PropertyType_RackDoor           = 1001  # Set rack door state in slot
TER_PropertyType_SafeHandling       = 1002  # Set safe handling
TER_PropertyType_TargetPort         = 1003  # Set SAS port
TER_PropertyType_AdjustTargetTemp   = 1004  # Adjust target temp w/o resetting PID loop
TER_PropertyType_5VRiseFallTimes            = 1005  # Set/Get 5V Rise Fall Times
TER_PropertyType_12VRiseFallTimes           = 1006  # Set/Get 12V Rise Fall Times
TER_PropertyType_5V12VSeqTime               = 1007  # Set/Get 5V and 12V Sequence Time
TER_PropertyType_FanDutyCycle               = 1008  # Set/Get Fan Duty CCycle
TER_PropertyType_EnableSafeHandling         = 1009  # Enable/Disable safe handling
TER_PropertyType_FanRpm                     = 1010  # Slot fan speed control

#Switch board operation
TER_PropertyType_SB_MuxEn       = 1100,       #enable mux by site, 1 enable, 0 disable
TER_PropertyType_SB_MuxSel      = 1101,       #select Mux channel, '0' switch to AP, '1' switch to FP
TER_PropertyType_SB_VbusEn      = 1102,       #enable vbus by site, 1 enable, 0 disable
TER_PropertyType_SB_PCIeReset   = 1103,       #reset PCIe of ASM3142, '0' to reset
TER_PropertyType_SB_FireFlySel  = 1104,       #select fire fly module, '0' to ff0, '1' to ff1
TER_PropertyType_SB_PexReset    = 1105,       #reset the PEX, 1 reset.

TER_PropertyType_Max                        = 2000    # Max DIO TER_Property Type
#}


# enum TER_UartSelection = {
SelectDutUart = 0
SelectFpUart = 1
#}

#enum TER_SerialReaders {
SerialReaderSio = 0        # The SIO Application reads the serial port.
SerialReaderApi = 1        # An external client reads the serial port.
SerialReaderUnknown = 9999
#};


#enum TER_DutUsbChannelMuxSel, used to operate the MUX on switch board of scan slot
TER_DutUsbChannelFp = 0x0       #FP to dut
TER_DutUsbChannelAp = 0x1       #appliance to dut

#enum TER_JtagType {
JtagType_None = 0   #Take no action
JtagType_Instruction = 1    #Instruction
JtagType_Data = 2   #Data
#};
#enum TER_JtagResetType{
TER_JtagResetType_Tms = 0
TER_JtagResetType_Trst=1
TER_JtagResetType_System = 2
#};

TER_PowerMeasurement_Volts = 1
TER_PowerMeasurement_Amps = 2
TER_PowerMeasurement_Watts = 3


TER_StorageMode_Wrap = 1
TER_StorageMode_Stop = 2


_TER_SlotStatusBits = {

    # TER_SlotStatusBits:
    #   These bits provide an indication of whether the
    #   slot, sled and drive are present
    'IsSlotPresent' : 0x00000001,  # True = present, False = missing
    'IsSledPresent' : 0x00000002,  # True = present, False = missing
    'IsDrivePresent' : 0x00000004, # True = present, False = missing
    'IsSsdPresent'   : 0x00000008, # true if SSD component is present


    #  These bits indicate the status of temperature controls.
    #  Only the following states are legitimate:
    #    Temperature control off          : 0x07
    #    Temperature is Ramping Up        : 0x57
    #    Temperature is Ramping Down      : 0x97
    #    Temperature is holding at target : 0x37

    'IsTempCtrlEn' : 0x00000010,   # True = Temperature Control is on
                                 # False = Temperature Control is off
    'IsAtTempTarget' : 0x00000020, # True = target temperature is reached
                                 # False = ramping or temp control is off
    'IsRampUp' : 0x00000040,       # True if ramping up
    'IsRampDown' : 0x00000080,     # True if ramping down
    'IsHeaterEnabled'         : 0x00000100, # true if heater enabled
    'IsCoolerEnabled'         : 0x00000200, # true if cooler enabled
    'IsFIDReset'                  : 0x00001000, # true if FIDReset
    'IsFIDBootStrap'              : 0x00002000, # true if FIDBootStrap
    'IsPM2'                       : 0x00004000, # true if PM2
    'IsPSV'                       : 0x00008000, # true if PSV
    'IsPowerEn'                   : 0x00001000, # true if Signal PowerEn
    'IsBootEn'                    : 0x00002000, # true if Signal BootEn
    'IsSrEn'                      : 0x00004000, # true if SR En
    'IsDevSleep'                  : 0x00008000, # true if Dev Sleep
    'TER_StatusBits_LedState0'    : 0x00010000, # individual bit of led state
    'TER_StatusBits_LedState1'    : 0x00020000, # individual bit of led state
    'TER_StatusBits_LedState2'    : 0x00040000, # individual bit of led state
    'TER_StatusBits_LedState'     : 0x00070000, # led state
    'IsFullSpeedLinkLed'          : 0x00080000, # X261 Ether Link Speed
    'IsDrivePowerOn'              : 0x00100000, # Is the drive power on
    'IsDriveTxHigh'               : 0x00200000, # Is the TX Bit high


}

statusIdxs = {
              'SlotErrors'               : 0,
              'StatusBits'               : 1,
              'TempDrive_x10'            : 2,
              'TempSlot_x10'             : 3,
              'CoolDemandPercent'        : 4,
              'HeatDemandPercent'        : 5,
              'BlowerRPM'                : 6,
              'VoltageActual_3V_mV'      : 7,
              'VoltageActual_5V_mV'      : 8,
              'VoltageActual_12V_mV'     : 9,
              'VoltageActual_18V_mV'     : 10,
              'VoltageActual_Heat_mV'    : 11,
              'CurrentActual_3V_mA'      : 12,
              'CurrentActual_5V_mA'      : 13,
              'CurrentActual_12V_mA'     : 14,
              'CurrentActual_Heat_mA'    : 15,
              'PresentTempTarget'        : 16
              }

settingsIdxs = {
                'PowerSupplyOnOff'       : 0,
                'BaudRate'               : 1,
                'SerialLogicLevels_mV'   : 2,
                'TempTarget_x10'         : 3,
                'TempRampRateCool_x10'   : 4,
                'TempRampRateHeat_x10'   : 5,
                'StatusBits'             : 6,
                'VoltageSetting_3V_mV'   : 7,
                'VoltageSetting_5V_mV'   : 8,
                'VoltageSetting_12V_mV'  : 9
                }

infoIdxs = {
            'SioPcbSerialNum'   : 0,
            'SioAppVer'         : 1,
            'SioFpgVer'         : 2,
            'SlotPcbSerialNum'  : 3,
            'SlotAppVer'        : 4,
            'SioPcbPartNum'     : 5,
            'SlotPcbPartNum'     : 6
            }

def getInfoNames():
    return infoIdxs.keys()

def getStatusNames():
    return statusIdxs.keys()

def getSettingsNames():
    return settingsIdxs.keys()

def getFieldLocation(field):
    # Do status first because A: it is the biggest
    #  and B: I want the SlotStatusBits from here rather than settings.
    if statusIdxs.has_key(field):
        return ("TER_GetSlotStatus", statusIdxs[field])
    elif _TER_SlotStatusBits.has_key(field):
        bit = _TER_SlotStatusBits[field]
        return("StatusBits", bit)
    #TODO: Add notifiers.
    elif settingsIdxs.has_key(field):
        return ("TER_GetSlotSettings", settingsIdxs[field])
    elif infoIdxs.has_key(field):
        return ("TER_GetSlotInfo", infoIdxs[field])
    else:
        return ("Unknown", -1)


def parse(tupleIn, field):
    if statusIdxs.has_key(field):
        return tupleIn[statusIdxs[field]]
    elif settingsIdxs.has_key(field):
        return tupleIn[settingsIdxs[field]]
    elif infoIdxs.has_key(field):
        return tupleIn[infoIdxs[field]]
    else:
        return -1



class SioApi(object):

    def __init__(self, sioProtocol, slotIdx):
        self.sio = sioProtocol
        self.slotIdx = slotIdx
        self._lastRecv = "(nothing yet)"
        self._lastStatus = TER_Status_none

    def setSlotIdx(self, slotIdx):
        self.slotIdx = slotIdx

    def getLastStatus(self):
        return self._lastStatus

    def getLastRecv(self):
        return self._lastRecv

    def doCmd(self, cmdIdx, params):
        try:
            result = self.sio.sendReceiveMessage(cmdIdx, self.slotIdx, params)
        except:
            raise
        self._lastStatus = result[0]
        self._lastRecv = result[1:]
        if result[0] != TER_Status_none:
            raise Exception ("%s %s\n\treturned %s" % ( cmdIdxToName(cmdIdx), repr(params), repr(result[0])))
            #raise Exception, "%s %s\n\treturned %s" % ( cmdIdxToName(cmdIdx), repr(params), repr(result[0]))
        return result[1:]

    def TER_Reset(self, resetType):
        return self.doCmd(_cmdNameToIdxDict['TER_Reset'], (resetType,))

    def TER_SetPowerEnable(self, msk, onOff):
        return self.doCmd(_cmdNameToIdxDict['TER_SetPowerEnable'], (msk, onOff,))

    def TER_SetSerialParameters(self, baudRate, stopBits):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSerialParameters'], (baudRate, stopBits,))

    def TER_SetSerialEnable(self, enable):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSerialEnable'], (enable,))

    def TER_SioSendBuffer(self, sendData):
        return self.doCmd(_cmdNameToIdxDict['TER_SioSendBuffer'], (sendData,))

    def TER_SioReceiveBuffer(self, timeoutMilliseconds, numBytes):
        return self.doCmd(_cmdNameToIdxDict['TER_SioReceiveBuffer'], (timeoutMilliseconds, numBytes,))

    def TER_UartSendBuffer(self, uartSelect, sendData):
        return self.doCmd(_cmdNameToIdxDict['TER_UartSendBuffer'], (uartSelect, sendData,))

    def TER_UartReceiveBuffer(self, uartSelect, timeoutMilliseconds, numBytes):
        return self.doCmd(_cmdNameToIdxDict['TER_UartReceiveBuffer'], (uartSelect, timeoutMilliseconds, numBytes,))

    def TER_SpiSendReceive(self, spiPortSelect, numReadBytes, sendData):
        return self.doCmd(_cmdNameToIdxDict['TER_SpiSendReceive'], (spiPortSelect, numReadBytes, sendData,))


    def TER_JtagSendReceive(self, registerType, bitCount, sendData):
        return self.doCmd(_cmdNameToIdxDict['TER_JtagSendReceive'], (registerType, bitCount, sendData,))

    def TER_SioSendReceiveBuffer(self, sendData, timeoutMilliseconds, numBytes):
        return self.doCmd(_cmdNameToIdxDict['TER_SioReceiveBuffer'], (sendData, timeoutMilliseconds, numBytes,))

    def TER_IsSlotThere(self):
        return self.doCmd(_cmdNameToIdxDict['TER_IsSlotThere'], ())

    def TER_GetSlotSettings(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSlotSettings'], ())

    def TER_GetSlotStatus(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSlotStatus'], ())

    def TER_GetUserString(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetUserString'], ())

    def TER_SetUserString(self, userString):
        return self.doCmd(_cmdNameToIdxDict['TER_SetUserString'], (userString,))

    def TER_SetTempControlEnable(self, enable):
        return self.doCmd(_cmdNameToIdxDict['TER_SetTempControlEnable'], (enable,))

    def TER_SetTargetTemperature(self, targetTemp, coolRate, heatRate, coolEn, heatEn):
        return self.doCmd(_cmdNameToIdxDict['TER_SetTargetTemperature'], (targetTemp, coolRate, heatRate, coolEn, heatEn,))

    def TER_SetPowerVoltage(self, msk, voltageMillivolts):
        return self.doCmd(_cmdNameToIdxDict['TER_SetPowerVoltage'], (msk, voltageMillivolts,))

    def TER_SetSerialLevels(self, levelInMillivolts):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSerialLevels'], (levelInMillivolts,))

    def TER_SetSerialSelect(self, select ):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSerialSelect'], (select,))

    def TER_GetSerialSelect(self ):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSerialSelect'], ())

    def TER_SetSignal(self, msk, value):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSignal'], (msk, value,))

    def TER_PulseSignal(self, msk, value, pulseWidth):
        return self.doCmd(_cmdNameToIdxDict['TER_PulseSignal'], (msk, value, pulseWidth))

    def TER_DioCmd(self, cmdStr ):
        return self.doCmd(_cmdNameToIdxDict['TER_DioCmd'], (cmdStr,))

    def TER_Debug(self, cmdStr ):
        return self.doCmd(_cmdNameToIdxDict['TER_Debug'], (cmdStr,))

    def TER_Measure(self, cmdStr ):
        return self.doCmd(_cmdNameToIdxDict['TER_Measure'], (cmdStr,))

    def TER_WriteFpgaRegisters(self, argumentTuple):    # argument tuple:  (count, addr, data, <additional addr, data pairs)
        return self.doCmd(_cmdNameToIdxDict['TER_WriteFpgaRegisters'], (argumentTuple)) #

    def TER_ReadFpgaRegisters(self, argumentTuple):             # argument tuple:  (count, addr, <additional addresses>)
        return self.doCmd(_cmdNameToIdxDict['TER_ReadFpgaRegisters'], (argumentTuple))

    def TER_GetSlotInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSlotInfo'], ())

    def TER_SioPing(self):
        return self.doCmd(_cmdNameToIdxDict['TER_SioPing'], ())

    def TER_DioMultiCmd(self, cmdStr, slotMsk):
        return self.doCmd(_cmdNameToIdxDict['TER_DioMultiCmd'], (cmdStr, slotMsk))

    def TER_SioReboot(self, fpIndex= None):
        return self.doCmd(_cmdNameToIdxDict['TER_SioReboot'], (fpIndex))

    def TER_StartSlotPoll(self):
        return self.doCmd(_cmdNameToIdxDict['TER_StartSlotPoll'], ())

    def TER_GetSlotPoll(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSlotPoll'], ())

    def TER_StartTest(self, tempTarget, rampRate, timeout, isRestart, testType=2, serialNumber=''):
        return self.doCmd(_cmdNameToIdxDict['TER_StartTest'], (tempTarget, rampRate, timeout, isRestart, testType, serialNumber))

    def TER_StopTest(self):
        return self.doCmd(_cmdNameToIdxDict['TER_StopTest'], ())

    def TER_GetTestStatus(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetTestStatus'], ())

    def TER_GetSioInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSioInfo'], ())

    def TER_GetFpInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetFpInfo'], ())

    def TER_SetFpInfo(self, serialNumber, fpAppVer, fwVer, partNumber, tftpVersion, imageVersion, osType):
        return self.doCmd(_cmdNameToIdxDict['TER_SetFpInfo'], (serialNumber, fpAppVer, fwVer, partNumber, tftpVersion, imageVersion, osType,))

    def TER_GetCachedSlotInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetCachedSlotInfo'], ())

    def TER_SetSerialPinout(self, pinoutIdx):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSerialPinout'], (pinoutIdx,))

    def TER_SetThermalType(self, typeName):
        return self.doCmd(_cmdNameToIdxDict['TER_SetThermalType'], (typeName,))

    def TER_WriteFpgaField(self, address, mask, data):
        return self.doCmd(_cmdNameToIdxDict['TER_WriteFpgaField'], (address, mask, data,))

    def TER_GetSlotUpgradeStatus(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSlotUpgradeStatus'], ())

    def TER_UpgradeSlot(self):
        return self.doCmd(_cmdNameToIdxDict['TER_UpgradeSlot'], ())

    def TER_SliceCmd(self, command, messageBody):
        return self.doCmd(_cmdNameToIdxDict['TER_SliceCmd'], (command, messageBody))

    def TER_SetSafeHandlingEnable(self, selection):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSafeHandlingEnable'], (selection,))

    def TER_SetTargetPort(self, port):
        return self.doCmd(_cmdNameToIdxDict['TER_SetTargetPort'], (port,))

    def TER_AdjustTargetTemperature(self, tempTarget):
        return self.doCmd(_cmdNameToIdxDict['TER_AdjustTargetTemperature'], (tempTarget,))

    def TER_SetProperty(self, property, valueCount, values):
        if type( values )  == tuple :
            params = (property, valueCount) + values
            return self.doCmd(_cmdNameToIdxDict['TER_SetProperty'], params)
        else:
            return self.doCmd(_cmdNameToIdxDict['TER_SetProperty'], (property, valueCount, values,))


    def TER_GetRawSio4Info(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetRawSio4Info'], ())

    def TER_UserDiag(self):
        return self.doCmd(_cmdNameToIdxDict['TER_UserDiag'], ())

    def TER_GetCachedPackInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetCachedPackInfo'], ())

    def TER_GetProperty(self, propertyName):
        return self.doCmd(_cmdNameToIdxDict['TER_GetProperty'], (propertyName,))

    def TER_Do(self, params):
        return self.doCmd(_cmdNameToIdxDict['TER_Do'], (params))

    def TER_InitializeCarrier(self ):
        return self.doCmd(_cmdNameToIdxDict['TER_InitializeCarrier'], ())

    def TER_GetCarrierInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetCarrierInfo'], ())

    def TER_GetDutInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetDutInfo'], ())

    def TER_Sync(self):
        return self.doCmd(_cmdNameToIdxDict['TER_Sync'], ())

    def TER_WriteFpga(self, address, data):    # argument tuple:  (count, addr, data, <additional addr, data pairs)
        return self.doCmd(_cmdNameToIdxDict['TER_WriteFpga'], (address, data)) #

    def TER_ReadFpgas(self, address):             # argument tuple:  (count, addr, <additional addresses>)
        return self.doCmd(_cmdNameToIdxDict['TER_ReadFpga'], (address,))

    def TER_CarrierInit(self):
        return self.doCmd(_cmdNameToIdxDict['TER_InitializeCarrier'], ())

    def TER_UartReceiveLn(self, uart, timeoutMilliseconds, numLines):
        return self.doCmd(_cmdNameToIdxDict['TER_UartReceiveLn'], (uart, timeoutMilliseconds, numLines,))

    def TER_UartGetStatus(self, uart):
        return self.doCmd(_cmdNameToIdxDict['TER_UartGetStatus'], (uart,))

    def TER_UartSetPosition(self, uart, position):
        return self.doCmd(_cmdNameToIdxDict['TER_UartSetPosition'], (uart, position))

    def TER_UartReceive(self, uartSelect, timeoutMilliseconds, numBytes):
        return self.doCmd(_cmdNameToIdxDict['TER_UartReceive'], (uartSelect, timeoutMilliseconds, numBytes,))

    def TER_SetPowerBounds(self,supplyMask,  lowerLimit, upperLimit):
        return self.doCmd(_cmdNameToIdxDict['TER_SetPowerBounds'], (supplyMask, lowerLimit, upperLimit))

    def TER_SetPowerTripPoint(self, supplyMask, measurementType, limit, numSamples):
        return self.doCmd(_cmdNameToIdxDict['TER_SetPowerTripPoint'], (supplyMask, measurementType, limit, numSamples,))

    def TER_ResetAveraging(self):
        return self.doCmd(_cmdNameToIdxDict['TER_ResetAveraging'], ())

    def TER_GetAveragingInfo(self, supplyMask):
        return self.doCmd(_cmdNameToIdxDict['TER_GetAveragingInfo'], (supplyMask,))

    def TER_GetAveragingData(self, supplyMask, measurementType, offset, numSamples):
        return self.doCmd(_cmdNameToIdxDict['TER_GetAveragingData'], (supplyMask, measurementType, offset, numSamples,))

    def TER_SetStorageMode(self, mode):
        return self.doCmd(_cmdNameToIdxDict['TER_SetStorageMode'], (mode,))

    def TER_SetSampleRate(self, supplyMask, rate):
        return self.doCmd(_cmdNameToIdxDict['TER_SetSampleRate'], (supplyMask, rate,))

    def TER_GetSbInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSbInfo'], ())

    def TER_GetSbStatus(self, siteIdx):
        return self.doCmd(_cmdNameToIdxDict['TER_GetSbStatus'], (siteIdx))

    def TER_ApplianceReset(self, applianceResetType):
        return self.doCmd(_cmdNameToIdxDict['TER_ApplianceReset'], (applianceResetType,))

    def TER_GetApplBiosInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplBiosInfo'], ())

    def TER_GetApplOsInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplOsInfo'], ())

    def TER_GetApplHwInfo(self):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplHwInfo'], ())

    def TER_GetApplNvmeDriveInfo(self, nvmeDriveId):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplNvmeDriveInfo'], (nvmeDriveId,))

    def TER_GetApplNvmeDriveStatus(self, nvmeDriveId):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplNvmeDriveStatus'], (nvmeDriveId,))

    def TER_GetApplSwitchBoardStatus(self, switchBoardId):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplSwitchBoardStatus'], (switchBoardId,))

    def TER_GetApplUsbStatus(self, siteId):
        return self.doCmd(_cmdNameToIdxDict['TER_GetApplUsbStatus'], (siteId))
