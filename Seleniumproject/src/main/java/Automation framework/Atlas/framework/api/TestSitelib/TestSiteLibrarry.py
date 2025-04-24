from enum import Enum
from enum import IntEnum, IntFlag

class PropertyType(IntEnum):
    TER_PropertyType_None = 0
    TER_PropertyType_SpiConfiguration = 2
    TER_PropertyType_PropertyDvTest = 3
    TER_PropertyType_FpgaRegLoopback = 4
    TER_PropertyType_MemoryErase = 5
    TER_PropertyType_StartBusTest = 6
    TER_PropertyType_GetBusTestStatus = 7
    TER_PropertyType_ThermalInterfaceEnable = 8
    TER_PropertyType_TcbMessagingEnable = 9
    TER_PropertyType_LedHeartbeat = 10
    TER_PropertyType_UartConfiguration = 11
    TER_PropertyType_PowerStatusSelect = 12
    TER_PropertyType_FanRPM = 14
    TER_PropertyType_JtagLoopback = 15
    TER_PropertyType_FpBootMode = 33
    TER_PropertyType_FpBootFlash = 34
    TER_PropertyType_FpFlashMuxSel = 36
    TER_PropertyType_FpxPowerEn = 37
    TER_PropertyType_FpPowerBtn = 39
    TER_PropertyType_FpRstBtn = 40
    TER_PropertyType_PollStatusInterval = 41
    TER_PropertyType_FanDutyCycle = 42
    TER_PropertyType_FanTachometer = 43
    TER_PropertyType_LedState = 44
    TER_PropertyType_RTCurvePoint = 45
    TER_PropertyType_TcbSiteParameters = 46
    TER_PropertyType_PcieLtssmHistory = 47
    TER_PropertyType_AltVoltageCurrent = 48
    TER_PropertyType_MrpcKeepalive = 49
    TER_PropertyType_PcieDisableRetimer = 50
    TER_PropertyType_PcieDisableRetimerI2c = 51
    TER_PropertyType_TestType = 52
    TER_PropertyType_SbBootStatus = 1199
    TER_PropertyType_SB_MuxEn = 1200
    TER_PropertyType_SB_MuxSel = 1201
    TER_PropertyType_SB_VbusEn = 1202
    TER_PropertyType_SB_PCIeReset = 1203
    TER_PropertyType_SB_FireFlySel = 1204
    TER_PropertyType_SB_PexReset = 1205
    TER_PropertyType_SB_PexReg = 1206
    TER_PropertyType_PipelineDebugBits = 2002


