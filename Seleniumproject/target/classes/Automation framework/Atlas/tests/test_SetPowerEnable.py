from array import array

import pytest
import allure
from ATLAS.framework.api.TestSiteLib.TestSiteRunner import TSAR
from ATLAS.framework.api.TestSiteLib.TestSiteLibrarry import (UartId_Internal, TER_Status, RailId, SiteStatus,
                                                              SiteComponent, SiteComponentAttribute, StatusBits)

from typing import Callable, TypeVar, Optional

from ATLAS.framework.api.TestSiteLib.ClientException import *

def ExpectClientEx(status, method):
    return ClientException(status, f"Expected exception for method: {method}")


T = TypeVar('T')


class TestStatus:
    PASS = "Pass"
    FAIL = "Fail"


def default_compare(x: T, y: T) -> bool:
    """Default comparison function using equality."""
    return x == y


def format_value(value: T, fmt: str) -> str:
    """Formats the value based on the provided format string."""
    if value is None:
        return "(null)"
    try:
        return f"{value:{fmt}}" if fmt else str(value)
    except (ValueError, TypeError):
        return f"[Invalid Format: {fmt}]"


def log_result(status: str, message: str, exp_label: str, exp_str: str, act_label: str, act_str: str, options: str):
    """Placeholder function to log the comparison results."""
    print(f"{status}: {message}")
    print(f"{exp_label} {exp_str}, {act_label} {act_str}, Options: {options}")


def Compare(
        message: str,
        expect: T,
        actual: T,
        compare_func: Optional[Callable[[T, T], bool]] = None,
        options: str = "",
        fmt: str = ""
) -> str:
    """Compares expected and actual values and logs the result."""

    exp_str = format_value(expect, fmt)
    act_str = format_value(actual, fmt)

    compare_func = compare_func or default_compare
    exp_label = "Expected"

    status = TestStatus.PASS if compare_func(expect, actual) else TestStatus.FAIL

    log_result(status, message, f"{exp_label}:", exp_str, "Actual:", act_str, options)

    return status



class CarrierType:
    Magnus = "Magnus"
    Mtk = "Mtk"
    Titan = "Titan"

class VoltageLimit:
    def __init__(self, min, max):
        self.min = min
        self.max = max

class SltbTypeVotlageSettings:
    def __init__(self, vbatMin, vbatMax, vbatVoltageTarget, vbatVoltageLimit, vbatVoltageLimitPeriod,
                 vbatVoltageTolerancePeriod, vbatVoltageTolerancePercent, vbatCurrentLimit,
                 vbatCurrentLimitPeriod, vbulkCurrentLimit, vbulkCurrentPeriod):
        self.vbatMin = vbatMin
        self.vbatMax = vbatMax
        self.vbatVoltageTarget = vbatVoltageTarget
        self.vbatVoltageLimit = vbatVoltageLimit
        self.vbatVoltageLimitPeriod = vbatVoltageLimitPeriod
        self.vbatVoltageTolerancePeriod = vbatVoltageTolerancePeriod
        self.vbatVoltageTolerancePercent = vbatVoltageTolerancePercent
        self.vbatCurrentLimit = vbatCurrentLimit
        self.vbatCurrentLimitPeriod = vbatCurrentLimitPeriod
        self.vbulkCurrentLimit = vbulkCurrentLimit
        self.vbulkCurrentPeriod = vbulkCurrentPeriod

class SetupData:
    def __init__(self, TargetRailID, TargetValueV, MarginOnV, MarginOffV, TargetValueC,
                 MarginOnC, MarginOffC, HasLoad, ex):
        self.TargetRailID = TargetRailID  # could be internal rail ID or public rail ID
        self.TargetValueV = TargetValueV
        self.MarginOnV = MarginOnV
        self.MarginOffV = MarginOffV
        self.TargetValueC = TargetValueC
        self.MarginOnC = MarginOnC
        self.MarginOffC = MarginOffC
        self.HasLoad = HasLoad
        self.ex = ex

