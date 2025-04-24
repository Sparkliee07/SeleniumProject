Feature: Embedded - FP Boot and Reboot Validation

  Scenario: FP Reboot Test (All Boot Modes)
    Given the FP supports boot modes "SelectPxeBoot" and "SelectSsdBoot"
    When I invoke the RebootFpTest method
    Then the FP should successfully reboot in each boot mode
    And the current FP boot mode should be logged
    When I reboot FP into each boot mode
    Then the reboot steps and results should be properly logged
    And for "SelectPxeBoot", Linux boot should be verified using AssertLinuxBoot
    And for "SelectSsdBoot", Windows boot should be verified using AssertWindowsBoot
    And the results for each boot mode should be logged

  Scenario: Multi-SIO Reboot Test
    Given a list of valid SIO IPs and a reboot timeout parameter
    When I configure SioIpAddresses with valid IPs
    And set the SioRebootTimeInSeconds parameter
    And invoke the MultiSIOsRebootTest method
    Then each SIO should reboot successfully within the timeout
    And logs should capture any failure cases

  Scenario: Validation of Linux FP Boot
    Given a valid Linux FP with IP "<Linux IP>"
    When I invoke the AssertLinuxFpBoot method with the valid IP
    Then I should establish an SSH connection
    When I execute the "uname -a" command
    Then the hostname in the output should match the expected LinuxExpectedHostname

  Scenario: Validation of Windows FP Boot
    Given a valid Windows FP with IP "<Windows IP>"
    When I invoke the AssertWindowsBoot method with the valid IP
    Then I should establish a remote connection
    When I execute the "systeminfo" command
    Then the output should contain the correct Windows OS details

  Scenario: FP Boot Mode Transition
    Given the FP supports boot modes "SelectPxeBoot" and "SelectSsdBoot"
    When I reboot FP from "SelectPxeBoot" to "SelectSsdBoot"
    Then the FP should successfully reboot into the new boot mode
    When I reboot FP from "SelectSsdBoot" to "SelectPxeBoot"
    Then the FP should successfully reboot back
    And all transition steps should be logged

  Scenario: Negative Testing for Invalid Conditions
    Given an FP with invalid configurations
    When I use invalid IP addresses in SioIpAddresses
    Then the system should log proper error messages
    When I test missing Linux credentials
    Then the system should not crash or throw unhandled exceptions
    When I attempt to boot with an unsupported mode
    Then the system should reject the request and log an error
    When I test timeout conditions during FP/SIO reboot
    Then the system should handle the timeout gracefully