class TER_Status(IntEnum):
    Success = 0
    slotid_error = 3
    Error_Argument_Invalid = 5
    I2cError = 10
    ArgumentCountError = 19
    rpc_fail = 22
    NotImplemented = 24
    Invalid_Response = 58
    ThermalTypeError = 59
    I2cBusy = 71
    MemoryAllocError = 72
    SpiTransactionError = 81
    HW_Timeout_Error = 82
    Error_TCP_Connection = 83
    MRPC_Error = 84
    Error_Communications_Fault = 85
    SiteNotActive = 86
    TcbParameterInvalid = 87
    TcbCommandError = 88
    TcbMessagingSequenceError = 89
    TcbMessagingError = 90
    ImageUpdateFault = 91
    TcbFpgaStatus = 92
    LidNotClosedError = 93
    PowerEnabledError = 94
    SltbRailInvalid = 95
    PowerFault = 96
    LvdsError = 97
    NotInitialized = 98
    Invalid_Baud_Rate = 99
    Invalid_Stop_Bits = 100
    Timeout = 101
    AggregateError = 102
    CarrierNotPresent = 103
    CarrierInfoNotAvailable = 104
    Buffer_Overflow = 105
    JtagGeneralFailure = 106
    RFSplitterError = 108
    PowerSetupIncomplete = 109
    Faulted = 110
    NoData = 111
    UartBusy = 112
    InternalError = 113
    InitializationError = 114
    LoggingAlreadyStarted = 115
    LoggingAlreadyStopped = 116
    FileOperationError = 117
    EepromDataFormatError = 118
    UsbVbusOverCurrentFault = 119
    UartError = 120
    DutIO_InternalFault = 121
    SltbNotPresent = 122
    InvalidHardware = 123
    FileSystemMountError = 124
    EepromWriteError = 125
    I2C_Poller_NotReady = 126
    Fan_Fault = 127
    FanSpinUpFault = 128
    FanStallFault = 129
    FanDriveFail = 130
    FanControllerWatchDogExpired = 140
    BaseBoardPowerFault = 141
    PowerBoardPowerFault = 142
    PowerBoardOutputFault = 143
    IonizerPowerFault = 144
    IonizerAlarm = 145
    LedPowerFault = 146
    SafetyCircuitPowerFault = 147
    PcieEnumerationFailure = 148
    LidPowerFault = 149
    TimestampInvalid = 150
    SltbPowerFault = 151
    SltbPowerDisabled = 152
    DutBufferEnabled = 153
    LidControlNotAllowed = 154
    ParameterConflict = 155
    LidLockedDuringCoolDown = 156
    ThermalFault = 157
    PcieDeviceNotFound = 158
    DmiReadError = 159
    MrpcDefinitionMismatch = 160
    JsonParseError = 161
    ImageUpdateInProgress = 162
    ChecksumFailure = 163
    ProcessNotKilled = 164
    VFPStartFailed = 165
    VFPStopFailed = 166
    VFPDeviceAttachFailed = 167
    VFPDeviceDetachFailed = 168
    VFPUndefineFailed = 169
    InterfaceBoardPowerFault = 170
    DutPowerSupplyFault = 171
    PowerBoardReboot = 172
    PowerBoardTimeout = 173
    IpmiError = 174
    DutPowerDisabled = 175
    DidNotReboot = 176
    InternalTcpConnectionError = 177
    InternalTcpCommunicationsFault = 178
    InternalMrpcError = 179
    InternalTimeout = 180
    VFPUsbControllerAbsent = 181
    VFPInitializationError = 182
    VFPNotInitialized = 183
    OutOfResources = 184
    I2cTimeout = 185
    I2cNoAck = 186
    I2cArbitrationLost = 187
    I2cAccessError = 188
    I2cCommandFailure = 189
    I2cInvalidCommand = 190
    I2cRestart = 191
    I2cUnknownError = 192
    I2cClockLow = 193
    I2cDataLow = 194
    I2cDriverError = 195
    ScanSwitchboard = 200
    ScanPipelineDevice = 201
    ScanPipelineGeneral = 202
    ScanDownloaderServiceError = 203
    ScanDeterminConfigFail = 204
    ScanCreateResMgrFail = 205
    ScanResMgrInitializeFail = 206
    ScanPipelineLibInitFail = 207
    BaseboardNotPresent = 230
    PcieCommunicationError = 231
    BaseboardConfigurationError = 232
    ApiBufferOverflow = 1000
    ApiNullPointer = 1001
    ApiNotConnected = 1002
    ApiBufferUnderflow = 1003
    ApiNotInitialized = 1004
    Warning_MinimumCode = 1005
    MaxValue = 1006

# -----------------------------
#       Site Component
# -----------------------------


class SiteComponent(Enum):
    """
    Provides unique identifiers for SiteComponent.
    """
    SiteComponentInvalid = 0
    ControllerBoard = 1
    ThermalBoard = 2
    PowerBoard = 3
    IOBoard = 4
    FunctionalProcessor = 5
    FunctionalProcessorHost = 6
    Backplane = 7
    CarrierBoard = 8
    CarrierAssembly = 9
    InstrumentAssembly = 10
    PogoInterfaceModule = 11
    ProbeBlock = 12
    HeatSink = 13
    CoolantValve = 14
    InterpreterBoard = 15
    ScanSwitchBoard = 16
    InterfaceBoard = 17
    PowerSupply = 18


