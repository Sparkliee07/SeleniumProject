@DEP_DHCP
#DHCP Client IP Assignment Validation
Feature: DHCP Client Service IP Assignment Validation
  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-17629
  @allure.issue:UI-123
  @allure.tms:TMS-456
  @prerequisite
  Scenario: Verify the IP assignment to System PC through DHCP
    Given Correct switch port connections to active DHCP client devices and the network connection is active
    When the network diagram is available in the Doc-reference sheet
    Then verify DHCP network diagram


  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9012
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9012
  Scenario: Verify Atlas DHCP as an actual windows service
    Given Atlas DHCP Client service is configured to start automatically
    And Open DHCP process is running as expected
    When open the "services.msc" application
    Then should see the Atlas DHCP Client service with the "Automatic" start setting
    And Open DHCP process should be running

    When stop the Atlas DHCP Client service
    Then Atlas DHCP Client service should stop running in the services list
    And Open DHCP process should no longer be running in the Task Manager

    When open Task Manager in a separate window
    Then should not see the Open DHCP process running in the Task Manager

    When start the Atlas DHCP Client service
    Then Atlas DHCP Client service should start running again in the services list
    And Open DHCP process may or may not start running after the service restart

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9011
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9011
  Scenario: Verify DHCP Service - IP assignment RCB
    Given The network connection is active
    When ping the IP address "192.168.1.202"
    Then should receive a ping reply with no errors or timeouts

  #Scenario: Verify manual IP assignment for System PC in AMZ 1.0 build
  #  Given the System PC is part of the AMZ 1.0 build
  #  When I check the IP configuration of System PC
  #  Then the IP address should be manually assigned and not via DHCP

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9010
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9010
  Scenario: Verify the IP assignment to System PC through DHCP
    Given The network connection is active
    When ping the IP address "192.168.100.1"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9009
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9009
  Scenario: Verify DHCP Service - IP assignment SOM
    Given The network connection is active
    When ping the IP address "192.168.1.2"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9008
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9008
  Scenario: Verify DHCP Service - IP assignment SOM
    Given The network connection is active
    When ping the IP address "192.168.1.2"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9007
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9007
  Scenario: Verify DHCP Service - IP assignment Light Tower
    Given The network connection is active
    When ping the IP address "192.168.100.51"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9006
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9006
  Scenario: Verify DHCP Service - IP assignment SLTB
    Given The network connection is active
    When ping the IP address "192.168.1.201"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9005
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @HAL-9005
  Scenario: Verify DHCP Service - IP assignment System Switch
    Given The network connection is active
    When ping the IP address "192.168.100.254"
    Then should receive a ping reply with no errors or timeouts

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-900
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @prerequisite1
  Scenario: Verify that an unregistered laptop does not receive an IP address from DHCP
    Given a Windows laptop port is configured as a DHCP client
    When I connect the laptop's DHCP client port to an unreserved port on the system switch
    Then the laptop should be denied an IP address if it is not part of the network diagram

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-9004
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @prerequisite1
  @HAL-9004
  Scenario: Verify DHCP service deny IPAddress to unknown devices
    Given The laptop is connected to an unreserved switch port
    When run the command 'ipconfig /release' from the command line
    Then The laptop's current IP configuration should be released

    When run the command 'ipconfig /renew' from the command line
    Then after a few minutes, a DHCP configuration error should be displayed

    When run the command 'ipconfig /all' from the command line
    Then there should be no DHCP gateway server or DHCP server listed for the Ethernet port

@critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-900
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @prerequisite1
  @HAL-9003
  Scenario: Verify system switch IP assignment and DHCP service log
    Given the system has been turned up as part of the system bring-up process
    And the system switch is initially assigned the IP address "192.168.250.1"
    When view the DHCP service log at "\OpenDHCPServer\Log"
    Then the system switch should be assigned the static IP address "192.168.100.254"
    And there should be no DHCP IP-to-MAC coupling in the Open DHCP ini file updates in the service log

  @critical
  @allure.label.owner:Muthu
  @allure.link:https://teradyne-ist.atlassian.net/browse/HAL-900
  @allure.issue:UI-xxx
  @allure.tms:TMS-xxx
  @prerequisite1
  @HAL-9002
  Scenario: Verify CDU IP Assignment
    Given the system startup has finished
    When ping all connected active CDU devices
    Then should receive a ping reply with no errors or timeouts

    When view or grep the DHCP service log file
    Then the DHCP service should assign IP addresses according to the network diagram





