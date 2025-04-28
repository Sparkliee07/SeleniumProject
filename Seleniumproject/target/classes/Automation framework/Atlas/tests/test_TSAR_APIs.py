import pytest
import allure
import time
import sys
import os
import logging

from django.utils.log import configure_logging
from setuptools.logging import configure

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ATLAS.framework.api.TestSiteLib.TestSiteRunner import TSAR
import logging

import logging

def configure_logging():
    # Configure logging
    log_file = "tsar_log.txt"  # Define the log file name
    logging.basicConfig(
        level=logging.INFO,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Define log format
        handlers=[
            logging.FileHandler(log_file),  # Log to file
            logging.StreamHandler()  # Log to console
        ]
    )




@pytest.fixture(scope="class")
def tsar_instance(request):
    """Creates a single TSAR instance for all tests in the class."""
    #tsar = TSAR( UserName="cpc",Password="Teradyne",IhcIP="131.101.47.35",FpIP="192.168.122.1",SiteIP="192.168.122.1")
    tsar = TSAR(UserName="cpc", Password="Teradyne",
                IhcIP="131.101.47.35", FpIP="192.168.122.1",
                SiteIP="192.168.122.1", SlotNo=1)
    success = tsar.ConnectSsh()
    if not success:
        pytest.fail("SSH connection failed. Aborting tests.")


    time.sleep(5)

    # Attach the TSAR instance to the test class
    request.cls.tsar_instance = tsar

    yield tsar  # Provide the instance to tests

    tsar.disconnectSsh()  # Disconnect after all tests are done

# -----------------------------
#       Get API List
# -----------------------------
TASR_GetAPI_List =[
    "get_BuildInfo",
    "get_ErrorHandler"
    "get_WarningHandler"
    "get_SiteID",

    "GetAttribute",
    "GetAttributes",
    "GetBaseBoardAdcStatus",
    "GetComponentAttributes",
    "GetComponents",
    "GetCrossWireInfo",

    "GetHashCode"
    "GetInfo",
    "GetLidStatus",
    "GetLogFileName",

    "GetMfgInfo",
    "GetPingCmd",
    "GetProperty",
    "GetProxyDutInsertionCount",
    "GetRebootCmd",
    "GetRegisters",

    "GetScripter",
    "GetSiteDutIOStatus",
    "GetSiteFanStatus",
    "GetSiteInfo",
    "GetSitePbPowerStatus",
    "GetSiteStatus",
    "GetSiteTcbPowerStatus",
    "GetSiteThermalStatusInternal",
    "GetSwitchBoardInfo",
    "GetSwitchBoardStatus",
    "GetSwitchBoardStatus1",

    "GetTemperatureStatus",
    "GetType",
    "GetUptimeCmd",
    "GetUsbStatus",
    "GetUserString",
    "GetVFPDevices",
    "GetVFPs",
    "GetWriteCrosswireInfo",

    ]
@allure.feature("TSAR SSH Commands")
@pytest.mark.usefixtures("tsar_instance")  # Apply the fixture at the class level
class TestTSAR:

    def execute_CMD(self,api_name, full_CMD):
        result, reply = self.tsar_instance.executeSsh_Command(api_name, full_CMD)
        with allure.step(f" {api_name} : {reply}"):
            assert result == True, f"TSAR command {api_name} failed"
        return reply

    @allure.story("Common Get TSAR Commands")
    @pytest.mark.parametrize("api_name", TASR_GetAPI_List)
    @allure.step("Executing {api_name} command")
    def test_common_get_apis(self, api_name):
        full_CMD = api_name
        result,reply = self.tsar_instance.executeSsh_Command(api_name, full_CMD)
        with allure.step(f"{api_name} : {reply}"):
            assert result == True, f"TSAR command {api_name} failed"

#

# -----------------------------
#       Uart API Sanity Check
# ---------------------------
    allure.story("UART TSAR Commands")
    @pytest.mark.parametrize("api_name, full_cmd", [
        ("UartSetEnable", "UartSetEnable 2 true"),
        ("UartSetBaudRate", "UartSetBaudRate 2 1"),
        ("UartReceive", "UartReceive 2 256 "),
    ])
    @allure.step("Executing {api_name} command")
    def test_Get_apis(self, api_name, full_cmd):
        self.execute_CMD(api_name,full_cmd )

if __name__ == "__main__":
    configure_logging()
    logging.info("Logging system initialized.")  # Example log message
    pytest.main(["-v", "--alluredir=./reports/allure-results"])