class SiteComponentAttribute(Enum):
    """
    Provides version information and unique identifiers for a SiteComponent.
    Some attributes may not apply to every SiteComponent.
    """
    PartNumber = 1
    SerialNumber = 2
    Revision = 3
    RevisionDate = 4
    FpgaVersion = 5
    BootloaderVersion = 6
    ApplicationVersion = 7
    TftpVersion = 8
    OperatingSystem = 9
    ImageVersion = 10
    RuntimeVersion = 11
    Platform = 12
    MfgLotId = 13
    LidSwitchPosition = 15
    ConfigurationVersion = 16
    MacAddress = 17

# -----------------------------
#       Uart
# -----------------------------

class UartId_Internal(IntEnum):
    Uart_1_Internal = 1
    Uart_2_Internal = 2
    Fp_Uart = 1000
    UART_DUTIO_0 = 1001
    UART_DUTIO_1 = 1002
    UART_DUTIO_2 = 1003

class UartProperty(IntEnum):
    UartPropertyLoopbackMode = 1
    UartPropertyTestDataGeneratorMode = 2
    UartPropertyPollingMode = 3
    UartPropertyBaudRate = 4


class LogId_Internal(IntEnum):
    Log_Id_Invalid = 0
    UartLog_1 = 1
    UartLog_2 = 2
    PowerLog = 3
    ThermalLog = 4
    TcbDebugLog = 5
    DebugSpewLog = 6
    FpLog = 7
    FpUartLog = 8
    Log_Id_Max = 9


class UartBaudRate(IntEnum):
    UartBaudRate_115200 = 1
    UartBaudRate_921600 = 2
    UartBaudRate_1500000 = 3

class UartBaudRate(IntEnum):
    UartBaudRate_115200 = 115200
    UartBaudRate_921600 = 921600
    UartBaudRate_1500000 = 1500000

# Simulate baud rates (and provide an alias for one commonly used value)
# baud_rate_values = [115200, 921600, 1500000]
# UartBaudRate = type(
#     "UartBaudRate",
#     (),
#     {"UartBaudRate_115200": 115200, "values": baud_rate_values}
# )

maskOfUartEnableBit = 0x00000080
# Constants used in the original code
#PropertyType = MagicMock(TER_PropertyType_UartConfiguration=0)
#UartProperty = MagicMock(UartPropertyLoopbackMode=0, UartPropertyTestDataGeneratorMode=1)
#UartId_Internal = [1, 2 , 3 , 1000, 1001]  # Mocked enum values
#LogId_Internal = [0, 1 ]   # Mocked enum values
#RegisterType = MagicMock(RegTypeRowController=0, RegTypeDutIo=1)
#ResetType = MagicMock(SiteReset=0)
#TestStatus = MagicMock(Pass=0, FAIL=1)
#TesterAlarmBits = MagicMock(InternalBusFault=0)

#validUarts = [1, 2]
uartBlockTable = {0: 0x00000000, 1: 0x0000000D, 2: 0x00000003}


#UartBaudRate = [0, 1, 2]     # Mocked enum values
# For calls that need a specific UART by name
UartId = {"Uart_1": 0}

# -----------------------------
#       Tcb
# -----------------------------
class TcbUpdateStatus(IntEnum):
    NoUpdate = 0
    FpgaImageUpdateReq = 1
    FpgaImageUpdateFail = 2
    FpgaImageUpdateSuccess = 4
    AppImageUpdateReq = 16
    AppImageUpdateFail = 32
    AppImageUpdateSuccess = 64
    ImageUpdateReq = 1
    ImageUpdateFail = 2
    ImageUpdateSuccess = 4

# -----------------------------
#       Set PowerEnable
# -----------------------------
class StatusBits:
    """
    Provides test site temperature or hardware status information.
    SltbPresent can also be considered as equivalent to carrier-present.
    SltbPresent=CarrierPresent bit is always set with fpga bit CARRIER_IO__CARRIER_PRESENT set.
    irrespective of whether SLTB hardware exists inside the carrier.
    """
    TempControlEnabled = 0x1
    TempAtTarget = 0x2
    TempRampingUp = 0x4
    TempRampingDown = 0x8
    SiteEnergized = 0x10000000
    SiteReady = 0x20000000
    SltbPresent = 0x40000000
    SitePresent = 0x80000000


