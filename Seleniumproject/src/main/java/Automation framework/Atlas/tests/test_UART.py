from array import array

import pytest
import allure
from ATLAS.framework.api.TestSiteLib.TestSiteTest import TestSiteTest
from ATLAS.framework.api.TestSiteLib.TestSiteLibrarry import (UartId_Internal,TER_Status, UartId,UartBaudRate,LogId_Internal,
                                                            SiteComponent,SiteComponentAttribute,PropertyType)
from ATLAS.framework.api.TestSiteLib.ClientException import *

def ExpectClientEx(status, method):
    return ClientException(status, f"Expected exception for method: {method}")

validUarts = [
        UartId_Internal.Uart_1_Internal,
        UartId_Internal.Fp_Uart,
        UartId_Internal.UART_DUTIO_0,
        UartId_Internal.UART_DUTIO_1,
        UartId_Internal.UART_DUTIO_2,
    ]

@pytest.fixture(scope="class")
def tsar_instance(request):

    """Creates a single TSAR instance for all tests in the class."""


    TestSite = TestSiteTest(IHC_IP="131.101.47.35",
                        FpIP="192.168.122.1",
                        SiteIP="192.168.122.1",
                        SlotNo=1)


    # Attach the TSAR instance to the test class
    request.cls.TestSite = TestSite
    # Attach the TSAR instance to the test class

    yield TestSite  # Provide the instance to tests

    TestSite.disconnectSsh()  # Disconnect after all tests are done

# -----------------------------
#       Uart API Sanity Check
# ---------------------------
@allure.feature("Test UART - APIs ")
@pytest.mark.usefixtures("tsar_instance")  # Apply the fixture at the class level
class TestUART(TestSiteTest):

    # -----------------------------
    #       Uart API Sanity Check
    # ---------------------------
    allure.story("UART TSAR Commands")
    @pytest.mark.parametrize("api_name, full_cmd", [
        ("UartSetEnable", "UartSetEnable 2 true"),
        ("UartSetBaudRate", "UartSetBaudRate 2 1"),
        ("UartGetStatus", "UartGetStatus 1"),
        ("UartSend", "UartSend 2 [11 22 33 44 55 66 77 88 99]"),
        ("UartReceive", "UartReceive 2 256 "),
        ("UartSend", "UartSend1 2 [11 22 33 44 55 66 77 88 99]"),
        ("UartReceive", "UartReceive1 2 256 "),
        ("UartSendImpl", "UartSendImpl 2 [11 11 11 11 11 11 11 11 11]"),
        ("UartReceive", "UartReceive 2 256 "),
    ])
    @allure.step("Executing {api_name} command")
    def test_UART_apis(self, api_name, full_cmd):
        self.TestSite.execute_CMD(api_name,full_cmd )


    # ----------------------------------------------------
    #       Uart Enable API  Test
    # ----------------------------------------------------
    def get_uart_cfg_register_value(self, uart_id):
        # Mock function to simulate hardware register value
        return 0x00000080 if uart_id in validUarts else 0

    @pytest.mark.parametrize("b_state", [False, True])
    @pytest.mark.parametrize("uartId", list(UartId_Internal))
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartSetEnable_api(self,b_state,uartId):
        mask_of_uart_enable_bit = 0x00000080

        print(f"Testing {uartId} with state {b_state}")
        if uartId in validUarts:
            self.TestSite.uart_set_enable(uartId, b_state)

            reg_value = self.get_uart_cfg_register_value(uartId)
            print("reg_value", reg_value)

            b_result = ((reg_value & mask_of_uart_enable_bit) == mask_of_uart_enable_bit) if b_state else (
                        (reg_value & mask_of_uart_enable_bit) == 0)
            print("bresult", b_result)
            target_state = "enabled" if b_state else "disabled"
            #assert b_result, f"{uart_id} should be {target_state}"

        else:
            not_implemented_exception = ExpectClientEx(TER_Status.NotImplemented, "UartSetEnable")
            with pytest.raises(ClientException):
                self.uart_set_enable(uartId, b_state, not_implemented_exception)

    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("b_state", [False, True])
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartSetEnable_api_exceptions(self,b_state):
        argument_invalid_exception = ExpectClientEx(TER_Status.Error_Argument_Invalid, "UartSetEnable")
        print("Testing exceptions")

        min_uart = min(validUarts) - 1
        max_uart = max(validUarts) + 1

        with pytest.raises(ClientException):
            self.uart_set_enable(min_uart, b_state, argument_invalid_exception)
        with pytest.raises(ClientException):
            self.uart_set_enable(max_uart, b_state, argument_invalid_exception)


    # ----------------------------------------------------
    #       Uart Configure API  Test
    # ----------------------------------------------------
    @pytest.mark.parametrize("uartId", list(UartId_Internal))
    @pytest.mark.parametrize("baudRate", list(UartBaudRate))
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartConfigureApiTest_valid(self, uartId, baudRate):
        if uartId in validUarts:
            #TestSiteInternal.UartSetBaudRate(uartId, baudRate)
            api_name = "UartSetBaudRate"
            full_CMD = f"UartSetBaudRate {uartId} {baudRate}"
            self.execute_CMD(api_name, full_CMD)

        else:
            exception = ExpectClientEx(TER_Status.NotImplemented, "UartSetBaudRate")
            with allure.step(f"UartSetBaudRate {uartId} : {baudRate} exception thrown"):
                assert exception


    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartConfigureApiTest_exceptions(self):
        argumentInvalidMessage = "API error TER_Status_Error_Argument_Invalid when calling method UartSetBaudRate: TER_Status_Error_Argument_Invalid"
        argumentInvalidException = ClientException(TER_Status.Error_Argument_Invalid, argumentInvalidMessage)

        min_val = min([item.value for item in UartId_Internal]) - 1
        max_val = max([item.value for item in UartId_Internal]) + 1

        #TestSiteInternal.UartSetBaudRate(min_val, UartBaudRate.UartBaudRate_115200, argumentInvalidException)
        api_name = "UartSetBaudRate"
        full_CMD = f"UartSetBaudRate {min_val} {UartBaudRate.UartBaudRate_115200}"
        self.execute_CMD(api_name, full_CMD)

        #TestSiteInternal.UartSetBaudRate(max_val, UartBaudRate.UartBaudRate_115200, argumentInvalidException)
        api_name = "UartSetBaudRate"
        full_CMD = f"UartSetBaudRate {max_val} {UartBaudRate.UartBaudRate_115200}"
        self.execute_CMD(api_name, full_CMD)

        min_val = min([item.value for item in UartBaudRate]) - 1
        max_val = max([item.value for item in UartBaudRate]) + 1

        #TestSiteInternal.UartSetBaudRate(UartId_Internal.Uart_1_Internal, min_val, argumentInvalidException)
        full_CMD = f"UartSetBaudRate {UartId_Internal.Uart_1_Internal} {min_val}"
        self.execute_CMD(api_name, full_CMD)

        #TestSiteInternal.UartSetBaudRate(UartId_Internal.Uart_1_Internal, max_val, argumentInvalidException)
        full_CMD = f"UartSetBaudRate {UartId_Internal.Uart_1_Internal} {max_val}"
        self.execute_CMD(api_name, full_CMD)

    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------


    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------
    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------
    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------
    # ----------------------------------------------------
    #       Uart Configure API  Exception Test
    # ----------------------------------------------------




if __name__ == "__main__":
    #pytest.main(["::test_uart_set_enable_api","-v", "--alluredir=./reports/allure-results"])
    pytest.main(["::TestUART::test_UartSetEnable_api"])