class Power:
    def __init__(self):
        self.UseLid: bool = False
        self.HasFixedLoad: bool = False
        self.HasVariableLoad: bool = False
        self.HasFixedRemoteSense: bool = False
        self.HasVariableRemoteSense: bool = False
        self.FixedRailVoltageOnTolerance: float = 0.0
        self.FixedRailVoltageOffTolerance: float = 0.0
        self.FixedRailCurrentTarget: float = 0.0
        self.FixedRailCurrentOnTolerance: float = 0.0
        self.FixedRailCurrentOffTolerance: float = 0.0
        self.VariableRailVoltageOnTolerance: float = 0.0
        self.VariableRailVoltageOffTolerance: float = 0.0
        self.VariableRailCurrentTarget: float = 0.0
        self.VariableRailCurrentOnTolerance: float = 0.0
        self.VariableRailCurrentOffTolerance: float = 0.0
        self.ValidLamdaPowerSupply: bool = True

        self.StatusPollCount: int = 23
        self.SetupDataDictionary: Dict[str, dict] = {}

        self.eTER_Status_PowerEnabledError: Optional[Exception] = None
        self.eTER_Status_PowerEnabledError_Lid: Optional[Exception] = None
        self.eTER_Status_SltbRailInvalid: Optional[Exception] = None
        self.eTER_Status_LidNotClosedError: Optional[Exception] = None

        self.fixedRailVoltageTarget: float = 24.0
        self.variableRailVoltageTarget: float = 0.0


@pytest.fixture(scope="class")
def tsar_instance(request):
    """Creates a single TSAR instance for all tests in the class."""
    tsar = TSAR(UserName="cpc", Password="Teradyne",
                IhcIP="131.101.47.35",
                FpIP="192.168.122.1",
                SiteIP="192.168.122.1", SlotNo=1)
    tsar.ConnectSsh()

    # Attach the TSAR instance to the test class
    request.cls.tsar_instance = tsar

    yield tsar  # Provide the instance to tests

    tsar.disconnectSsh()  # Disconnect after all tests are done

