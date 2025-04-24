import socket
from typing import List, Optional, Dict
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.BaseTest import BaseTest

#==================================================
from enum import Enum
from typing import List, Dict, Optional
import ipaddress
import allure

from ATLAS.framework.api.TestSiteLib.TitanIpMapHacks import TitanIpMapHack


class ITestSite:
    def Connect(self, address: str, siteIndex: int):
        pass

    def Reset(self, resetType):
        pass

    def RebootFP(self):
        pass

    def GetSiteInfo(self) -> str:
        return ""

    def SpiSendReceive(self, id, sendData: bytes, receiveByteCount: int) -> bytes:
        return b""

    def SpiSetClockRate(self, id, clockRateRequested: float) -> float:
        return 0.0

    def SpiSetMode(self, id, mode):
        pass

    def GetComponents(self):
        return []

    def GetComponentAttributes(self, component):
        return []

    def GetAttribute(self, component, attribute) -> str:
        return ""

    def GetAttributes(self, component, attributes):
        return []

    def GetSiteStatus(self):
        return None

    def ThermalSetEnable(self, enable: bool):
        pass

    def ThermalSetType(self, thermaltype: str):
        pass

    def PowerSetEnable(self, id, enable: bool):
        pass

    def PowerSetVoltage(self, id, voltage: float):
        pass

    def UsbSetSuperSpeedEnable(self, id, enable: bool):
        pass

    def PowerSetVoltageLimit(self, id, voltage: float, period: float):
        pass

    def PowerSetCurrentLimit(self, id, current: float, period: float):
        pass

    def PowerSetVoltageTolerance(self, id, percent: float, period: float):
        pass

    def PowerSetVoltageBounds(self, id, minVoltage: float, maxVoltage: float):
        pass

    def LidSetPowerRestriction(self, id, restriction, limit: float):
        pass

    def UsbSetVbusEnable(self, id, enable: bool):
        pass

    def DutBufferEnable(self, enable: bool):
        pass

    def UartSetBaudRate(self, id, baudRate):
        pass

    def UartSend(self, id, data: bytes):
        pass

    def UartReceive(self, id, byteCount: int, timeout: float) -> bytes:
        return b""

    def JtagSetClockRate(self, id, clockRate: float):
        pass

    def JtagSetEnable(self, id, enable: bool):
        pass

    def JtagReset(self, id, type_, durationInMs: int):
        pass

    def JtagWriteReadIR(self, id, tdiData: bytes, bitCount: int) -> bytes:
        return b""

    def JtagWriteReadDR(self, id, tdiData: bytes, bitCount: int) -> bytes:
        return b""

    def GpioWrite(self, id, state):
        pass

    def GpioRead(self, id):
        return None

    def StartLogging(self, id) -> str:
        return ""

    def StopLogging(self, id):
        pass

    def SyncLogging(self, id):
        pass

    def I2cSend(self, busId, address: int, data: bytes):
        pass

    def I2cReceive(self,
                   busId,
                   address: int,
                   bytesToReceiveCount: int,
                   command: Optional[bytes] = None) -> bytes:
        return b""

class TestSiteFactory:
    @staticmethod
    def Create() -> ITestSite:
        return ITestSite()

import json
import sys
import os


from operator import truediv

import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestSiteCallerMode:
    CallerModeDotNet = 0
    CallerModeTsar = 1

class AlarmBits:
    NoFaults = 0

class StatusBits:
    SltbPresent = 1
    SiteReady = 2

class SltPlatform:
    TitanHP = 1
    All = 2
    Titan = 3
    Aries = 4
    Mercury = 5

class SubSltPlatform:
    TitanHP_1 = 1
    None_ = 2

class ResetType:
    SiteReset = 1

class SiteComponent:
    ControllerBoard = 1
    InstrumentAssembly = 2

class TestSiteCallerMode(Enum):
    CallerModeDotNet = 0
    CallerModeTsar = 1

