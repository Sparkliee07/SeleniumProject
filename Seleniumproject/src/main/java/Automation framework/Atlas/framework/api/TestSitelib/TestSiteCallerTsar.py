import json
from operator import truediv
import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os
import time
import sys
from datetime import datetime
from ATLAS.framework.api.TestSiteLib.TestSiteCaller import TestSiteCaller
import socket
from typing import List, Optional

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create a handler that writes log messages to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
#TSAR_FileName = "./TSAR.json"
TSAR_FileName = "../TestSiteCaller/TSAR_DeadPool.json"

import subprocess
import os
import enum
from typing import List, Tuple, Type

class TestStatus(enum.Enum):
    FAIL = 0

class Test:
    TsarFilePathLinux = "/path/to/tsar/linux"
    TsarFilePathWindows = "C:\\path\\to\\tsar\\windows"

    @staticmethod
    def LogResult(status, message):
        print(f"{status.name}: {message}")


class TestSiteCallerTsar(TestSiteCaller):
    def __init__(self, test, sio_address, site_index, interface_id_str="Default"):
        super().__init__(test, sio_address, site_index, interface_id_str)

    def CreateTestSite(self):
        # Don't need to create the Test Site Interface with TSAR
        pass

    def CallMethodTsar(self, command_name, input_tuple_args: List[Tuple[object, Type]], output_types: List[Type], exp_exc=None):
        tsar_command = self.CreateTsarCommandHeader(command_name)
        tsar_command += self.ParseTupleListToTsarCommandString(input_tuple_args)
        tsar_output = self.ExecuteTsarCommand(tsar_command)

        if self.CheckForTsarException(tsar_output, exp_exc):
            raise Exception("TSAR Raised " + tsar_output)

        tsar_output_string_array = self.SplitTsarOutputString(tsar_output.strip(), ' ')
        try:
            tsar_output_object_array = self.ParseTsarOutputStringArrayToObjectArray(tsar_output_string_array, output_types)
        except Exception as ex:
            self._test.LogResult(TestStatus.FAIL, f"Exception while parsing TSAR output: {str(ex)}")
            raise Exception(f"Exception while parsing TSAR output: {str(ex)}")

        return tsar_output_object_array

    def CreateTsarCommandHeader(self, command_name):
        return f"{self.SioAddress} {self.SiteIndex} {command_name} "

    def ParseTupleListToTsarCommandString(self, input_tuple_args: List[Tuple[object, Type]]):
        output = ""

        for i, input_tuple in enumerate(input_tuple_args):
            if input_tuple[0] is None:
                return None

            if input_tuple[1] == str:
                output += f"\"{input_tuple[0]}\""
            elif isinstance(input_tuple[0], list):
                output += f"[{self.ParseArrayObjectToString(input_tuple[0])}]"
            elif isinstance(input_tuple[0], tuple):
                output += f"[{self.ParseStructObjectToString(input_tuple[0])}]"
            else:
                output += self.ParseObjectToString(input_tuple[0])

            if i < len(input_tuple_args) - 1:
                output += ' '

        return output

    def ParseArrayObjectToString(self, array_to_parse):
        output = ""
        for i, item in enumerate(array_to_parse):
            if isinstance(item, list):
                output += f"[{self.ParseArrayObjectToString(item)}]"
            elif isinstance(item, tuple):
                output += f"[{self.ParseStructObjectToString(item)}]"
            else:
                output += self.ParseObjectToString(item)
            if i < len(array_to_parse) - 1:
                output += ' '
        return output

    def ParseStructObjectToString(self, struct_object):
        output = ""
        for i, field in enumerate(struct_object):
            if isinstance(field, list):
                output += f"[{self.ParseArrayObjectToString(field)}]"
            elif isinstance(field, tuple):
                output += f"[{self.ParseStructObjectToString(field)}]"
            else:
                output += self.ParseObjectToString(field)
            if i < len(struct_object) - 1:
                output += ' '
        return output

    def ParseObjectToString(self, print_object):
        if isinstance(print_object, str):
            return f"\"{print_object}\""
        return str(print_object)

    def ExecuteTsarCommand(self, command_string):
        if os.name == 'posix':
            file_name = self._test.TsarFilePathLinux
        else:
            file_name = self._test.TsarFilePathWindows

        result = subprocess.run([file_name, command_string], capture_output=True, text=True)
        return result.stdout

    def CheckForTsarException(self, tsar_output, expected_exception=None):
        if tsar_output.startswith("Exception: "):
            if expected_exception:
                return self.CheckTsarExceptionMatches(tsar_output, expected_exception)

            self._test.LogResult(TestStatus.FAIL, "TSAR call returned an exception when none expected")
            return True
        return False

    def CheckTsarExceptionMatches(self, tsar_output, expected_exception):
        split_tsar_output = tsar_output.split('\n')

        if len(split_tsar_output) != 3:
            self._test.LogResult(TestStatus.FAIL, "TSAR Output Exception incorrect format")
            return False

        status = self._test.Compare("Exception message", expected_exception.message,
                                    split_tsar_output[1][9:].rstrip('\r'), options={"SuppressPass": True})
        return status == TestStatus.Pass

    def SplitTsarOutputString(self, tsar_output_string, split_char):
        return tsar_output_string.split(split_char)

    def ParseTsarOutputStringArrayToObjectArray(self, output_strings, output_types):
        output_objects = []
        for output_string, output_type in zip(output_strings, output_types):
            output_objects.append(self.ParseGeneralObjectFromString(output_type, output_string))
        return output_objects

    def ParseGeneralObjectFromString(self, arg_type, arg_value):
        ret_object = None
        if self.IsTypeArrayOrStruct(arg_type):
            sub_arguments = self.SplitTsarOutputString(arg_value, ' ')

            if isinstance(arg_type, list):
                array_type = arg_type[0]
                ret_array = []

                for sub_arg in sub_arguments:
                    if array_type == str:
                        sub_arg = sub_arg.strip().strip('\"')
                    ret_array.append(self.ParseGeneralObjectFromString(array_type, sub_arg))

                return ret_array
            else:
                ret_object = arg_type()
                for field, sub_arg in zip(arg_type.__annotations__.items(), sub_arguments):
                    field_name, field_type = field
                    if field_type == str:
                        sub_arg = sub_arg.strip().strip('\"')
                    setattr(ret_object, field_name, self.ParseGeneralObjectFromString(field_type, sub_arg))
                return ret_object

        if issubclass(arg_type, enum.Enum):
            try:
                ret_object = arg_type[arg_value]
                return ret_object
            except KeyError:
                raise ValueError(f"Could not parse Enum of type {arg_type} from string {arg_value}")

        ret_object = self.ParseObjectFromString(arg_type, arg_value.strip())
        return ret_object

    def IsTypeArrayOrStruct(self, arg_type):
        return isinstance(arg_type, list) or (isinstance(arg_type, type) and hasattr(arg_type, '__annotations__'))

    def ParseObjectFromString(self, arg_type, arg_value):
        if arg_type == str:
            return arg_value
        elif self.IsHexParsableType(arg_type) and arg_value.startswith("0x"):
            return int(arg_value, 16)
        else:
            try:
                return arg_type(arg_value)
            except ValueError:
                raise ValueError(f"Could not parse string {arg_value}, to type {arg_type}")

    def IsHexParsableType(self, arg_type):
        return arg_type in [int, bytes]


    def reset(self, reset_type, ex=None):
        input_args = [(reset_type, type(reset_type))]

        try:
            ret_objs = self.call_method_tsar(self.reset.__name__, input_args, [], ex)
        except Exception as exc:
            self._test.log_message(f"{exc}")

    def GetSiteInfo(self, ex=None):
        try:
            ret_objs = self.call_method_tsar(self.get_site_info.__name__, [], [str], ex)
            return ret_objs[0]
        except Exception as exc:
            self._test.log_message(f"{exc}")
            return None

    def spi_send_receive(self, id, send_data, receive_byte_count, ex=None):
        pass

    def get_components(self, ex=None):
        pass

    def get_component_attributes(self, component, ex=None):
        pass

    def get_attribute(self, component, attribute, ex=None, suppress_pass=False):
        pass

    def get_attributes(self, component, attributes, ex=None):
        pass

    def get_site_status(self, ex=None):
        pass

    def carrier_wait_for_ready(self, state=True):
        return False

    def thermal_set_enable(self, enable, ex=None):
        pass

    def thermal_set_target(self, temp_target, ex=None):
        pass

    def thermal_set_ramp_rate(self, cool_ramp_rate, heat_ramp_rate, ex=None):
        pass

    def thermal_set_type(self, thermal_type, ex=None):
        pass

    def power_set_enable(self, id, enable, ex=None):
        pass

    def power_set_voltage(self, id, voltage, ex=None):
        pass

    def usb_set_super_speed_enable(self, id, enable, ex=None):
        pass

    def power_set_voltage_limit(self, id, voltage, period, ex=None):
        pass

    def power_set_current_limit(self, id, current, period, ex=None):
        pass

    def power_set_voltage_tolerance(self, id, percent, period, ex=None):
        pass

    def power_set_voltage_bounds(self, id, min_voltage, max_voltage, ex=None):
        pass

    def usb_set_vbus_enable(self, id, enable, ex=None):
        pass

    def dut_buffer_enable(self, enable, ex=None):
        pass

    def uart_set_baud_rate(self, id, baud_rate, ex=None):
        input_args = [(id, type(id)), (baud_rate, type(baud_rate))]

        try:
            ret_objs = self.call_method_tsar(self.uart_set_baud_rate.__name__, input_args, [], ex)
        except Exception as exc:
            self._test.log_message(f"{exc}")

    def uart_send(self, id, data, ex=None, suppress_pass=False):
        input_args = [(id, type(id)), (data, type(data))]

        try:
            ret_objs = self.call_method_tsar(self.uart_send.__name__, input_args, [], ex)
        except Exception as exc:
            self._test.log_message(f"{exc}")

    def uart_receive(self, id, byte_count, timeout, ex=None, suppress_pass=False):
        input_args = [(id, type(id)), (byte_count, int), (timeout, float)]

        try:
            ret_objs = self.call_method_tsar(self.uart_receive.__name__, input_args, [bytes], ex)
            return ret_objs[0]
        except Exception as exc:
            self._test.log_message(f"{exc}")
            return None

    def jtag_set_clock_rate(self, id, clock_rate, ex=None):
        pass

    def jtag_set_enable(self, id, enable, ex=None):
        pass

    def jtag_reset(self, id, type, duration_in_ms, ex=None):
        pass

    def jtag_write_read_ir(self, id, tdi_data, bit_count, ex=None):
        pass

    def jtag_write_read_dr(self, id, tdi_data, bit_count, ex=None):
        pass

    def gpio_set_state(self, id, state, ex=None):
        pass

    def gpio_get_state(self, id, ex=None):
        pass

    def start_logging(self, id, ex=None):
        pass

    def stop_logging(self, id, ex=None):
        pass

    def sync_logging(self, id, ex=None):
        pass

    def i2c_send(self, bus_id, address, data, ex=None):
        pass

    def i2c_receive(self, bus_id, address, bytes_to_receive_count, command, ex=None):
        pass

    def ionizer_enable(self, id, enable, ex=None):
        pass

    def call_method_tsar(self, method_name, input_args, output_types, ex):
        # Placeholder for method invocation logic
        pass

#===============================================================

if __name__ == "__main__":
    # Log the message