# -----------------------------
#       Uart API Sanity Check
# ---------------------------
@allure.feature("Test Set Power Enable- APIs ")
@pytest.mark.usefixtures("tsar_instance")  # Apply the fixture at the class level
class TestSetPowerEnable:

    def execute_CMD(self,api_name, full_CMD):
        print("Full CMD : ",full_CMD)
        result, reply = self.tsar_instance.executeSsh_Command(api_name, full_CMD)
        print("Resp :", reply)
        with allure.step(f" {api_name} : {reply}"):
            assert result == True, f"TSAR command {api_name} failed"
        return reply

    # -----------------------------
    #       PowerSet Enable API Sanity Check
    # ---------------------------
    #TestSite.PowerSetEnable(RailId.Variable_1, true);
    allure.story("PowerSet Enable TSAR Commands")
    @pytest.mark.parametrize("api_name, full_cmd", [
        ("PowerSetEnable", f"PowerSetEnable {RailId.Variable_1} true"),
    ])
    @allure.step("Executing {api_name} command")
    def test_PowerSetEnable_apis(self, api_name, full_cmd):
        self.execute_CMD(api_name, full_cmd)

    # ----------------------------------------------------
    #       PowerSetEnable API  Test
    # ----------------------------------------------------
    @pytest.mark.parametrize("RailId", list(RailId))
    @allure.severity(allure.severity_level.CRITICAL)
    def test_UartConfigureApiTest_valid(self, RailId ):

        # TestSiteInternal.UartSetBaudRate(uartId, baudRate)
        api_name = "PowerSetEnable"
        full_CMD = f"PowerSetEnable {RailId} {"True"}"
        self.execute_CMD(api_name, full_CMD)



    # ----------------------------------------------------
    #       test VBat
    # ----------------------------------------------------
    @allure.severity(allure.severity_level.CRITICAL)
    def test_VBat(self):
        tpnLengthToCompare = 8
        magnusPimPartNumber = ["000-000-00", "660-752-00", "661-561-60", "670-026-00"]
        magnus5vPimPartNumber = ["699-294-00"]
        titanPimPartNumber = ["651-178-00", "652-564-60", "656-636-00"]

        pimPartNumbers = {
            CarrierType.Magnus: magnusPimPartNumber,
            CarrierType.Mtk: magnus5vPimPartNumber,
            CarrierType.Titan: titanPimPartNumber
        }

        voltageLimits = {
            CarrierType.Magnus: VoltageLimit(min=3.4, max=10.0),
            CarrierType.Mtk: VoltageLimit(min=3.4, max=10.0),
            CarrierType.Titan: VoltageLimit(min=3.4, max=4.5)
        }

        #pimPartNumber = TestSite.GetAttribute(SiteComponent.CarrierBoard, SiteComponentAttribute.PartNumber)
        api_name = "GetAttribute"
        full_CMD = f"GetAttribute {SiteComponent.CarrierBoard} {SiteComponentAttribute.PartNumber}"
        resp= self.execute_CMD(api_name, full_CMD)
        print(resp)
        pimPartNumber = resp


        carrierType = CarrierType.Titan  # Defaults to Titan.

        for keyValuePair in pimPartNumbers.items():
            for partNumber in keyValuePair[1]:
                if pimPartNumber[:tpnLengthToCompare] == partNumber[:tpnLengthToCompare]:
                    carrierType = keyValuePair[0]

        vBatMinDef = voltageLimits[carrierType].min
        vBatMaxDef = voltageLimits[carrierType].max
        vBatTarget = vBatMinDef
        stepV = (vBatMaxDef - vBatMinDef) / 5

        while vBatTarget <= vBatMaxDef:
            powerSettings = SltbTypeVotlageSettings(
                vbatMin=vBatMinDef,
                vbatMax=vBatMaxDef,
                vbatVoltageTarget=vBatTarget,
                vbatVoltageLimit=vBatTarget + 0.8,
                vbatVoltageLimitPeriod=5.0 / 1024.0,
                vbatVoltageTolerancePercent=6.0,
                vbatVoltageTolerancePeriod=5.0 / 1024.0,
                vbatCurrentLimit=6.0,
                vbatCurrentLimitPeriod=5.0 / 1024.0,
                vbulkCurrentLimit=2.0,
                vbulkCurrentPeriod=5.0 / 1024.0,
            )

            powerTolerance = SetupData(
                TargetRailID=int(RailId.Variable_1),
                TargetValueV=vBatTarget,
                MarginOnV=Power.VariableRailVoltageOnTolerance,
                MarginOffV=Power.VariableRailVoltageOffTolerance,
                TargetValueC=Power.VariableRailCurrentTarget,
                MarginOnC=Power.VariableRailCurrentOnTolerance,
                MarginOffC=Power.VariableRailCurrentOffTolerance,
                HasLoad=True,
                ex=None
            )

            #SetTitanPowerParameters(powerSettings)

            #TestSite.PowerSetEnable(RailId.Variable_1, True)
            api_name = "PowerSetEnable"
            full_CMD = f"PowerSetEnable {RailId.Variable_1} {"True"}"
            resp = self.execute_CMD(api_name, full_CMD)
            print(resp)



            #CheckRailOn(True, powerTolerance)  # Check by site status.


            #siteStatus = TestSite.GetSiteStatus()
            api_name = "GetSiteStatus"
            full_CMD = f"GetSiteStatus"
            resp = self.execute_CMD(api_name, full_CMD)
            print(resp)
            # based on respons
            SiteStatus.statusBits = 0x01

            siteEnergized = (siteStatus.statusBits & StatusBits.SiteEnergized) != 0
            Compare("SiteEnergized-VBat ON", True, siteEnergized)

            #TestSite.PowerSetEnable(RailId.Variable_1, False)


            CheckRailOn(False, powerTolerance)  # Check by site status.

            #siteStatus = TestSite.GetSiteStatus()

            #siteStatus = TestSite.GetSiteStatus()
            api_name = "GetSiteStatus"
            full_CMD = f"GetSiteStatus"
            resp = self.execute_CMD(api_name, full_CMD)
            print(resp)
            # based on respons
            siteStatus = SiteStatus(
                alarmBits="ExampleAlarmBits",
                testerAlarmBits="ExampleTesterAlarmBits",
                statusBits=StatusBits,
                powerStatus=["ExamplePowerStatus"],
                thermalStatus="ExampleThermalStatus",
                AlarmDiagCode=["ExampleAlarmDiagCode"]
            )

            siteEnergized = (siteStatus.statusBits & StatusBits.SiteEnergized) != 0

            result = Compare("SiteEnergized-VBat OFF", False, siteEnergized)
            print("Test Result:", result)

            # Example usage
            #result = compare("Checking values", 100, 101, fmt=".2f")



            if stepV != 0.0:
                vBatTarget += stepV
            else:
                break



        #TestSiteInternal.UartSetBaudRate(UartId_Internal.Uart_1_Internal, max_val, argumentInvalidException)



if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=./reports/allure-results"])


