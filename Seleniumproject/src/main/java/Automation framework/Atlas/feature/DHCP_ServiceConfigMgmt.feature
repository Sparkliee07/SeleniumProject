Feature: DHCP Service Configuration Management
  As a network administrator
  I want to manage the DHCP server configuration
  So that it reflects the current network setup

  Scenario: Load switch port to IP address mapping
    Given the DHCP service is running
    When the switch port to IP address mapping is loaded from "SwitchModel.json"
    Then the mapping should be applied to the DHCP server configuration

  Scenario: Discover devices using SNMP
    Given the DHCP service is running
    When the service discovers devices using SNMP
    Then the MAC addresses of connected devices should be mapped to their respective IP addresses

  Scenario: Restart DHCP server to apply changes
    Given the DHCP service is running
    When the DHCP server configuration is updated
    Then the DHCP server should be restarted to apply the changes

  Scenario: Validate DHCP server settings
    Given the DHCP service is running
    When the DHCP server settings are validated
    Then any invalid settings should be replaced with defaults
    And the DHCP server should be restarted

  Scenario: Manage DHCP server as a Windows service
    Given the DHCP service is running as a Windows service
    When the DHCP server is stopped
    Then the DHCP service should restart the DHCP server as a Windows service

  Scenario: Manage DHCP server as a process
    Given the DHCP service is running as a process
    When the DHCP server is stopped
    Then the DHCP service should restart the DHCP server as a process



  Scenario: Spy on DHCP requests
    Given the DHCP service is running
    When DHCP requests are broadcast on the network
    Then the DHCP service should log the MAC address, message type, and hostname of each request

  Scenario: Scan a switch for connected devices
    Given the DHCP service is running
    When a switch with IP address "192.168.0.2" is scanned
    Then the MAC addresses and port numbers of connected devices should be logged