class RailId:
    """
    Specifies a power rail.
    """
    RailIdInvalid = 0x0
    Variable_1 = 0x2
    Fixed24V_1 = 0x4
    Fixed12V_1 = 0x8
    Fixed12V_2 = 0x10
    Variable_2 = 0x20


class PowerAlarmBits:
    """
    Specifies the currently occurring test site power faults.
    """
    NoPowerFaults = 0x0
    OverVoltageFault = 0x1
    OverCurrentFault = 0x2
    VoltageToleranceFault = 0x4
    VoltageTimeoutFault = 0x8
    ShortCircuitFault = 0x10
    CurrentImbalanceFault = 0x20

class TesterAlarmBits:
    """
    Provides the information about tester alarm bits.
    """
    NoTesterFaults = 0x0
    SiteFault = 0x1
    PeriodicFault = 0x2
    InternalPowerSupplyFault = 0x4
    InternalBusFault = 0x8
    TemperatureSensorFault = 0x10
    IonizerFault = 0x20
    ComponentRebootFault = 0x40
    ComponentTimeoutFault = 0x80
    VirtualFpFault = 0x100


class PcieStatus:
    """
    Pcie status details.
    """
    def __init__(self, Enumerated, LinkWidth, LinkSpeed, LinkErrorCorrectable, LinkErrorNonFatal, LinkErrorFatal):
        self.Enumerated = Enumerated
        self.LinkWidth = LinkWidth
        self.LinkSpeed = LinkSpeed
        self.LinkErrorCorrectable = LinkErrorCorrectable
        self.LinkErrorNonFatal = LinkErrorNonFatal
        self.LinkErrorFatal = LinkErrorFatal

class PcieLtssmStatus:
    """
    Pcie LTSSM status details.
    """
    def __init__(self, State, RecoveryCount):
        self.State = State
        self.RecoveryCount = RecoveryCount

class SessionStatus:
    """
    Session status information for a scan session.
    """
    def __init__(self, LogFolder, SessionSummaryFileName):
        self.LogFolder = LogFolder
        self.SessionSummaryFileName = SessionSummaryFileName

class SessionSetup:
    """
    Session setup parameters.
    """
    def __init__(self, SessionSummaryFormat, EndSessionIsAsync, ArchiveUniquenessPlaceholder):
        self.SessionSummaryFormat = SessionSummaryFormat
        self.EndSessionIsAsync = EndSessionIsAsync
        self.ArchiveUniquenessPlaceholder = ArchiveUniquenessPlaceholder

class RunPatternSetup:
    """
    Run pattern setup parameters.
    """
    def __init__(self, PacketType, BitWidth, StimulusPattern, ExpectedPattern, MaskPattern,
                 PacketByteCount, StopOnFail, DataOffset, DataCaptureLimit,
                 Timeout, MaskPolarity):
        self.PacketType = PacketType
        self.BitWidth = BitWidth
        self.StimulusPattern = StimulusPattern
        self.ExpectedPattern = ExpectedPattern
        self.MaskPattern = MaskPattern
        self.PacketByteCount = PacketByteCount
        self.StopOnFail = StopOnFail
        self.DataOffset = DataOffset
        self.DataCaptureLimit = DataCaptureLimit
        self.Timeout = Timeout
        self.MaskPolarity = MaskPolarity

