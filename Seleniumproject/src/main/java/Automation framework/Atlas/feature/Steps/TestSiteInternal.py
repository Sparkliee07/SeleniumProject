import re
from typing import Dict, List, Tuple
import json
from operator import truediv

import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os
import time
import sys
from datetime import datetime




# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create a handler that writes log messages to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(console_handler)
#TSAR_FileName = "TestData/TSAR_1.json"
TSAR_FileName = "TSAR_Config.json"
#TSAR_FileName = "TSAR_Config_thp01.json"
#TSAR_FileName = "TSAR_Config_thp05.json"

# get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print("Current date & time : ", current_datetime)
# convert datetime obj to string
str_current_datetime = str(current_datetime)
# Append-adds at last
logFileName = 'TSAR_Results.csv'
file1 = open(logFileName, "w")  # append mode
Header = "Input Cmd , Result \n"
#print(Header)
file1.write(Header)
file1.close()

def log_to_file(message):
    """Logs a message to a file named 'ShhTest.log'."""
    file1 = open(logFileName, "a")  # append mode
    file1.write(message)
    file1.close()



# -----------------------------
#       TSAR class
# -----------------------------
class TSAR:
    def __init__(self):
        # logger.info(tsar_definitions)
        self.TSAR_FileName = "TSAR_Config.json"
        self.FpIP = None
        self.IhcIP = "131.101.47.35"
        self.UserName = "cpc"
        self.Password = "Teradyne"
        self.SiteIP = "192.168.122.1"
        self.SlotNo = 1
        self.APIS = None
        #self.GetTSAR_JsonDataConnectSsh()
        self.SSH_Client = paramiko.SSHClient()

    #@staticmethod
    def GetTSAR_JsonDataConnectSsh(self):
        logging.info("*** TSAR.json Commands ***")
        if os.path.exists(self.TSAR_FileName):
            logging.info(f"TSAR Json File found in the given path {TSAR_FileName}")
            with open(TSAR_FileName, "r") as f:
                tsar_definitions = json.load(f)

            if tsar_definitions:
                self.FpIP = tsar_definitions['FpIP']
                self.IhcIP =  tsar_definitions['IHC_IP']
                self.UserName = tsar_definitions['UserName']
                self.Password = tsar_definitions['Password']
                self.SiteIP = tsar_definitions['SiteIP']
                self.SlotNo = tsar_definitions['SlotNo']
                self.APIS = tsar_definitions['APIS']
        else:
            logging.error(f"TSAR Json File does not exist in the given path{TSAR_FileName}")

        return


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


    def executeSsh_Command(self, apiName, fullCMD):
        nResult = True
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
            nResult = False
            return nResult,reply
        else:
            logging.info(f"Response for the API call {apiName} : {reply}")
            return nResult,reply

    def Process_Tsar_API_List(self):
            nResult = 0
            remarks = ""

            logging.info("*** Executing TSAR Commands ***")
            try:
                for api in self.APIS:
                    time.sleep(1)
                    logger.info(f"Executing CMD {api['Name']}")
                    cmdPath = f"{api['Name']} {' '.join(api['Parameters'])}"
                    nResult = self.executeSsh_Command(api['Name'], cmdPath)

            except Exception as e:
                logger.error(f" Exception while executing TSAR Command ")

            remarks = "" if nResult >= 0 else "Fail in TSAR execution"
            return nResult, remarks




class TestSiteInternal:


    @staticmethod
    def get_mfg_info() -> str:
        # Mock implementation of the actual method
        tsar = TSAR()
        tsar.ConnectSsh()
        result,reply = tsar.executeSsh_Command("GetMfgInfo", f"GetMfgInfo")
        #dummy = "ThermalBoard:PartNumber=123-456-78,SerialNumber=ABCDEF12,Revision=A,RevisionDate=2021A;PowerBoard:PartNumber=234-567-89,SerialNumber=XYZ98765,Revision=1A,RevisionDate=2020B"
        if result :
            return reply
        tsar.disconnectSsh()
        return dummy

