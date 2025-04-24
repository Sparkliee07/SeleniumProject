import allure
import re
from typing import Dict, List, Tuple
from tms.framework.api.TestFramework.TestStatus import TestStatus

site_component_attributes: Dict[str, List[str]] = {
    "controllerboard": ["partnumber", "serialnumber"],
    "interfaceboard": ["partnumber" , "serialnumber" ,"revision", "revisiondate"],
    "ThermalBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"],
    "PowerBoard": ["PartNumber", "SerialNumber", "Revision", "RevisionDate", "MacAddress"]
}

class CompareOptions:
    def __init__(self):
        self.custom_options = {}

custom_options = CompareOptions()


def compare(message: str, pattern: str, actual: str, compare_type: str, options: CompareOptions = None) -> str:
    if compare_type == "CompareRegex":
        return TestStatus.Pass if re.match(pattern, actual) else TestStatus.FAIL
    elif compare_type == "CompareNot":
        return TestStatus.Pass if pattern != actual else TestStatus.FAIL
    elif compare_type == "CompareMax":
        return TestStatus.Pass if int(pattern) >= actual else TestStatus.FAIL
    return TestStatus.FAIL

def log_message(message: str):
    print(message)





@given(u'I have a properly set up TestSiteInternal')
def step_impl(context):
    result = context.tsar.ConnectSsh()
    assert result, "Failed to Connect SIO "
    pass

@when(u'I call the GetMfgInfo method')
def step_impl(context):
     result, reply = context.tsar.executeSsh_Command("GetMfgInfo", f"GetMfgInfo")
     assert result, "Failed to Get Mfg Info "
     if result:
         trimmed_Mfg_Info = reply.rstrip("\n")
         trimmed_Mfg_Info = trimmed_Mfg_Info.rstrip(";")
         trimmed_Mfg_Info = trimmed_Mfg_Info.lstrip('"')
         with allure.step(f"mfg Info response :  {trimmed_Mfg_Info}"):
             context.MfgInfo_resp = trimmed_Mfg_Info


@then(u'it should return manufacturing information split into various components')
def step_impl(context):
    trimmed_Mfg_Info = context.MfgInfo_resp
    # Initialize an empty dictionary
    boards_dict = {}
    with allure.step(f"Processing mfg Info response..."):
        # Process each board section
        for section in trimmed_Mfg_Info.strip().split(';'):
            with allure.step(f"Section :  {section}"):
                section = section.strip()
                if not section:
                    continue
                if ":" in section:
                    key, values = section.split(": ", 1)  # Split at the first colon
                    attributes = dict(item.split("=") for item in values.split(", "))  # Convert attributes to dict
                    boards_dict[key.strip()] = attributes  # Assign to dictionary


    #with allure.step(f"boards Dict :  {boards_dict}"):
        # Print the structured dictionary
    print(boards_dict)

    Components = boards_dict.keys()
    with allure.step(f"split into various Components {Components}"):
        for sub in Components:
            with allure.step(f"Component : {sub}"):
                print(sub)
    # Separate site info into various components
    context.actual_board_dict = boards_dict
    pass


@then(u'it should log each component')
def step_impl(context):

    with allure.step(f"Expected Components : {list(site_component_attributes.keys())}"):

        with allure.step(f"Actual Component :  {list(context.actual_board_dict.keys())}"):
            print(context.actual_board_dict.keys())
    pass


@then(u'it should verify each expected component and its attributes for the specified platform')
def step_impl(context):
    with allure.step("Verify each Components "):
        #context.actual_attributes = None
        for expected_component, expected_attributes in site_component_attributes.items():
            if  expected_component in context.actual_board_dict.keys():
                expect_found = True
                # Get the entire dictionary for expected i.e 'controllerboard'
                actual_attributes = context.actual_board_dict[expected_component]

            with allure.step(f"Verify Expected component {expected_component} : {actual_attributes} "):
                result = compare(f"{expected_component} found", "true",
                                 "false" if not actual_attributes else "true", "CompareNot")

                assert result == TestStatus.Pass


            with allure.step(f"Verify each Attributes {actual_attributes}"):
                attributes = {pair[0].strip(): pair[1].strip() for pair in
                  [attr.split('=') for attr in actual_attributes.split(',')]}

                for expected_attribute in expected_attributes:
                    message = f"{expected_component} {expected_attribute}"
                    actual_attribute = attributes.get(expected_attribute, "")
                    if expected_attribute == "PartNumber":
                        assert compare(message, r"^\d\d\d-\d\d\d-\d\d$", actual_attribute, "CompareRegex",
                                       options=custom_options) == TestStatus.Pass
                        assert compare(message, "ffffffffff", actual_attribute, "CompareNot",
                                       options=custom_options) == TestStatus.Pass
                    elif expected_attribute == "SerialNumber":
                        assert compare(message, r"^[a-zA-Z0-9]{8,}$", actual_attribute, "CompareRegex",
                                       options=custom_options) == TestStatus.Pass
                        assert compare(message, "ffffffff", actual_attribute, "CompareNot",
                                       options=custom_options) == TestStatus.Pass
                    elif expected_attribute == "Revision":
                        if len(actual_attribute) == 1:
                            assert compare(message, r"^[a-zA-Z]{1}$", actual_attribute, "CompareRegex",
                                           options=custom_options) == TestStatus.Pass
                            assert compare(message, "f", actual_attribute, "CompareNot",
                                           options=custom_options) == TestStatus.Pass
                        elif len(actual_attribute) == 2:
                            assert compare(message, r"^[a-zA-Z]{1}[0-9]{1}$", actual_attribute, "CompareRegex",
                                           options=custom_options) == TestStatus.Pass
                            assert compare(message, "ff", actual_attribute, "CompareNot",
                                           options=custom_options) == TestStatus.Pass
                        else:
                            assert compare(message + " length", "2", len(actual_attribute), "CompareMax",
                                           options=custom_options) == TestStatus.Pass
                    elif expected_attribute == "RevisionDate":
                        assert compare(message, r"^\d\d\d\d[a-zA-Z]{1}$", actual_attribute, "CompareRegex",
                                       options=custom_options) == TestStatus.Pass
                        assert compare(message, "fffff", actual_attribute, "CompareNot",
                                       options=custom_options) == TestStatus.Pass
                    elif expected_attribute == "MacAddress":
                        assert compare(message, r"^([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2})$", actual_attribute, "CompareRegex",
                                       options=custom_options) == TestStatus.Pass
                        assert compare(message, "fffffffffffffffff", actual_attribute, "CompareNot",
                                       options=custom_options) == TestStatus.Pass

    pass




@given(u'I have a properly set up TestSiteFpInternal')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I have a properly set up TestSiteFpInternal')


@given(u'the Functional Processor (FP) address is not null')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the Functional Processor (FP) address is not null')


@when(u'I call the GetMfgInfo method for FP')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the GetMfgInfo method for FP')