class RunPatternLoggingSetup:
    """
    Run pattern logging setup parameters.
    """
    def __init__(self, UniquenessLogPrepend, ResultsLogPass, ResultsLogFail,
                 ResultsLogFileName, PinMapping, ResultsOutputFormat,
                 ReceivedLogDataOnlyOnFail, ReceivedLogDataFileName,
                 FfcGenerateResult):
        self.UniquenessLogPrepend = UniquenessLogPrepend
        self.ResultsLogPass = ResultsLogPass
        self.ResultsLogFail = ResultsLogFail
        self.ResultsLogFileName = ResultsLogFileName
        self.PinMapping = PinMapping
        self.ResultsOutputFormat = ResultsOutputFormat
        self.ReceivedLogDataOnlyOnFail = ReceivedLogDataOnlyOnFail
        self.ReceivedLogDataFileName = ReceivedLogDataFileName
        self.FfcGenerateResult = FfcGenerateResult


class ResetType(IntEnum):
    """
    Enum representing different reset types.
    """
    Reset_None = 0  # Not a valid reset type.
    SiteReset = 1  # Turns off a test site's VBat, VBulk, VBus, carrier power, and signals.
                   # Resets it to its lowest power state.
    SiteThermalReset = 2  # Resets all thermal control parameters and settings.
    SiteInitialization = 3  # Turns off a test site's VBat, VBulk, VBus, carrier power, and signals.
                            # Resets it to its lowest power state. Resets the fan speed to the config file default.
    AutomationSafeReset = 4  # Turns off power to a carrier and performs a SiteReset on its test sites
                             # so it can be safely removed.


class GpioId(IntEnum):
    """
    Enum representing GPIO lines in the system.
    """
    Gpio_Invalid = 0

    # GPIO lines 1 through 128
    Gpio_1 = 1
    Gpio_2 = 2
    # ... (fill in the sequence as needed for all Gpio_3 to Gpio_128)
    Gpio_3 = 3
    Gpio_4 = 4
    Gpio_5 = 5
    Gpio_6 = 6
    Gpio_7 = 7
    Gpio_8 = 8
    Gpio_9 = 9
    Gpio_10 = 10
    Gpio_11 = 11
    Gpio_12 = 12
    Gpio_13 = 13
    Gpio_14 = 14
    Gpio_15 = 15
    Gpio_16 = 16
    Gpio_17 = 17
    Gpio_18 = 18
    Gpio_19 = 19
    Gpio_20 = 20
    Gpio_21 = 21
    Gpio_22 = 22
    Gpio_23 = 23
    Gpio_24 = 24
    Gpio_25 = 25
    Gpio_26 = 26
    Gpio_27 = 27
    Gpio_28 = 28
    Gpio_29 = 29
    Gpio_30 = 30
    Gpio_31 = 31
    Gpio_32 = 32
    Gpio_33 = 33
    Gpio_34 = 34
    Gpio_35 = 35
    Gpio_36 = 36
    Gpio_37 = 37
    Gpio_38 = 38
    Gpio_39 = 39
    Gpio_40 = 40
    Gpio_41 = 41
    Gpio_42 = 42
    Gpio_43 = 43
    Gpio_44 = 44
    Gpio_45 = 45
    Gpio_46 = 46
    Gpio_47 = 47
    Gpio_48 = 48
    Gpio_49 = 49
    Gpio_50 = 50
    Gpio_51 = 51
    Gpio_52 = 52
    Gpio_53 = 53
    Gpio_54 = 54
    Gpio_55 = 55
    Gpio_56 = 56
    Gpio_57 = 57
    Gpio_58 = 58
    Gpio_59 = 59
    Gpio_60 = 60
    Gpio_61 = 61
    Gpio_62 = 62
    Gpio_63 = 63
    Gpio_64 = 64
    Gpio_65 = 65
    Gpio_66 = 66
    Gpio_67 = 67
    Gpio_68 = 68
    Gpio_69 = 69
    Gpio_70 = 70
    Gpio_71 = 71
    Gpio_72 = 72
    Gpio_73 = 73
    Gpio_74 = 74
    Gpio_75 = 75
    Gpio_76 = 76
    Gpio_77 = 77
    Gpio_78 = 78
    Gpio_79 = 79
    Gpio_80 = 80
    Gpio_81 = 81
    Gpio_82 = 82
    Gpio_83 = 83
    Gpio_84 = 84
    Gpio_85 = 85
    Gpio_86 = 86
    Gpio_87 = 87
    Gpio_88 = 88
    Gpio_89 = 89
    Gpio_90 = 90
    Gpio_91 = 91
    Gpio_92 = 92
    Gpio_93 = 93
    Gpio_94 = 94
    Gpio_95 = 95
    Gpio_96 = 96
    Gpio_97 = 97
    Gpio_98 = 98
    Gpio_99 = 99
    Gpio_100 = 100
    Gpio_101 = 101
    Gpio_102 = 102
    Gpio_103 = 103
    Gpio_104 = 104
    Gpio_105 = 105
    Gpio_106 = 106
    Gpio_107 = 107
    Gpio_108 = 108
    Gpio_109 = 109
    Gpio_110 = 110
    Gpio_111 = 111
    Gpio_112 = 112
    Gpio_113 = 113
    Gpio_114 = 114
    Gpio_115 = 115
    Gpio_116 = 116
    Gpio_117 = 117
    Gpio_118 = 118
    Gpio_119 = 119
    Gpio_120 = 120
    Gpio_121 = 121
    Gpio_122 = 122
    Gpio_123 = 123
    Gpio_124 = 124
    Gpio_125 = 125
    Gpio_126 = 126
    Gpio_127 = 127
    Gpio_128 = 128

    # PCIe-specific GPIO lines
    Gpio_Pcie1_PRSNT_L = 10000
    Gpio_Pcie1_PRSNT0_L = 10000
    Gpio_Pcie1_PRSNT1_L = 10001
    Gpio_Pcie1_PERST_L = 10002
    Gpio_Pcie1_PERST0_L = 10002
    Gpio_Pcie1_PERSTB_L = 10003
    Gpio_Pcie1_PERST1_L = 10003
    Gpio_Pcie1_CLKREQ_L = 10004
    Gpio_Pcie1_PWRDIS = 10005
    Gpio_Pcie1_DUALPORTEN_L = 10006
    Gpio_Pcie1_LED = 10007
    Gpio_Pcie1_LED_1_L = 10007
    Gpio_Pcie1_ACTIVITY_L = 10007
    Gpio_Pcie1_WAKE_L = 10008
    Gpio_Pcie1_MFG = 10009
    Gpio_Pcie1_SMRST_L = 10010
    Gpio_Pcie1_EDSFF_A42 = 10011
    Gpio_Pcie1_EDSFF_B8 = 10012



