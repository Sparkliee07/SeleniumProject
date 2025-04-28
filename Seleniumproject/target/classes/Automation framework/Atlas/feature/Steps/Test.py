
import allure
import re
from typing import Dict, List, Tuple
from tms.framework.api.TestFramework.TestStatus import TestStatus

MfgInfo_resp =("controllerboard: partnumber=eb202-cp, serialnumber=515-23091301400015; "
               "interfaceboard: partnumber=000-000-00, serialnumber=ffffffff, revision=??, revisiondate=ffff?;"
               "powerboard: partnumber=000-000-00, serialnumber=ffffffff, revision=??, revisiondate=ffff?;"
               "thermalboard: partnumber=000-000-00, serialnumber=ffffffff, revision=??, revisiondate=ffff?;")

Components = [component.strip() for component in MfgInfo_resp.strip().split(';') if component.strip()]
trimmed_Mfg_Info = MfgInfo_resp.rstrip("\n")
# Initialize an empty dictionary
boards_dict = {}
with allure.step(f"processing mfg Info response :  {trimmed_Mfg_Info}"):
    # Process each board section
    for section in trimmed_Mfg_Info.strip().split(';'):
        with allure.step(f"Component :  {section}"):
            section = section.strip()
            if not section:
                continue
            key, values = section.split(": ", 1)  # Split at the first colon
            attributes = dict(item.split("=") for item in values.split(", "))  # Convert attributes to dict
            boards_dict[key.strip()] = attributes  # Assign to dictionary

with allure.step(f"boards Dict :  {boards_dict}"):
    # Print the structured dictionary
    print(boards_dict)