def log_message(message: str):
    print(message)

class TestStatus:
    Pass = "Pass"
    Fail = "Fail"

class CompareOptions:
    def __init__(self):
        self.custom_options = {}

def compare(message: str, pattern: str, actual: str, compare_type: str, options: CompareOptions = None) -> str:
    if compare_type == "CompareRegex":
        return TestStatus.Pass if re.match(pattern, actual) else TestStatus.Fail
    elif compare_type == "CompareNot":
        return TestStatus.Pass if pattern != actual else TestStatus.Fail
    elif compare_type == "CompareMax":
        return TestStatus.Pass if int(pattern) >= actual else TestStatus.Fail
    return TestStatus.Fail



site_component_attributes: Dict[str, List[str]] = {
    "controllerboard": ["partnumber", "serialnumber"],
    "interfaceboard": ["partnumber" , "serialnumber" ,"revision", "revisiondate"],
    "ThermalBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"],
    "PowerBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"]
}

thermal_board_present = True
power_board_present = True
functional_processor_present = True
io_board_present = True
coolant_valve_present = True
carrier_present = True
custom_options = CompareOptions()

def get_mfg_info_test():
    mfg_info = TestSiteInternal.get_mfg_info()
    subs = mfg_info.split(';')
    for sub in subs:
        log_message(sub)

    actual_components = [comp.strip() for comp in mfg_info.strip().split(';') if comp.strip()]

    log_message(actual_components)



    for expected_component, expected_attributes in site_component_attributes.items():
        expect_found = True
        if expected_component == "ThermalBoard":
            expect_found = thermal_board_present
        elif expected_component == "PowerBoard":
            expect_found = power_board_present
        elif expected_component == "FunctionalProcessor":
            expect_found = functional_processor_present
        elif expected_component == "IOBoard":
            expect_found = io_board_present
        elif expected_component == "CoolantValve":
            expect_found = coolant_valve_present
        elif expected_component in ["CarrierAssembly", "CarrierBoard"]:
            expect_found = carrier_present

        actual_attributes = ""
        for component in actual_components:
            component_name, component_attributes = component.split(':')
            if component_name.strip().lower() == expected_component.lower():
                actual_attributes = component_attributes.strip()
                break

        if compare(f"{expected_component} found", "true", "false" if not actual_attributes else "true", "CompareNot") == TestStatus.Pass:
            attributes = {pair[0].strip(): pair[1].strip() for pair in [attr.split('=') for attr in actual_attributes.split(',')]}

            for expected_attribute in expected_attributes:
                message = f"{expected_component} {expected_attribute}"
                actual_attribute = attributes.get(expected_attribute, "")
                if expected_attribute == "PartNumber":
                    assert compare(message, r"^\d\d\d-\d\d\d-\d\d$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                    assert compare(message, "ffffffffff", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass
                elif expected_attribute == "SerialNumber":
                    assert compare(message, r"^[a-zA-Z0-9]{8,}$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                    assert compare(message, "ffffffff", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass
                elif expected_attribute == "Revision":
                    if len(actual_attribute) == 1:
                        assert compare(message, r"^[a-zA-Z]{1}$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                        assert compare(message, "f", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass
                    elif len(actual_attribute) == 2:
                        assert compare(message, r"^[a-zA-Z]{1}[0-9]{1}$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                        assert compare(message, "ff", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass
                    else:
                        assert compare(message + " length", "2", len(actual_attribute), "CompareMax", options=custom_options) == TestStatus.Pass
                elif expected_attribute == "RevisionDate":
                    assert compare(message, r"^\d\d\d\d[a-zA-Z]{1}$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                    assert compare(message, "fffff", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass
                elif expected_attribute == "MacAddress":
                    assert compare(message, r"^([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2})$", actual_attribute, "CompareRegex", options=custom_options) == TestStatus.Pass
                    assert compare(message, "fffffffffffffffff", actual_attribute, "CompareNot", options=custom_options) == TestStatus.Pass

if __name__ == "__main__":
    get_mfg_info_test()