# Enum for GPIO input/output signal state
class GpioState(IntEnum):
    """
    Identifies the GPIO input/output signal state.
    """
    InvalidState = 0
    Low = 1
    High = 2


# Enum for GPIO direction
class GpioDirection(IntEnum):
    """
    Identifies the GPIO direction.
    """
    InvalidDirection = 0
    Input = 1
    Output = 2


# Enum for ionizer interface
class IonizerId(IntEnum):
    """
    Identifies an ionizer interface.
    """
    IonizerIdInvalid = 0
    Ionizer_1 = 1


# Enum for aggregation methods
class Aggregation(IntEnum):
    """
    Specifies an aggregation method for multiple values.
    """
    AggregationNone = 0  # No aggregation
    Single = 1           # Single value
    Average = 2          # Average of values
    Maximum = 3          # Maximum of values


# Enum for temperature sensor using IntFlag to allow bitwise OR
class TemperatureSensor(IntFlag):
    """
    Identifies a temperature sensor.
    Values can be bitwise ORed to select multiple sensors.
    """
    TemperatureSensorInvalid = 0x0  # Invalid sensor
    SensorNone = 0x0                # No sensor
    DutSensor_1 = 0x1               # DUT sensor #1
    DutSensor_2 = 0x2               # DUT sensor #2
    DutSensor_3 = 0x4               # DUT sensor #3
    DutSensor_4 = 0x8               # DUT sensor #4


# Enum for uptime component
class UptimeId(IntEnum):
    """
    Identifies uptime component.
    """
    SourceInvalid = 0     # Invalid value
    UptimeHost = 1        # Host uptime
    UptimeService = 2     # Service application uptime


