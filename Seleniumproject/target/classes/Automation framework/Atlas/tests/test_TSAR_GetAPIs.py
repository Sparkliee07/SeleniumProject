from collections import defaultdict
import pytest
import allure
import time
import sys
import os
import logging


from ATLAS.framework.api.TestSiteLib.TestSiteRunner import TSAR
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.TestSiteLibrarry import SiteComponent,SiteComponentAttribute

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

def Compare(message, pattern, actual, comparison_type=None, options=None):
    # Mock comparison logic
    return TestStatus.Pass if comparison_type == "CompareRegex" else TestStatus.Pass




# Mock siteComponentAttributes dictionary
siteComponentAttributes = defaultdict(list)
ThermalBoardPresent = True
PowerBoardPresent = True
FunctionalProcessorPresent = True
IOBoardPresent = True
CoolantValvePresent = False
CarrierPresent = False

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
    #@pytest.mark.parametrize("api_name", TASR_GetAPI_List)
    @pytest.mark.parametrize("api_name", ["GetMfgInfo"])
    @allure.step("Executing {api_name} command")
    def test_common_get_apis(self, api_name):
        full_CMD = api_name
        self.execute_CMD(api_name,full_CMD)


    @allure.story("Get Mfg Info")
    def test_GetMfgInfo(self):
        # Simulate fetching manufacturing info
        mfgInfo = "ThermalBoard:PartNumber=123-456-78,SerialNumber=SN12345;PowerBoard:SerialNumber=PB12345,Revision=A1"

        # Separate site info into components
        actualComponents = [comp.strip() for comp in mfgInfo.split(';') if comp.strip()]
        print(actualComponents)

        for expectedComponent, expectedAttributes in siteComponentAttributes.items():
            expectFound = True
            if expectedComponent == SiteComponent.ThermalBoard:
                expectFound = ThermalBoardPresent
            elif expectedComponent == SiteComponent.PowerBoard:
                expectFound = PowerBoardPresent
            elif expectedComponent == SiteComponent.FunctionalProcessor:
                expectFound = FunctionalProcessorPresent
            elif expectedComponent == SiteComponent.IOBoard:
                expectFound = IOBoardPresent
            elif expectedComponent == SiteComponent.CoolantValve:
                expectFound = CoolantValvePresent
            elif expectedComponent in {SiteComponent.CarrierAssembly, SiteComponent.CarrierBoard}:
                expectFound = CarrierPresent

            actualAttributes = ""

            for component in actualComponents:
                componentName, componentAttributes = map(str.strip, component.split(':'))
                if componentName.lower() == expectedComponent.lower():
                    actualAttributes = componentAttributes
                    break

            if Compare(f"{expectedComponent} found", True, bool(actualAttributes)) == TestStatus.Pass:
                attributes = dict(
                    map(lambda pair: map(str.strip, pair.split('=')),
                        actualAttributes.split(',')))

                for expectedAttribute in expectedAttributes:
                    message = f"{expectedComponent} {expectedAttribute}"
                    actualAttribute = attributes.get(expectedAttribute, "")

                    if expectedAttribute == SiteComponentAttribute.PartNumber:
                        self.assertRegex(actualAttribute, r"^\d\d\d-\d\d\d-\d\d$")
                        self.assertNotEqual(actualAttribute, "ffffffffff")
                    elif expectedAttribute == SiteComponentAttribute.SerialNumber:
                        self.assertRegex(actualAttribute, r"^[a-zA-Z0-9]{8,}$")
                        self.assertNotEqual(actualAttribute, "ffffffff")
                    elif expectedAttribute == SiteComponentAttribute.Revision:
                        if len(actualAttribute) == 1:
                            self.assertRegex(actualAttribute, r"^[a-zA-Z]{1}$")
                            self.assertNotEqual(actualAttribute, "f")
                        elif len(actualAttribute) == 2:
                            self.assertRegex(actualAttribute, r"^[a-zA-Z]{1}[0-9]{1}$")
                            self.assertNotEqual(actualAttribute, "ff")
                        else:
                            self.assertLessEqual(len(actualAttribute), 2)
                    elif expectedAttribute == SiteComponentAttribute.RevisionDate:
                        self.assertRegex(actualAttribute, r"^\d\d\d\d[a-zA-Z]{1}$")
                        self.assertNotEqual(actualAttribute, "fffff")
                    elif expectedAttribute == SiteComponentAttribute.MacAddress:
                        self.assertRegex(actualAttribute, r"^([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2})$")
                        self.assertNotEqual(actualAttribute, "fffffffffffffffff")

# -----------------------------
#       Uart API Sanity Check
# ---------------------------


if __name__ == "__main__":
    configure_logging()
    logging.info("Logging system initialized.")  # Example log message
    pytest.main(["-v", "--alluredir=./reports/allure-results"])