class TestSiteTest(BaseTest):
    def __init__(self,IHC_IP, FpIP, SiteIP,SlotNo):
        self.CallerMode: TestSiteCallerMode = TestSiteCallerMode.CallerModeDotNet
        self.TestSites: List[int] = []
        self.TestSiteAddresses: List[str] = []
        self.UserName='cpc'
        self.Password ='Teradyne'
        self.IhcIP = IHC_IP
        #self.IhcIP: ipaddress.IPv4Address = ipaddress.IPv4Address(IHC_IP)
        self.SioAddress: ipaddress.IPv4Address = ipaddress.IPv4Address(SiteIP)
        self.FpAddress: List[ipaddress.IPv4Address] = [ipaddress.IPv4Address(FpIP)]
        self.ScanInstAddress: ipaddress.IPv4Address = ipaddress.IPv4Address('0.0.0.0')
        self.Interface: str = "Default"
        self.PlatformParam: str = ""
        self.SubPlatformParam: str = ""
        self.TftpPath: str = ""
        self.ThermalBoardPresent: bool = True
        self.PowerBoardPresent: bool = True
        self.BaseBoardPresent: bool = True
        self.FpBoardPresent: bool = True
        self.IOBoardPresent: bool = True
        self.FunctionalProcessorPresent: bool = True
        self.CoolantValvePresent: bool = True
        self.CarrierPresent: bool = True
        self.SltbFansPresent: bool = True
        self.DutPowerSupplyPresent: bool = True
        self.IonizerPresent: bool = True
        self.InterfaceBoardPresent: bool = True
        self.ScanEnabled: bool = False
        self.ThermalSetupPresent: bool = True
        # ssh Client
        self.SSH_Client = paramiko.SSHClient()
        self.SlotNo = SlotNo
        self.SiteIP = SiteIP
        self.SetUpSite()


    @property
    def FpSiteAddress(self) -> str:
        if 1 <= self.SiteIndex <= len(self.TestSiteAddresses):
            return self.TestSiteAddresses[self.SiteIndex - 1]
        if self.SltPlatform == "TitanHP" and self.SubSltPlatform == "TitanHP_1":
            return TitanIpMapHack.get_titan_hp_fp_ip(str(self.SioAddress), self.SiteIndex)
        else:
            return TitanIpMapHack.get_fp_ip(str(self.SioAddress), self.SiteIndex)

    @property
    def ScanInsSiteAddress(self) -> str:
        if 1 <= self.SiteIndex <= len(self.TestSiteAddresses):
            return self.TestSiteAddresses[self.SiteIndex - 1]
        return TitanIpMapHack.get_scan_ins_ip(str(self.SioAddress), self.SiteIndex)

    @property
    def SiteIndex(self) -> int:
        return 1 if not hasattr(self, 'Iteration') or not getattr(self.Iteration, 'Value', None) else getattr(self.Iteration, 'Value')

    @property
    def _tftpPath(self) -> str:
        return self.TftpPath if len(self.TftpPath) > 0 else TitanIpMapHack.get_tftp_path(str(self.SioAddress))

    def SetUpIteration(self):
        self.SetUpSite()

    @property
    def SiteIndex(self):
        return self.Iteration.Value if self.Iteration.Value else 1

    @property
    def _tftpPath(self):
        return self.TftpPath if self.TftpPath else None

    @property
    def EmbSwInfo(self):
        if not self._embSwInfo:
            self._embSwInfo = None
        return self._embSwInfo

    def ConnectSsh(self):
        logging.info(f"*** Connecting SSH to {self.IhcIP} ...  ***")
        try:
            self.SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.SSH_Client.connect(self.IhcIP, username=self.UserName, password=self.Password)
            logging.info(f"SSHClient connection was successful for FP {self.IhcIP}")
            return True
        except Exception as e:
            logging.error(f"SSHClient connection was not successful for FP {self.IhcIP}")
        return False


    def disconnectSsh(self):
        # tsar.SSH_Client.d
        # Disconnect the SSH client
        self.SSH_Client.close()
        print("SSH client disconnected")


    def executeTSAR_Command(self, apiName, fullCMD):

        logging.info(f"TSAR Command {fullCMD}")
        cmdHeader = f"cd ../../teradyne/TestSiteRunner && ./TestSiteRunner {self.SiteIP} {self.SlotNo} "
        fullCMD = cmdHeader + fullCMD
        stdin, stdout, stderr = self.SSH_Client.exec_command(fullCMD)
        reply = stdout.read().decode('utf-8').lower()
        if any(error in reply for error in
               ["arguments mismatch", "could not parse", "exception", "api error", "invalid command", "not found",
                "not implemented"]):
            logging.error(
                f"TSAR command {apiName} returned the reply with error: The method or operation is not implemented Reply = {reply}")

            return False,reply
        else:
            logging.info(f"Response for the API call {apiName} : {reply}")
            return True,reply

    def executeSsh_Command(self,fullCMD):

        logging.info(f"SSH Command {fullCMD}")
        stdin, stdout, stderr = self.SSH_Client.exec_command(fullCMD)
        reply = stdout.read().decode('utf-8').lower()
        if any(error in reply for error in
               ["arguments mismatch", "could not parse", "exception", "api error", "invalid command", "not found",
                "not implemented"]):
            logging.error(
                f"Ssh command {fullCMD} returned the reply with error: Reply = {reply}")

            return False,reply
        else:
            logging.info(f"Response for the cmd {fullCMD} : {reply}")
            return True,reply


    def execute_CMD(self, api_name, full_CMD):
        result, reply = self.executeTSAR_Command(api_name, full_CMD)
        with allure.step(f" {api_name} : {reply}"):
            assert result == True, f"TSAR command {api_name} failed"
        return reply


    def SetUpIteration(self):
        self.SetUpSite()

    # def SetUpSite(self):
    #     if not self.SioAddress:
    #         return
    #     self.ConnectSsh()

        # self.ConnectTestSite()
        # self.ConnectTestSiteInternal()
        # self.TestSite.Reset(self.ResetType.SiteReset)
        # if self.ScanEnabled:
        #     self.SetUpTestSiteInstrument()
        # self.SetPlatform()

    def SetUpFpSite(self):
        self.ConnectFp()
        self.ConnectTestSiteFpInternal()
        self.TestFp.Reset(self.ResetType.SiteReset)

    def SetUpTestSiteInstrument(self):
        self.ConnectScanInstrumentTestSite()
        self.ConnectScanInstrumentTestSiteInternal()
        self.TestScanInstrument.Reset(self.ResetType.SiteReset)

    def SetPlatform(self):
        pass

    def RunPlatformSetup(self):
        pass

    def TearDownIteration(self):
        self.TearDownSite()

    def TearDownSite(self):
        if not self.SioAddress:
            return
        self.Do("Dispose TestSite", lambda: self.TestSite.Dispose())
        self.Do("Dispose TestSiteInternal", lambda: self.TestSiteInternal.Dispose())
        self.Do("Dispose TestScanInsInternal", lambda: self.TestScanInsInternal.Dispose())
        self.TestSite = None
        self.TestSiteInternal = None
        self.TestScanInsInternal = None


    def SetUpSite(self):
        if str(self.SioAddress) == '0.0.0.0':
            return
        self.ConnectSsh()


        #self.ConnectTestSiteInternal()
        # Assuming TestSite is an object with a Reset method
        # TestSite.Reset(ResetType.SiteReset)
        if self.ScanEnabled:
            self.SetUpTestSiteInstrument()
        # Assuming SetPlatform is a method to be defined later
        # SetPlatform()

    # ----------------------------------------------------
    #       Uart APIs
    # ----------------------------------------------------
    #       uart_set_enable API
    def uart_set_enable(self, uart_id, state, expected_exception=None):
        if expected_exception:
            raise expected_exception

        # Simulating enabling/disabling UART hardware
        api_name = "UartSetEnable"
        full_CMD = f"UartSetEnable {uart_id} {state}"
        self.execute_CMD(api_name, full_CMD)

    # ----------------------------------------------------
    #        API
    # ----------------------------------------------------

    def SetUpFpSite(self):
        # Assuming ConnectFp and ConnectTestSiteFpInternal are methods to be defined later
        # ConnectFp()
        # ConnectTestSiteFpInternal()
        # Assuming TestFp is an object with a Reset method
        # TestFp.Reset(ResetType.SiteReset)
        pass

    def SetUpTestSiteInstrument(self):
        # Assuming ConnectScanInstrumentTestSite and ConnectScanInstrumentTestSiteInternal are methods to be defined later
        # ConnectScanInstrumentTestSite()
        # ConnectScanInstrumentTestSiteInternal()
        # Assuming TestScanInstrument is an object with a Reset method
        # TestScanInstrument.Reset(ResetType.SiteReset)
        pass



#===============================================================

if __name__ == "__main__":
    # Log the message
    test_site_test = TestSiteTest(IHC_IP="131.101.47.35",
                        FpIP="192.168.122.1",
                        SiteIP="192.168.122.1",
                        SlotNo=1)
    # Example usage of the class:
    # Log the message
    test_site_test.executeTSAR_Command("GetStieInfo","GetStieInfo")
    test_site_test.disconnectSsh()
    print("Setup iteration completed.")