# Enum for PCIe link width
class PcieLinkWidth(IntEnum):
    """
    Identifies PCIe link width.
    """
    PcieLinkWidthInvalid = 0
    Pcie_x1 = 1
    Pcie_x2 = 2
    Pcie_x4 = 3
    Pcie_x8 = 4
    Pcie_x16 = 5


# Enum for PCIe link speed
class PcieLinkSpeed(IntEnum):
    """
    Identifies PCIe link speed.
    """
    PcieLinkSpeedInvalid = 0
    Pcie_2_5_GT_s = 1
    Pcie_5_GT_s = 2
    Pcie_8_GT_s = 3
    Pcie_16_GT_s = 4
    Pcie_32_GT_s = 5
    Pcie_64_GT_s = 6


# Enum for power restriction for lid control
class PowerRestriction(IntEnum):
    """
    Power restriction for lid control.
    """
    PowerRestrictionInvalid = 0
    PowerRestrictionNone = 1
    PowerRestrictionPowerOff = 2
    PowerRestrictionCurrentLimit = 3


# Enum for PCIe device IDs
class PcieId(IntEnum):
    """
    PCIe device IDs.
    """
    PcieIdInvalid = 0
    Pcie_1 = 1
    Pcie_2 = 2


# Enum for format of pattern test output record
class RunPatternOutputFormat(IntEnum):
    """
    Format of pattern test output record.
    """
    PinRecordFormat = 0
    CycleRecordFormat = 1
    ErrorMapBin = 2
    ErrorMapTxt = 3
    NUM_OF_OUTPUT_FORMAT = 4


# Enum for USB speed
class UsbSpeed(IntEnum):
    """
    Represents USB speed.
    """
    UsbSpeedUnknown = 0
    UsbSpeedLow = 1
    UsbSpeedFull = 2
    UsbSpeedHigh = 3
    UsbSpeedSuper = 4
    UsbSpeedSuperPlus = 5


# Enum for USB reset type
class UsbResetType(IntEnum):
    """
    Represents the USB reset type.
    """
    UsbReset_None = 0
    UsbDriver = 1
    UsbHostController = 2
    UsbHostControllerParent = 3


# Enum for ADC sampling capture mode
class CaptureMode(IntEnum):
    """
    Capture Mode used for ADC sampling.
    """
    StopOnFull = 1
    WrapAround = 2


# Enum for ADC sampling measurement type
class MeasurementType(IntEnum):
    """
    Measurement Type used for ADC sampling.
    """
    Voltage = 1
    Current = 2
    Power = 3

# Register width
class RegisterWidth(IntEnum):
    """
    Register width used for PCIe configuration registers.
    """
    RegisterWidth8 = 8
    RegisterWidth16 = 16
    RegisterWidth32 = 32


# PCIe Equalization presets
class PcieEqPreset(IntEnum):
    """
    PCIe Equalization presets.
    """
    PcieEqPreset0 = 0
    PcieEqPreset1 = 1
    PcieEqPreset2 = 2
    PcieEqPreset3 = 3
    PcieEqPreset4 = 4
    PcieEqPreset5 = 5
    PcieEqPreset6 = 6
    PcieEqPreset7 = 7
    PcieEqPreset8 = 8
    PcieEqPreset9 = 9
    PcieEqPreset10 = 10


