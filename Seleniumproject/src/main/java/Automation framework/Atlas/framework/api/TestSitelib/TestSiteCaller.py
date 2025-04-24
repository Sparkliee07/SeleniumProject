import os
import time
from datetime import timedelta
from unittest.mock import MagicMock
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
import ipaddress
from enum import Enum
from typing import List, Optional
from ATLAS.framework.api.TestSiteLib.TestSiteLibrarry import (TER_Status,
        SiteComponent,SiteComponentAttribute)


# -----------------------------
#       Test Site caller
# -----------------------------

class TestSiteCallerMode(Enum):
    CallerModeDotNet = 0
    CallerModeTsar = 1


class TestSiteCaller:

    def __init__(self, test, sio_address=None, site_index=None, interface_id_str="Default"):
        self.TestSite = None
        self.SioAddress = sio_address
        self.SiteIndex = site_index
        self.LogSiteIndex = True
        self._test = test
        self._disposed = False
        self.CreateTestSite()
        self.ConnectTestSite()

        if sio_address is not None and site_index is not None:
            if not self.__class__.__name__ == "TestSiteCallerTsar":
                type_name = self.__class__.__name__.replace("Caller", "")
                test.Do(f"Create {type_name}", lambda: self.CreateTestSite(), suppressPass=True)
                test.Do(f"Connect {type_name}", lambda: self.TestSite.Connect(str(sio_address), site_index))

    def __init__(self, test, site_index, ip_addr, port, interface_id_str="Default"):
        self.TestSite = None
        self.SioAddress = None
        self.SiteIndex = site_index
        self.LogSiteIndex = True
        self._test = test
        self._disposed = False

        type_name = self.__class__.__name__.replace("Caller", "")
        test.Do(f"Create {type_name}", lambda: self.CreateTestSite(), suppressPass=True)
        test.Do(f"Connect {type_name}", lambda: self.TestSite.Connect(str(ip_addr), site_index, port))
        test.LogMessage(
            f"TestSiteCaller, Create test site and connect with {str(ip_addr)} at site {site_index} port {port}")

    def GetFpAddressFromSiteIndex(self, SiteIndex, TestSites, fpAddress):
        CurrentSiteFpAddress = ipaddress.IPv4Address('0.0.0.0')
        index = TestSites.index(SiteIndex) if SiteIndex in TestSites else -1
        if 0 <= index < len(fpAddress) and fpAddress[index] != ipaddress.IPv4Address('0.0.0.0'):
            CurrentSiteFpAddress = fpAddress[index]
        return CurrentSiteFpAddress

        def CreateTestSite(self):
            self.TestSite = TestSite()

        def Reset(self, reset_type, ex=None):
            self.Call(f"Reset({reset_type})", lambda: self.TestSite.Reset(reset_type), ex)

        def RebootFP(self, ex=None):
            self.Call("RebootFP", lambda: self.TestSite.RebootFP(), ex)

        def ConnectTestSite(self):
            pass  # To be overridden

        def Call(self, message, action, ex=None):
            if self.LogSiteIndex:
                message = f"S{self.SiteIndex} {message}"
            try:
                action()
                if ex:
                    raise ex
            except Exception as e:
                self._test.LogResult(TestStatus.FAIL, f"Exception in {message}: {str(e)}")

        def GetSiteInfo(self, ex=None):
            result = None
            # self.Call("GetSiteInfo", lambda: result := self.TestSite.GetSiteInfo(), ex)
            self.call("GetSiteInfo", lambda: setattr(self, 'result', self.TestSite.GetSiteInfo(), ex))
            return self.result
            # return result

        def UartSend(self, id, data, ex=None, suppress_pass=False):
            length = 0 if data is None else len(data)
            self.call(f"uart_send - id = {id}, dataLength = {length}",
                      lambda: self.TestSite.uart_send(id, data),
                      ex,
                      suppress_pass)

        def uart_receive(self, id, byte_count, timeout, ex=None, suppress_pass=False):
            type_str = str(id)
            retval = bytearray()
            self.call(f"uart_receive - id = {id}, byteCount = {byte_count}, timeout = {timeout}",
                      lambda: setattr(self, 'retval', test_site_internal.uart_receive(id, byte_count, timeout)),
                      ex,
                      suppress_pass)
            return retval

        def uart_set_baud_rate(id, baud_rate, ex=None):
            call(f"uart_set_baud_rate - id = {id}, baudRate = {baud_rate}",
                 lambda: test_site_internal.uart_set_baud_rate(id, baud_rate),
                 ex)

        def uart_set_enable(id, enable, ex=None):
            call(f"uart_set_enable - id = {id}, bEnable = {enable}",
                 lambda: test_site_internal.uart_set_enable(id, enable),
                 ex)

        def SpiSendReceive(self, id, send_data, receive_byte_count, ex=None):
            return_value = None
            self.Call(f"SpiSendReceive({id}, {receive_byte_count}, {send_data})",
                      lambda: setattr(return_value := self.TestSite.SpiSendReceive(id, send_data, receive_byte_count)),
                      ex)
            return return_value

        def Dispose(self, disposing=True):
            if not self._disposed:
                self._disposed = True

        def __del__(self):
            self.Dispose()

    # ===========================================

    def CreateTestSite(self):
        self.TestSite = TestSiteFactory.Create()

    def Reset(self, resetType, ex=None):
        type_str = str(resetType)
        self.Call(f"Reset({resetType})", lambda: self.TestSite.Reset(resetType), ex)

    def RebootFP(self, ex=None):
        self.Call("RebootFP", lambda: self.TestSite.RebootFP(), ex)

    def GetSiteInfo(self, ex=None):
        result = None
        #self.Call("GetSiteInfo", lambda: result := self.TestSite.GetSiteInfo(), ex)
        return result

    def SpiSendReceive(self, id, sendData, receiveByteCount, ex=None):
        spiBusIdName = str(id)
        returnValue = None
        self.Call(f"SpiSendReceive({id}, {receiveByteCount}, {', '.join(map(str, sendData))})",
                  lambda: returnValue := self.TestSite.SpiSendReceive(id, sendData, receiveByteCount), ex)
        return returnValue

    def SpiSetClockRate(self, id, clockRateRequested, ex=None):
        returnValue = 0
        self.Call(f"SpiSetClockRate({id}, {clockRateRequested})",
                  lambda: returnValue := self.TestSite.SpiSetClockRate(id, clockRateRequested), ex)
        return returnValue

    def SpiSetMode(self, id, mode, ex=None):
        self.Call(f"SpiSetMode({id}, {mode})", lambda: self.TestSite.SpiSetMode(id, mode), ex)

    def GetComponents(self, ex=None):
        result = None
        self.Call("GetComponents", lambda: result := self.TestSite.GetComponents(), ex)
        return result

    def GetComponentAttributes(self, component, ex=None):
        result = None
        self.Call(f"GetComponentAttributes({component})",
                  lambda: result := self.TestSite.GetComponentAttributes(component), ex)
        return result

    def GetAttribute(self, component, attribute, ex=None, suppressPass=False):
        result = None
        self.Call(f"GetAttribute({component}, {attribute})",
                  lambda: result := self.TestSite.GetAttribute(component, attribute), ex, suppressPass)
        return result

    def GetAttributes(self, component, attributes, ex=None):
        result = None
        self.Call("GetAttributes", lambda: result := self.TestSite.GetAttributes(component, attributes), ex)
        return result

    def GetSiteStatus(self, ex=None):
        returnValue = SiteStatus()
        self.Call("GetSiteStatus", lambda: returnValue := self.TestSite.GetSiteStatus(), ex)
        return returnValue

    def CarrierWaitForReady(self, state=True):
        sw = Stopwatch()
        ts = TimeSpan(0, 0, 10)

        sw.Start()

        while sw.Elapsed < ts:
            status = self.TestSite.GetSiteStatus()
            siteReady = (status.statusBits & StatusBits.SiteReady) != 0
            sltbPresent = (status.statusBits & StatusBits.SltbPresent) != 0

            if sltbPresent and siteReady == state:
                return True

            time.sleep(0.25)

        _test.LogResult(TestStatus.FAIL,
                        f"Site statusBits: 0X{status.statusBits:X}, alarmBits:0X{status.alarmBits:X}, testerAlarmBits:0X{status.testerAlarmBits:X}")

        return False

    def ThermalSetEnable(self, enable, ex=None):
        self.Call(f"ThermalSetEnable({enable})", lambda: self.TestSite.ThermalSetEnable(enable), ex)

    def ThermalSetTarget(self, tempTarget, ex=None):
        raise Exception()

    def ThermalSetRampRate(self, coolRampRate, heatRampRate, ex=None):
        raise Exception()

    def ThermalSetType(self, thermaltype, ex=None):
        type_str = str(thermaltype)
        self.Call(f"ThermalSetType({thermaltype})", lambda: self.TestSite.ThermalSetType(type_str), ex)

    def PowerSetEnable(self, id, enable, ex=None):
        railIdStr = f"RailId.{id}"
        self.Call(f"PowerSetEnable({railIdStr}, {enable})", lambda: self.TestSite.PowerSetEnable(id, enable), ex)

    def PowerSetVoltage(self, id, voltage, ex=None):
        railIdStr = f"RailId.{id}"
        self.Call(f"PowerSetVoltage({railIdStr}, {voltage})", lambda: self.TestSite.PowerSetVoltage(id, voltage), ex)

    def UsbSetSuperSpeedEnable(self, id, enable, ex=None):
        Call($"{System.Reflection.MethodBase.GetCurrentMethod().Name} - enable ={enable}",
        () = > TestSite.UsbSetSuperSpeedEnable(id, enable),
        ex);

        def PowerSetVoltageLimit(self, id, voltage,





