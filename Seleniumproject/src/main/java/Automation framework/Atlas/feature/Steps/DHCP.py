from behave import given, when, then
from pythonping import ping
import allure
import pyautogui


@given("the network connection is active")
def step_given_network_active(context):
    # Placeholder for checking network connection (optional)
    # This is a placeholder. You can add network check logic if needed.
    context.network_active = True
    pass

@when('ping the IP address "{ip_address}"')
def step_when_ping_ip(context, ip_address):
    response = ping(ip_address, count=2, timeout=0.5)
    context.ping_result = response


@then("should receive a ping reply with no errors or timeouts")
def step_then_ping_successful(context):
    success = all(reply.success for reply in context.ping_result)
    assert success, f"Ping failed: {context.ping_result}"


@given("Atlas DHCP Client service is configured to start automatically")
def step_impl(context):
    # Capture the screen and save it
    screenshot_path = r"C:\Git\PythonAutomation\samples\features\Resource\image.png"

    #pyautogui.screenshot(screenshot_path)

    # Attach to Allure report
    with open(screenshot_path, "rb") as png_file:
        png_bytes = png_file.read()
    allure.attach(png_bytes, name="img", attachment_type=allure.attachment_type.PNG)

@given(u'Open DHCP process is running as expected')
def step_impl(context):
    # Capture the screen and save it
    screenshot_path = r"C:\Git\PythonAutomation\samples\features\Resource\image1.png"

    pyautogui.screenshot(screenshot_path)

    # Attach to Allure report
    with open(screenshot_path, "rb") as png_file:
        png_bytes = png_file.read()
    allure.attach(png_bytes, name="img", attachment_type=allure.attachment_type.PNG)
    raise NotImplementedError(u'STEP: Given Open DHCP process is running as expected')


@given(u'Correct switch port connections to active DHCP client devices and the network connection is active')
def step_impl(context):
    # Capture the screen and save it
    screenshot_path = "/Resource/image.png"
    pyautogui.screenshot(screenshot_path)

    # Attach to Allure report
    with open(screenshot_path, "rb") as png_file:
        png_bytes = png_file.read()
    allure.attach(png_bytes, name="img", attachment_type=allure.attachment_type.PNG)
    #raise NotImplementedError(u'STEP: Given Correct switch port connections to active DHCP client devices and the network connection is active')


@when(u'the network diagram is available in the Doc-reference sheet')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the network diagram is available in the Doc-reference sheet')


@then(u'verify DHCP network diagram')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then verify DHCP network diagram')




@when(u'open the "services.msc" application')
def step_impl(context):
    raise NotImplementedError(u'STEP: When open the "services.msc" application')


@then(u'should see the Atlas DHCP Client service with the "Automatic" start setting')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then should see the Atlas DHCP Client service with the "Automatic" start setting')


@then(u'Open DHCP process should be running')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Open DHCP process should be running')


@when(u'stop the Atlas DHCP Client service')
def step_impl(context):
    raise NotImplementedError(u'STEP: When stop the Atlas DHCP Client service')


@then(u'Atlas DHCP Client service should stop running in the services list')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Atlas DHCP Client service should stop running in the services list')


@then(u'Open DHCP process should no longer be running in the Task Manager')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Open DHCP process should no longer be running in the Task Manager')


@when(u'open Task Manager in a separate window')
def step_impl(context):
    raise NotImplementedError(u'STEP: When open Task Manager in a separate window')


@then(u'should not see the Open DHCP process running in the Task Manager')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then should not see the Open DHCP process running in the Task Manager')


@when(u'start the Atlas DHCP Client service')
def step_impl(context):
    raise NotImplementedError(u'STEP: When start the Atlas DHCP Client service')


@then(u'Atlas DHCP Client service should start running again in the services list')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Atlas DHCP Client service should start running again in the services list')


@then(u'Open DHCP process may or may not start running after the service restart')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Open DHCP process may or may not start running after the service restart')


@given(u'a Windows laptop port is configured as a DHCP client')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a Windows laptop port is configured as a DHCP client')


@when(u'I connect the laptop\'s DHCP client port to an unreserved port on the system switch')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I connect the laptop\'s DHCP client port to an unreserved port on the system switch')


@then(u'the laptop should be denied an IP address if it is not part of the network diagram')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the laptop should be denied an IP address if it is not part of the network diagram')


@given(u'The laptop is connected to an unreserved switch port')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given The laptop is connected to an unreserved switch port')


@when(u'run the command \'ipconfig /release\' from the command line')
def step_impl(context):
    raise NotImplementedError(u'STEP: When run the command \'ipconfig /release\' from the command line')


@then(u'The laptop\'s current IP configuration should be released')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then The laptop\'s current IP configuration should be released')


@when(u'run the command \'ipconfig /renew\' from the command line')
def step_impl(context):
    raise NotImplementedError(u'STEP: When run the command \'ipconfig /renew\' from the command line')


@then(u'after a few minutes, a DHCP configuration error should be displayed')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then after a few minutes, a DHCP configuration error should be displayed')


@when(u'run the command \'ipconfig /all\' from the command line')
def step_impl(context):
    raise NotImplementedError(u'STEP: When run the command \'ipconfig /all\' from the command line')


@then(u'there should be no DHCP gateway server or DHCP server listed for the Ethernet port')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then there should be no DHCP gateway server or DHCP server listed for the Ethernet port')


@given(u'the system has been turned up as part of the system bring-up process')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the system has been turned up as part of the system bring-up process')


@given(u'the system switch is initially assigned the IP address "192.168.250.1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the system switch is initially assigned the IP address "192.168.250.1"')


@when(u'view the DHCP service log at "\\OpenDHCPServer\\Log"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When view the DHCP service log at "\\OpenDHCPServer\\Log"')


@then(u'the system switch should be assigned the static IP address "192.168.100.254"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the system switch should be assigned the static IP address "192.168.100.254"')


@then(u'there should be no DHCP IP-to-MAC coupling in the Open DHCP ini file updates in the service log')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then there should be no DHCP IP-to-MAC coupling in the Open DHCP ini file updates in the service log')


@given(u'the system startup has finished')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the system startup has finished')


@when(u'ping all connected active CDU devices')
def step_impl(context):
    raise NotImplementedError(u'STEP: When ping all connected active CDU devices')

