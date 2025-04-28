
from collections import defaultdict

from ATLAS.framework.api.TestSiteLib.TestSiteRunner import TSAR
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.TestSiteLibrarry import SiteComponent,SiteComponentAttribute
import logging
import re
from typing import Dict, List



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



ThermalBoardPresent = True
PowerBoardPresent = True
FunctionalProcessorPresent = True
IOBoardPresent = True
CoolantValvePresent = False
CarrierPresent = False

# Define attributes for site components
controller_board_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

backplane_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

thermal_board_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

power_board_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

io_board_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

baseboard_attributes = [
    SiteComponentAttribute.PartNumber,
    SiteComponentAttribute.SerialNumber,
    SiteComponentAttribute.Revision
]

# Map site components to their attributes
site_component_attributes = {SiteComponent.ControllerBoard: controller_board_attributes,
                             SiteComponent.Backplane: backplane_attributes,
                             SiteComponent.in
                             }

# Mock siteComponentAttributes dictionary
# siteComponentAttributes = defaultdict(list)
# site_component_attributes: Dict[str, List[str]] = {
#     "controllerboard": ["partnumber", "serialnumber"],
#     "interfaceboard": ["partnumber" , "serialnumber" ,"revision", "revisiondate"],
#     "ThermalBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"],
#     "PowerBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"]
# }


class TestGetMfgInfo:
    def __init__(self):
        self.site_component_attributes_table: Dict[int, Dict[str, List[str]]] = {}
        self.site_component_fp_attributes_table: Dict[int, Dict[str, List[str]]] = {}
        self.site_index = 0

    @property
    def site_component_attributes(self) -> Dict[str, List[str]]:
        return self.site_component_attributes_table.setdefault(self.site_index, {})

    @property
    def site_component_fp_attributes(self) -> Dict[str, List[str]]:
        return self.site_component_fp_attributes_table.setdefault(self.site_index, {})

    def setup_site(self):
        print("Setting up site")

    def teardown_site(self):
        print("Tearing down site")

    def platform_setup_halos(self):
        self.site_component_attributes[SiteComponent.ControllerBoard] = [SiteComponentAttribute.PartNumber,
            SiteComponentAttribute.SerialNumber,
            SiteComponentAttribute.Revision,
        ]
        print("Platform Halos Setup Done")

    def platform_setup_fp(self):
        self.site_component_fp_attributes[SiteComponent.FunctionalProcessor] = [
            SiteComponentAttribute.PartNumber,
        ]
        print("Platform FP Setup Done")

    def get_mfg_info_test(self):
        mfg_info = "ControllerBoard: PartNumber=123-456-78, SerialNumber=A1B2C3D4, Revision=R1;"  # Example string
        actual_components = [comp.strip() for comp in mfg_info.split(';') if comp]

        for component, attributes in self.site_component_attributes.items():
            found = False
            print(f"component {component}  attributes {attributes} ")
            for entry in actual_components:
                comp_name, comp_attrs = entry.split(":")
                if comp_name.strip() == component:
                    found = True
                    print(f"{component} found")
                    attr_dict = dict(attr.split("=") for attr in comp_attrs.split(","))
                    for attr in attributes:
                        if attr in attr_dict:
                            print(f"{component} {attr}: {attr_dict[attr]}")
                        else:
                            print(f"{component} {attr} missing")
            if not found:
                print(f"{component} not found")


if __name__ == "__main__":
    test = TestGetMfgInfo()
    test.platform_setup_halos()
    test.get_mfg_info_test()
