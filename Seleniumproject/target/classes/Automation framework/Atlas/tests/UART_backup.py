import pytest
import allure
from unittest.mock import MagicMock
import time
from datetime import datetime
from tms.framework.api.TestSiteCaller.TestSiteCaller import TestSiteInternal,TestSite
from tms.framework.api.TestSiteLib.TestSiteLibrarry import (UartId_Internal,TER_Status, UartId,UartBaudRate,LogId_Internal,
                                                            SiteComponent,SiteComponentAttribute,PropertyType)
from tms.framework.api.TestSiteLib.ClientException import *
import logging
from tms.framework.api.TestSiteRunner.TestSiteRunner import TSAR

def ExpectClientEx(status, method):
    return ClientException(status, f"Expected exception for method: {method}")

@pytest.fixture(scope="class")
def tsar_instance(request):
    """Creates a single TSAR instance for all tests in the class."""
    tsar = TSAR()
    tsar.ConnectSsh()

    # Attach the TSAR instance to the test class
    request.cls.tsar_instance = tsar

    yield tsar  # Provide the instance to tests

    tsar.disconnectSsh()  # Disconnect after all tests are done

# -----------------------------
#       TestUART
# -----------------------------

@allure.feature("Test UART - TSAR SSH Commands")
@pytest.mark.usefixtures("tsar_instance")  # Apply the fixture at the class level
class Test_UART:
    def __init__(self):
        self.IOBoardPresent = True
        self.uartBlockTable = None
        self.validUarts = None
        self.validBaudRates = None
        self.logIdDict = None
        self.magnus5x = False
        self.SendByteCount = 2048
        self.TotalCount = 100
        self.ComprehensiveTests = False

        # Pytest Test Function: UartConfigureApiTest
        # -----------------------------
        self.validUarts = [
            UartId_Internal.Uart_1_Internal,
            UartId_Internal.Fp_Uart,
            UartId_Internal.UART_DUTIO_0,
            UartId_Internal.UART_DUTIO_1,
            UartId_Internal.UART_DUTIO_2,
        ]

    def SkipAllTests(self, message):
        print(message)

    def IsSubSltPlatformCayman(self):
        # Dummy implementation for example
        return True

    def base_PlatformSetupHalos(self):
        print("Base PlatformSetupHalos called")

    def base_PlatformSetupTitan(self):
        print("Base PlatformSetupTitan called")

    def compare(self, message, expected, actual):
        assert expected == actual, f"{message} - Expected: {expected}, Actual: {actual}"

    def compare_binary(self, message, expected, actual):
        assert expected == actual, f"{message} - Binary comparison failed"

    def log_step(self, message):
        print(f"Step: {message}")

    def log_result(self, status, message, *args):
        print(f"Result: {message}")

    def log_message(self, message):
        print(f"Message: {message}")

    def uart_set_loopback_mode(self, uart_id, mode):
        TestSiteInternal.SetProperty(PropertyType.TER_PropertyType_UartConfiguration,
                                     [UartProperty.UartPropertyLoopbackMode, uart_id, mode])

    def uart_set_data_generator_mode(self, uart_id, mode):
        TestSiteInternal.SetProperty(PropertyType.TER_PropertyType_UartConfiguration,
                                     [UartProperty.UartPropertyTestDataGeneratorMode, uart_id, mode])

    def uart_set_baud_rate(self, uart_id, baud_rate):
        TestSiteInternal.UartSetBaudRate(uart_id, baud_rate)

    def generate_buffer(self, byte_count):
        return bytes(range(byte_count))

    def uart_get_polling_mode(self, uart_id):
        return TestSiteInternal.GetProperty(PropertyType.TER_PropertyType_UartConfiguration, 1,
                                            [UartProperty.UartPropertyPollingMode, uart_id])[0]

    def uart_set_polling_mode(self, uart_id, mode):
        TestSiteInternal.SetProperty(PropertyType.TER_PropertyType_UartConfiguration,
                                     [UartProperty.UartPropertyPollingMode, uart_id, mode])

    def get_uart_cfg_register_value(self, uart_id):
        reg_value = 0
        reg = 0

        if uart_id in [0, 1, 2]:
            reg_addr = [self.build_address(uartBlockTable[uart_id], reg)]
            reg_data = TestSiteInternal.GetRegisters(RegisterType.RegTypeRowController, reg_addr)
            reg_value = reg_data[0]
        else:
            reg_addr = [(5 << 20) | (uartBlockTable[uart_id] << 16) | (reg << 0)]
            reg_data = TestSiteInternal.GetRegisters(RegisterType.RegTypeDutIo, reg_addr)
            reg_value = reg_data[0]

        return reg_value

    def build_address(self, block, reg):
        block_shift = 21
        site_shift = 18
        reg_shift = 12
        site = 0  # Mocked SiteIndex, assuming it is 1 for demonstration
        address = (block << block_shift) | (site << site_shift) | (reg << reg_shift)
        return address

    # -----------------------------
    #       Platform Setup
    # -----------------------------
    def PlatformSetupHalos(self):
        if not self.IOBoardPresent:
            self.SkipAllTests("DUT I/O board absent.")
            return

        if self.IsSubSltPlatformCayman():
            if self.uartBlockTable is None:
                self.uartBlockTable = {
                    UartId_Internal.Uart_1_Internal: 2,  # map to UART_DUTIO_2
                    UartId_Internal.Fp_Uart: 1,  # map to UART_DUTIO_1
                    UartId_Internal.UART_DUTIO_0: 0,
                    UartId_Internal.UART_DUTIO_1: 1,
                    UartId_Internal.UART_DUTIO_2: 2,
                }

            if self.validUarts is None or self.validBaudRates is None:
                self.logIdDict = {
                    UartId_Internal.Uart_1_Internal: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.Fp_Uart: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_0: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_1: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_2: LogId_Internal.Log_Id_Invalid,
                }

                self.validUarts = [
                    UartId_Internal.Uart_1_Internal,
                    UartId_Internal.Fp_Uart,
                    UartId_Internal.UART_DUTIO_0,
                    UartId_Internal.UART_DUTIO_1,
                    UartId_Internal.UART_DUTIO_2,
                ]

                self.validBaudRates = [
                    UartBaudRate.UartBaudRate_115200,
                ]
        else:
            if self.uartBlockTable is None:
                self.uartBlockTable = {
                    UartId_Internal.Uart_1_Internal: 1,  # map to UART_DUTIO_1
                    UartId_Internal.Uart_2_Internal: 2,  # map to UART_DUTIO_2
                    UartId_Internal.UART_DUTIO_0: 0,
                    UartId_Internal.UART_DUTIO_1: 1,
                    UartId_Internal.UART_DUTIO_2: 2,
                }

            if self.validUarts is None or self.validBaudRates is None:
                self.logIdDict = {
                    UartId_Internal.Uart_1_Internal: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.Uart_2_Internal: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_0: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_1: LogId_Internal.Log_Id_Invalid,
                    UartId_Internal.UART_DUTIO_2: LogId_Internal.Log_Id_Invalid,
                }

                self.validUarts = [
                    UartId_Internal.Uart_1_Internal,
                    UartId_Internal.Uart_2_Internal,
                    UartId_Internal.UART_DUTIO_0,
                    UartId_Internal.UART_DUTIO_1,
                    UartId_Internal.UART_DUTIO_2,
                ]

                self.validBaudRates = [
                    UartBaudRate.UartBaudRate_115200,
                ]

        self.base_PlatformSetupHalos()

    def PlatformSetupTitan(self):
        self.blockShift = 21
        self.siteShift = 18
        self.regShift = 12

        if self.uartBlockTable is None:
            self.uartBlockTable = {
                UartId_Internal.Uart_1_Internal: 0x00000000,
                UartId_Internal.Uart_2_Internal: 0x0000000D,
                UartId_Internal.Fp_Uart: 0x00000003,
            }

        if self.validUarts is None or self.validBaudRates is None:
            tpnLengthToCompare = 9

            attribute = TestSite.GetAttribute(SiteComponent.InstrumentAssembly, SiteComponentAttribute.PartNumber)

            self.logIdDict = {
                UartId_Internal.Uart_1_Internal: LogId_Internal.UartLog_1,
                UartId_Internal.Uart_2_Internal: LogId_Internal.UartLog_2,
                UartId_Internal.Fp_Uart: LogId_Internal.Log_Id_Invalid,
            }

            if attribute[:tpnLengthToCompare] == "magnusInstrumentAssemblyPartNumber5x"[:tpnLengthToCompare]:
                self.validUarts = [
                    UartId_Internal.Uart_1_Internal,
                    UartId_Internal.Uart_2_Internal,
                    UartId_Internal.Fp_Uart,
                ]

                self.validBaudRates = [
                    UartBaudRate.UartBaudRate_115200,
                    UartBaudRate.UartBaudRate_921600,
                    UartBaudRate.UartBaudRate_1500000,
                ]

                self.magnus5x = True
            else:
                self.validUarts = [
                    UartId_Internal.Uart_1_Internal,
                    UartId_Internal.Uart_2_Internal,
                    UartId_Internal.Fp_Uart,
                ]

                # logIdDict[UartId_Internal.Uart_2_Internal] = LogId_Internal.Log_Id_Invalid

                self.validBaudRates = [
                    UartBaudRate.UartBaudRate_115200,
                ]

                self.magnus5x = False

        self.base_PlatformSetupTitan()

    @pytest.mark.parametrize("uartId", list(UartId_Internal))
    @pytest.mark.parametrize("baudRate", list(UartBaudRate))
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartConfigureApiTest_valid(self, uartId, baudRate):
        if uartId in self.validUarts:
            TestSiteInternal.UartSetBaudRate(uartId, baudRate)
        else:
            exception = ExpectClientEx(TER_Status.TER_Status_NotImplemented, "UartSetBaudRate")
            TestSiteInternal.UartSetBaudRate(uartId, baudRate, exception)


    def test_UartConfigureApiTest_exceptions():
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartSetBaudRate: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage)

        min_val = min([item.value for item in UartId_Internal]) - 1
        max_val = max([item.value for item in UartId_Internal]) + 1

        TestSiteInternal.UartSetBaudRate(min_val, UartBaudRate.UartBaudRate_115200, argumentInvalidException)
        TestSiteInternal.UartSetBaudRate(max_val, UartBaudRate.UartBaudRate_115200, argumentInvalidException)

        min_val = min([item.value for item in UartBaudRate]) - 1
        max_val = max([item.value for item in UartBaudRate]) + 1

        TestSiteInternal.UartSetBaudRate(UartId_Internal.Uart_1_Internal, min_val, argumentInvalidException)
        TestSiteInternal.UartSetBaudRate(UartId_Internal.Uart_1_Internal, max_val, argumentInvalidException)

    @pytest.mark.parametrize("uartId", list(UartId_Internal))
    def test_UartConfigureApiTest(uartId):
        #LogStep(f"Testing {uartId}")
        for baudRate in UartBaudRate:
            full_cmd = f""
            result = self.tsar_instance.executeSsh_Command(api_name, full_cmd)
            assert result == 0, f"TSAR command {api_name} failed"
            test_UartConfigureApiTest_valid(uartId, baudRate)

        test_UartConfigureApiTest_exceptions()




    @allure.story("Common Get TSAR Commands")
    @pytest.mark.parametrize("api_name, full_cmd", [
        ("GetMfgInfo", "GetMfgInfo"),
        ("GetPingCmd", "GetPingCmd"),
        ("GetRebootCmd", "GetRebootCmd"),

        ("GetSiteDutIOStatus", "GetSiteDutIOStatus"),

        ("GetComponents", "GetComponents"),
        ("GetInfo", "GetInfo"),
        ("GetLidStatus", "GetLidStatus"),
        ("GetTemperature", "GetTemperature"),
    ])
    @allure.step("Executing {api_name} command")
    def test_common_get_apis(self, api_name, full_cmd):
        result = self.tsar_instance.executeSsh_Command(api_name, full_cmd)
        assert result == 0, f"TSAR command {api_name} failed"

    def test_get_site_info_api():
        #
        # This test verifies the API itself (validating parameters only).
        #
        argumentInvalidMessage = (
            "API error TER_Status_Error_Argument_Invalid when calling method UartSetBaudRate: "
            "TER_Status_Error_Argument_Invalid"
        )
        argumentInvalidException = ClientException(
            TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage
        )
        TestSiteInternal.GetSiteInfo()

    def test_uart_configure_api():
        #
        # This test verifies the API itself (validating parameters only).
        #
        argumentInvalidMessage = (
            "API error TER_Status_Error_Argument_Invalid when calling method UartSetBaudRate: "
            "TER_Status_Error_Argument_Invalid"
        )
        argumentInvalidException = ClientException(
            TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage
        )

        logging.info("*** setup_teardown - TestSiteInternal.Initialize()  ***")
        TestSiteInternal.Initialize()

        #TestSiteInternal.GetSiteInfo()


        # Loop through every UART ID defined in UartId_Internal.
        for uart_id in UartId_Internal:
            #print(f"Testing {uart_id} ")
            # For every baud rate (our simulated enum values)…
            for baud_rate in UartBaudRate.values:
                if uart_id in validUarts:
                    print(f"Testing {uart_id} {baud_rate}")
                    # For valid UARTs, the call should succeed (i.e. not raise an exception).
                    TestSiteInternal.UartSetBaudRate(uart_id, baud_rate)
                else:
                    # For other UART IDs, we expect a NotImplemented status.
                    notImplementedUartSetBaudRate = expect_client_ex(
                        TER_Status.TER_Status_NotImplemented, "UartSetBaudRate"
                    )
                    with pytest.raises(ClientException) as excinfo:
                        TestSiteInternal.UartSetBaudRate(uart_id, baud_rate, notImplementedUartSetBaudRate)
                    # The expected message for a “not implemented” error.
                    expected_msg = (
                        f"API error {TER_Status.TER_Status_NotImplemented} when calling method UartSetBaudRate: "
                        f"{TER_Status.TER_Status_NotImplemented}"
                    )
                    assert str(excinfo.value) == expected_msg

        print("LogStep: Testing exceptions")
        # Test invalid UART IDs.
        min_uart = min(UartId_Internal) - 1
        max_uart = max(UartId_Internal) + 1

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartSetBaudRate(min_uart, UartBaudRate.UartBaudRate_115200, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartSetBaudRate(max_uart, UartBaudRate.UartBaudRate_115200, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        # Test invalid baud rate values.
        min_baud = min(baud_rate_values) - 1
        max_baud = max(baud_rate_values) + 1

        with pytest.raises(ClientException) as excinfo:
            TestSite.UartSetBaudRate(UartId["Uart_1"], min_baud, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSite.UartSetBaudRate(UartId["Uart_1"], max_baud, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

    # -----------------------------
    # Test: Validate GetUartCfgRegisterValue Helper
    # -----------------------------

    def test_get_uart_cfg_register_value():
        # For uart ids 0, 1, 2 the condition is met and we expect the row controller register.
        for uart_id in [0, 1, 2]:
            reg_value = get_uart_cfg_register_value(uart_id)
            # In our simulation, GetRegisters for RegTypeRowController returns [0x80].
            assert reg_value == 0x80

        # For other uart IDs (e.g. 3) the DUTIO branch is taken.
        reg_value = get_uart_cfg_register_value(3)
        # In our simulation, GetRegisters for RegTypeDutIo returns [0].
        assert reg_value == 0

    def test_uart_set_enable_api(setup_teardown):
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartSetEnable: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage)

        for bState in [False, True]:
            for uart_id in UartId_Internal:
                setup_teardown.log_step(f"Testing {uart_id} with state {bState}")

                if uart_id in validUarts:
                    TestSiteInternal.UartSetEnable(uart_id, bState)

                    regValue = get_uart_cfg_register_value(uart_id)

                    bResult = (regValue & maskOfUartEnableBit) == maskOfUartEnableBit if bState else (regValue & maskOfUartEnableBit) == 0
                    targetState = "enabled" if bState else "disabled"
                    setup_teardown.compare(f"{uart_id} set to be {targetState}", True, bResult)
                else:
                    notImplementedFunc = ClientException(TER_Status.TER_Status_NotImplemented, "UartSetEnable")
                    with pytest.raises(ClientException) as excinfo:
                        TestSiteInternal.UartSetEnable(uart_id, bState, notImplementedFunc)
                    assert str(excinfo.value) == "NotImplemented"

            setup_teardown.log_step("Testing exceptions")

            min_value = min(UartId_Internal) - 1
            max_value = max(UartId_Internal) + 1

            with pytest.raises(ClientException) as excinfo:
                TestSiteInternal.UartSetEnable(min_value, bState, argumentInvalidException)
            assert str(excinfo.value) == argumentInvalidMessage

            with pytest.raises(ClientException) as excinfo:
                TestSiteInternal.UartSetEnable(max_value, bState, argumentInvalidException)
            assert str(excinfo.value) == argumentInvalidMessage
    # -----------------------------
    # Test: UartSendApi
    # This test verifies the API itslef.  It verifies valid as well as invalid parameters.
    # -----------------------------
    def test_uart_send_api(setup_teardown):
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartSend: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage)
        maxTxBytes = 2048
        data = bytearray([0x00])

        for uart_id in UartId_Internal:
            setup_teardown.log_step(f"Testing {uart_id}")

            data = bytearray([0x00])

            if uart_id in validUarts:
                TestSiteInternal.UartSend(uart_id, data)
            else:
                notImplementedUartSend = ClientException(TER_Status.TER_Status_NotImplemented, "UartSend")
                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.UartSend(uart_id, data, notImplementedUartSend)
                assert str(excinfo.value) == "NotImplemented"

        setup_teardown.log_step("Testing exceptions")

        min_value = min(UartId_Internal) - 1
        max_value = max(UartId_Internal) + 1

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartSend(min_value, data, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartSend(max_value, data, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        data = bytearray(maxTxBytes + 1)

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartSend(0, data, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        data = None

        with pytest.raises(ValueError):
            TestSiteInternal.UartSend(0, data, ValueError("data is None"))

    # -----------------------------
    # Test: UartReceive Api
    # This test verifies the API itslef.  It verifies valid as well as invalid parameters.
    # -----------------------------
    def test_uart_receive_api(setup_teardown):
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartReceive: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage)
        maxRxBytes = 65536

        for uart_id in UartId_Internal:
            setup_teardown.log_step(f"Testing {uart_id}")

            if uart_id in validUarts:
                TestSiteInternal.UartReceive(uart_id, 1, 0.0)
            else:
                notImplementedUartReceive = ClientException(TER_Status.TER_Status_NotImplemented, "UartReceive")
                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.UartReceive(uart_id, 1, 0.0, notImplementedUartReceive)
                assert str(excinfo.value) == "NotImplemented"

        setup_teardown.log_step("Testing exceptions")

        min_value = min(UartId_Internal) - 1
        max_value = max(UartId_Internal) + 1

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(min_value, 1, 0.0, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(max_value, 1, 0.0, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        min_bytes = -1
        max_bytes = maxRxBytes + 1

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(0, min_bytes, 0.0, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(0, max_bytes, 0.0, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(0, 1, -0.001, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartReceive(0, 1, 2.0011, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

    # -----------------------------
    # Test: UartGetStatus Api
    # -----------------------------
    def test_uart_get_status_api(setup_teardown):
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartGetStatus: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, argumentInvalidMessage)

        for uart_id in UartId_Internal:
            setup_teardown.log_step(f"Testing {uart_id}")

            if uart_id in validUarts:
                TestSiteInternal.UartGetStatus(uart_id)
            else:
                notImplementedUartGetStatus = ClientException(TER_Status.TER_Status_NotImplemented, "UartGetStatus")
                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.UartGetStatus(uart_id, notImplementedUartGetStatus)
                assert str(excinfo.value) == str(notImplementedUartGetStatus)

        setup_teardown.log_step("Testing exceptions")

        min_value = min(UartId_Internal) - 1
        max_value = max(UartId_Internal) + 1

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartGetStatus(min_value, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

        with pytest.raises(ClientException) as excinfo:
            TestSiteInternal.UartGetStatus(max_value, argumentInvalidException)
        assert str(excinfo.value) == argumentInvalidMessage

    # -----------------------------
    # Test: UartLogging Api
    # -----------------------------
    def test_uart_logging_api(setup_teardown):
        loggingAlreadyStartedException = ClientException(TER_Status.TER_Status_LoggingAlreadyStarted, "StartLogging")
        loggingAlreadyStoppedException = ClientException(TER_Status.TER_Status_LoggingAlreadyStopped, "StopLogging")
        argumentInvalidExceptionWhenStartLogging = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, "StartLogging")
        argumentInvalidExceptionWhenStopLogging = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, "StopLogging")
        argumentInvalidExceptionWhenSyncLogging = ClientException(TER_Status.TER_Status_Error_Argument_Invalid, "SyncLogging")

        for uart_id in UartId_Internal:
            log_id = logIdDict.get(uart_id, LogId_Internal.Log_Id_Invalid)
            setup_teardown.log_step(f"Testing {uart_id} with {log_id}")

            if uart_id in validUarts and log_id != LogId_Internal.Log_Id_Invalid:
                TestSiteInternal.StartLogging(log_id)
                TestSiteInternal.StartLogging(log_id, loggingAlreadyStartedException)

                TestSiteInternal.SyncLogging(log_id)

                TestSiteInternal.StopLogging(log_id)
                TestSiteInternal.StopLogging(log_id, loggingAlreadyStoppedException)
            else:
                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.StartLogging(log_id, argumentInvalidExceptionWhenStartLogging)
                assert str(excinfo.value) == str(argumentInvalidExceptionWhenStartLogging)

                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.SyncLogging(log_id, argumentInvalidExceptionWhenSyncLogging)
                assert str(excinfo.value) == str(argumentInvalidExceptionWhenSyncLogging)

                with pytest.raises(ClientException) as excinfo:
                    TestSiteInternal.StopLogging(log_id, argumentInvalidExceptionWhenStopLogging)
                assert str(excinfo.value) == str(argumentInvalidExceptionWhenStopLogging)


    # -----------------------------
    # Test: Uart send_receive_with_no_timeout
    # -----------------------------
    def test_uart_send_receive_with_no_timeout(setup_teardown):
        tx_data = setup_teardown.GenerateBuffer(SendByteCount)

        for uart_id in validUarts:
            setup_teardown.LogStep(f"Testing {uart_id}")

            setup_teardown.UartSetLoopbackMode(uart_id, True)

            for baud_rate in validBaudRates:
                temp_data = bytearray()
                total_bytes = 0

                start_time = datetime.now()

                setup_teardown.UartSetBaudRate(uart_id, baud_rate)

                # Flush any data that may be present.
                while len(temp_data) != 0:
                    temp_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, 2.0)

                for _ in range(TotalCount):
                    rx_data = bytearray()
                    retries = 10000
                    count = 0

                    TestSiteInternal.UartSend(uart_id, tx_data, suppress_pass=True)

                    while len(rx_data) < SendByteCount and count < retries:
                        count += 1
                        bytes_received = TestSiteInternal.UartReceive(uart_id, SendByteCount, timeout, suppress_pass=True)
                        rx_data.extend(bytes_received)

                    total_bytes += len(rx_data)

                    if count < retries:
                        if setup_teardown.Compare("bytes receive", SendByteCount, len(rx_data)) == "Pass":
                            if setup_teardown.CompareBinary("WriteVsRead", tx_data, rx_data) == "Pass":
                                setup_teardown.LogResult("Pass", f"{uart_id} {baud_rate} data", "Expect: ", "Match", "Actual: ", "Match")
                    else:
                        setup_teardown.LogResult("FAIL", f"Timed out - received {len(rx_data)} bytes")

                end_time = datetime.now()
                elapsed_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds

                setup_teardown.LogMessage(f"{uart_id} {baud_rate} - TotalTimeMs = {elapsed_time}, TotalBytes = {total_bytes}")

            uart_status = TestSiteInternal.UartGetStatus(uart_id)
            setup_teardown.Compare(f"{uart_id} - RX FIFO Overflow Count", 0, uart_status.rxFifoOverflowCount)
            setup_teardown.Compare(f"{uart_id} - RX Buff Overflow Count", 0, uart_status.rxBufferOverflowCount)

            setup_teardown.UartSetLoopbackMode(uart_id, False)

    # -----------------------------
    # Test: Uart send receive wit timeout
    # -----------------------------
    def test_uart_send_receive_with_timeout(setup_teardown):
        tx_data = setup_teardown.GenerateBuffer(SendByteCount)

        for uart_id in validUarts:
            setup_teardown.LogStep(f"Testing {uart_id}")

            setup_teardown.UartSetLoopbackMode(uart_id, True)

            for baud_rate in validBaudRates:
                temp_data = bytearray()

                setup_teardown.UartSetBaudRate(uart_id, baud_rate)

                # Flush any data that may be present.
                while len(temp_data) != 0:
                    temp_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, 2.0)

                for _ in range(TotalCount):
                    TestSiteInternal.UartSend(uart_id, tx_data, suppress_pass=True)

                    rx_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, timeout, suppress_pass=True)

                    if setup_teardown.Compare("bytes received", SendByteCount, len(rx_data)) == "Pass":
                        if setup_teardown.CompareBinary("WriteVsRead", tx_data, rx_data) == "Pass":
                            setup_teardown.LogResult("Pass", f"{uart_id} {baud_rate} data", "Expect: ", "Match", "Actual: ", "Match")

            uart_status = TestSiteInternal.UartGetStatus(uart_id)
            setup_teardown.Compare(f"{uart_id} - RX FIFO Overflow Count", 0, uart_status.rxFifoOverflowCount)
            setup_teardown.Compare(f"{uart_id} - RX Buff Overflow Count", 0, uart_status.rxBufferOverflowCount)

            setup_teardown.UartSetLoopbackMode(uart_id, False)

    # -----------------------------
    # Test: Uart partial receive
    # -----------------------------
    def test_uart_partial_receive(setup_teardown):
        for uart_id in validUarts:
            setup_teardown.LogStep(f"Testing {uart_id}")

            setup_teardown.UartSetLoopbackMode(uart_id, True)

            for baud_rate in validBaudRates:
                temp_data = bytearray()

                setup_teardown.UartSetBaudRate(uart_id, baud_rate)

                # Flush any data that may be present.
                while len(temp_data) != 0:
                    temp_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, 2.0)

                TestSiteInternal.UartSend(uart_id, txData, suppress_pass=True)

                rx_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, timeout, suppress_pass=True)

                if setup_teardown.Compare("bytes received", len(txData), len(rx_data)) == "Pass":
                    if setup_teardown.CompareBinary("WriteVsRead", txData, rx_data) == "Pass":
                        setup_teardown.LogResult("Pass", f"{uart_id} {baud_rate} data", "Expect: ", "Match", "Actual: ", "Match")

            uart_status = TestSiteInternal.UartGetStatus(uart_id)
            setup_teardown.Compare(f"{uart_id} - RX FIFO Overflow Count", 0, uart_status.rxFifoOverflowCount)
            setup_teardown.Compare(f"{uart_id} - RX Buff Overflow Count", 0, uart_status.rxBufferOverflowCount)

            setup_teardown.UartSetLoopbackMode(uart_id, False)


    def WaitForUartLogFile(file_name):
        start_time = time.time()
        while not os.path.exists(file_name) and (time.time() - start_time) < 300:
            time.sleep(0.1)
        elapsed_time = time.time() - start_time
        print(f"Uart log file created {file_name} in {elapsed_time * 1000} milliseconds")


    async def DoPeriodicUartLogFileSync(testSiteInternal):
        while True:
            for uart_id in validUarts:
                if logIdDict.get(uart_id, -1) != -1:
                    testSiteInternal.SyncLogging(logIdDict[uart_id])
            await asyncio.sleep(2)  # Wait 2 seconds before the next sync

    # -----------------------------
    # Test: Uart logging sunction
    # -----------------------------
    def test_uart_logging_functional(setup_teardown):
        tx_data = setup_teardown.GenerateBuffer(SendByteCount)

        TestSite = MagicMock()
        TestSite.Reset(ResetType=MagicMock(SiteReset=0))

        SYNC_TIMER_MS = 2.0
        loop = asyncio.get_event_loop()
        loop.call_later(SYNC_TIMER_MS, DoPeriodicUartLogFileSync, TestSiteInternal)

        for uart_id in validUarts:
            log_id = logIdDict.get(uart_id, -1)
            setup_teardown.LogStep(f"Testing {uart_id} with {log_id}")

            if uart_id in validUarts and log_id != -1:
                setup_teardown.UartSetLoopbackMode(uart_id, True)

                for baud_rate in validBaudRates:
                    temp_data = bytearray()

                    setup_teardown.UartSetBaudRate(uart_id, baud_rate)

                    while len(temp_data) != 0:
                        temp_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, 2.0)

                    file_name = TestSiteInternal.StartLogging(log_id)

                    TestSiteInternal.UartSend(uart_id, tx_data, suppress_pass=True)

                    rx_data = TestSiteInternal.UartReceive(uart_id, SendByteCount, timeout, suppress_pass=True)

                    setup_teardown.Compare(f"{uart_id} {baud_rate} api size", len(tx_data), len(rx_data))

                    if setup_teardown.CompareBinary("validate api", tx_data, rx_data) == "Pass":
                        setup_teardown.LogResult("Pass", f"{uart_id} {baud_rate} api data", "Expect: ", "Match", "Actual: ",
                                                 "Match")

                    TestSiteInternal.ConnectToNetworkPath(file_name, "cpc", "Teradyne")
                    WaitForUartLogFile(file_name)
                    TestSiteInternal.DisconnectFromNetworkPath(file_name)

                    with open(file_name, "rb") as file_stream:
                        while os.path.getsize(file_name) < SendByteCount:
                            time.sleep(0.1)  # Waiting for periodic sync to commit bytes to disk file

                        total_bytes_read = 0
                        retries = 0
                        max_retries = 10
                        file_data = bytearray(SendByteCount)

                        while total_bytes_read < SendByteCount and retries < max_retries:
                            bytes_read = file_stream.readinto(file_data[total_bytes_read:])
                            total_bytes_read += bytes_read
                            retries += 1

                    setup_teardown.Compare(f"{uart_id} {baud_rate} file size", SendByteCount, total_bytes_read)

                    if setup_teardown.CompareBinary("validate file", tx_data, file_data) == "Pass":
                        setup_teardown.LogResult("Pass", f"{uart_id} {baud_rate} file data", "Expect: ", "Match",
                                                 "Actual: ", "Match")

                    TestSiteInternal.StopLogging(logIdDict[uart_id])

                    uart_status = TestSiteInternal.UartGetStatus(uart_id)
                    setup_teardown.Compare("RX FIFO Overflow Count", 0, uart_status.rxFifoOverflowCount)
                    setup_teardown.Compare("RX Buff Overflow Count", 0, uart_status.rxBufferOverflowCount)

                setup_teardown.UartSetLoopbackMode(uart_id, False)
            else:
                print(f"{uart_id} is valid for {SltPlatform}, but has no uart log implemented yet")

        loop.stop()


    # -----------------------------
    # test uart_get_status_functional
    # -----------------------------
    def test_uart_get_status_functional(setup_teardown):
        rxFifoSize = 32 * 1024
        rxBufferSize = 5 * 1024 * 1024
        txData = setup_teardown.GenerateBuffer(SendByteCount)

        for uart_id in validUarts:
            setup_teardown.LogStep(f"Testing {uart_id}")

            TestSite.Reset(ResetType.SiteReset)

            site_status = TestSite.GetSiteStatus()

            setup_teardown.Compare(f"{uart_id} - uart alarm check after site reset", False,
                                  site_status.testerAlarmBits.HasFlag(TesterAlarmBits.InternalBusFault))

            uart_status = TestSiteInternal.UartGetStatus(uart_id)

            setup_teardown.Compare(f"{uart_id} rxFifoOverflowCount", 0, uart_status.rxFifoOverflowCount)
            setup_teardown.Compare(f"{uart_id} rxBufferOverflowCount", 0, uart_status.rxBufferOverflowCount)

            setup_teardown.UartSetLoopbackMode(uart_id, True)

            setup_teardown.UartSetPollingMode(uart_id, False)

            for bytes_sent in range(0, rxFifoSize, SendByteCount):
                TestSiteInternal.UartSend(uart_id, txData, suppress_pass=True)

            time.sleep(1)

            setup_teardown.UartSetPollingMode(uart_id, True)

            ComprehensiveTests = False  # Set this flag based on your requirement
            if ComprehensiveTests:
                setup_teardown.UartSetBaudRate(uart_id, 1500000)

                for bytes_sent in range(0, rxBufferSize, SendByteCount):
                    TestSiteInternal.UartSend(uart_id, txData, suppress_pass=True)

                TestSiteInternal.UartSend(uart_id, bytearray([1]), suppress_pass=True)

            time.sleep(0.2)

            setup_teardown.UartSetLoopbackMode(uart_id, False)

            site_status = TestSite.GetSiteStatus()

            if uart_id != 3:  # Assuming UartId_Internal.Fp_Uart = 3
                setup_teardown.Compare(f"{uart_id} - uart alarm check after enable polling mode but disable loopback",
                                      True, site_status.testerAlarmBits.HasFlag(TesterAlarmBits.InternalBusFault))
            else:
                IsSubSltPlatformCayman = False  # Set this flag based on your requirement
                if IsSubSltPlatformCayman:
                    setup_teardown.Compare(f"{uart_id} - uart alarm check after enable polling mode but disable loopback",
                                          True, site_status.testerAlarmBits.HasFlag(TesterAlarmBits.InternalBusFault))
                else:
                    setup_teardown.Compare(f"{uart_id} - uart alarm check after enable polling mode but disable loopback",
                                          False, site_status.testerAlarmBits.HasFlag(TesterAlarmBits.InternalBusFault))

            uart_status = TestSiteInternal.UartGetStatus(uart_id)

            if ComprehensiveTests:
                setup_teardown.Compare(f"{uart_id} rxFifoOverflowCount", 0, uart_status.rxFifoOverflowCount,
                                      compare_func="CompareNot")
                setup_teardown.Compare(f"{uart_id} rxBufferOverflowCount", 0, uart_status.rxBufferOverflowCount,
                                      compare_func="CompareNot")
            else:
                setup_teardown.Compare(f"{uart_id} rxFifoOverflowCount", 0, uart_status.rxFifoOverflowCount,
                                      compare_func="CompareNot")
                setup_teardown.Compare(f"{uart_id} rxBufferOverflowCount", 0, uart_status.rxBufferOverflowCount)

            TestSite.Reset(ResetType.SiteReset)

            site_status = TestSite.GetSiteStatus()

            setup_teardown.Compare(f"{uart_id} - uart alarm check after site reset", False,
                                  site_status.testerAlarmBits.HasFlag(TesterAlarmBits.InternalBusFault))

            uart_status = TestSiteInternal.UartGetStatus(uart_id)
            setup_teardown.Compare(f"{uart_id} rxFifoOverflowCount", 0, uart_status.rxFifoOverflowCount)
            setup_teardown.Compare(f"{uart_id} rxBufferOverflowCount", 0, uart_status.rxBufferOverflowCount)

# -----------------------------
# For direct execution of tests, run: pytest <test_UART.py>
# -----------------------------

@allure.feature("Sample Test Suite")
class TestSample:

    @allure.story("Test Addition")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_addition(self):
        """Test case for addition"""
        a, b = 5, 3
        result = a + b
        assert result == 8, "Addition result is incorrect"

    @allure.story("Test Subtraction")
    @allure.severity(allure.severity_level.NORMAL)
    def test_subtraction(self):
        """Test case for subtraction"""
        a, b = 10, 4
        result = a - b
        assert result == 6, "Subtraction result is incorrect"

    @allure.story("Test Multiplication")
    @allure.severity(allure.severity_level.MINOR)
    def test_multiplication(self):
        """Test case for multiplication"""
        a, b = 7, 6
        result = a * b
        assert result == 42, "Multiplication result is incorrect"

    @allure.story("Test Division")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_division(self):
        """Test case for division"""
        a, b = 20, 5
        result = a / b
        assert result == 4, "Division result is incorrect"


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=./allure-results"])