# PCIe Link Training Status State Machine (LTSMM) state
class PcieLtssmState(IntEnum):
    """
    PCIe Link Training Status State Machine (LTSMM) state.
    """
    LtssmStateInvalid = 0x0
    Detect = 0x100
    Detect_Quiet = 0x101
    Detect_Active = 0x102
    Polling = 0x200
    Polling_Active = 0x201
    Polling_Compliance = 0x202
    Polling_Config = 0x203
    Polling_Speed = 0x204
    Config = 0x400
    Config_Idle = 0x401
    Config_LinkWidth_Start = 0x402
    Config_LinkWidth_Accept = 0x403
    Config_LaneNum_Accept = 0x404
    Config_LaneNum_Wait = 0x405
    Config_Complete = 0x406
    Recovery = 0x800
    Recovery_RcvrLock = 0x801
    Recovery_Speed = 0x802
    Recovery_Equalization = 0x803
    Recovery_RcvrCfg = 0x804
    Recovery_Idle = 0x805
    L0 = 0x1000
    L0s = 0x2000
    L0s_Entry = 0x2001
    L0s_Idle = 0x2002
    L0s_Fts = 0x2003
    L1 = 0x4000
    L1_Entry = 0x4001
    L1_Idle = 0x4002
    L1_PM = 0x4003
    L2 = 0x80000
    L2_Idle = 0x8001
    L2_TransmitWake = 0x8002
    Disabled = 0x10000
    Loopback = 0x20000
    Loopback_Entry = 0x20001
    Loopback_Active = 0x20002
    Loopback_Exit = 0x20003
    HotReset = 0x40000
    Retimer = 0x100000
    Retimer_Admin = 0x100001

# Struct for PowerStatus
class PowerStatus:
    """
    Provides status information for a power rail.
    """
    def __init__(self, Rail, Voltage, Current, Faults):
        self.Rail = Rail  # Identifier of the power rail
        self.Voltage = Voltage  # Voltage in Volts
        self.Current = Current  # Current in Amps
        self.Faults = Faults  # Currently occurring power faults


# Struct for FanStatus
class FanStatus:
    """
    Provides test site fan information.
    """
    def __init__(self, Id, Rpm):
        self.Id = Id  # Fan identifier
        self.Rpm = Rpm  # Current RPM of this fan


# Struct for ThermalStatus
class ThermalStatus:
    """
    Provides test site thermal system status information.
    """
    def __init__(self, TargetTemp, FanStatuses, EstimatedDutTemp, EstimatedDutPower,
                 ActualDutTempCount, ActualDutTemp, Faults):
        self.TargetTemp = TargetTemp  # Temperature setpoint for the DUT
        self.FanStatuses = FanStatuses  # Status of all fans
        self.EstimatedDutTemp = EstimatedDutTemp  # Current DUT temperature
        self.EstimatedDutPower = EstimatedDutPower  # Power applied to the DUT
        self.ActualDutTempCount = ActualDutTempCount  # Count of measured temperatures
        self.ActualDutTemp = ActualDutTemp  # Measured temperatures by DUT sensors
        self.Faults = Faults  # Thermal faults


# Struct for SiteStatus
class SiteStatus:
    """
    Provides the information about the test site status and faults.
    The information updates every two seconds.
    """
    def __init__(self, alarmBits, testerAlarmBits, statusBits, powerStatus, thermalStatus, AlarmDiagCode):
        self.alarmBits = alarmBits
        self.testerAlarmBits = TesterAlarmBits
        self.statusBits = StatusBits
        self.powerStatus = powerStatus
        self.thermalStatus = thermalStatus
        self.AlarmDiagCode = AlarmDiagCode

# Struct for SiteSettings
class SiteSettings:
    """
    Provides the current thermal settings.
    """
    def __init__(self, TempTarget, TempRampRate, CoolRampRate, HeatRampRate, CoolerEnable, HeaterEnable, PowerRails, ThermalType):
        self.TempTarget = TempTarget
        self.TempRampRate = TempRampRate
        self.CoolRampRate = CoolRampRate
        self.HeatRampRate = HeatRampRate
        self.CoolerEnable = CoolerEnable
        self.HeaterEnable = HeaterEnable
        self.PowerRails = PowerRails
        self.ThermalType = ThermalType

# Struct for PcieInfo
class PcieInfo:
    """
    Provides information about PCIe.
    """
    def __init__(self, Bus, Device, Function, BusDeviceFunction, DeviceId, VendorId):
        self.Bus = Bus
        self.Device = Device
        self.Function = Function
        self.BusDeviceFunction = BusDeviceFunction
        self.DeviceId = DeviceId
        self.VendorId = VendorId
