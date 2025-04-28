import pytest
import allure
import time
from ATLAS.framework.api.TestSiteLib.TestSiteRunner import TSAR


@pytest.fixture(scope="class")
def tsar_instance(request):
    """Creates a single TSAR instance for all tests in the class."""
    tsar = TSAR()
    success  = tsar.ConnectSsh()
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
    "get_SiteID",
    "GetMfgInfo",
    "GetPingCmd",
    "get_BuildInfo",
    "get_ErrorHandler",
    "get_WarningHandler",
    "GetBaseBoardAdcStatus",
    "GetComponents",
    "GetCrossWireInfo",
    "GetHashCode"
    "GetInfo",
    "GetLidStatus",
    "GetRebootCmd",
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
    "GetBuildInfo",
    "GetTemperature"
    ]

@allure.feature("TSAR SSH Commands")
@pytest.mark.usefixtures("tsar_instance")  # Apply the fixture at the class level
class TestTSAR:

    # @allure.story("Common Get TSAR Commands")
    # @pytest.mark.parametrize("api_name", TASR_GetAPI_List)
    # @allure.step("Executing {api_name} command")
    # def test_common_get_apis(self, api_name):
    #     full_CMD = api_name
    #     result,reply = self.tsar_instance.executeSsh_Command(api_name, full_CMD)
    #     with allure.step(f"{api_name} : {reply}"):
    #         assert result == True, f"TSAR command {api_name} failed"

    @allure.story("Power  TSAR Commands")
    #@pytest.mark.parametrize("api_name", TASR_GetAPI_List)
    #@allure.step("Executing {api_name} command")
    def test_common_set_Power_apis(self):
        api_name="PowerSetEnable"
        fix12v= 0x2000000

        full_CMD = f"PowerSetEnable {fix12v} {true}"
        reply = self.tsar_instance.executeSsh_Command(api_name, full_CMD)
        with allure.step(f"{api_name} : {reply}"):
            assert result == True, f"TSAR command {api_name} failed"



#

if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=./reports/allure-results"])
