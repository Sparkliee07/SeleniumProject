Feature: DHCP Service IP Assignment
  As a network administrator
  I want the DHCP service to assign IP addresses correctly
  So that devices can communicate on the network

  Scenario: Assign IP address to a new device
    Given the DHCP service is running
    When a new device with MAC address "00:19:F3:00:C4:A4" connects to the network
    Then the device should be assigned the IP address "192.168.1.23"

  Scenario: Update IP address mapping for an existing device
    Given the DHCP service is running
    And a device with MAC address "00:19:F3:00:C4:A4" is connected to the network
    When the IP address mapping is updated to "192.168.2.253"
    Then the device should be assigned the new IP address "192.168.2.253"

  Scenario: Handle device reconnection
    Given the DHCP service is running
    And a device with MAC address "00:19:F3:00:C4:A4" was previously assigned the IP address "192.168.1.23"
    When the device reconnects to the network
    Then the device should be reassigned the IP address "192.168.1.23"

  Scenario: Exclude a device from IP assignment
    Given the DHCP service is running
    When a device with MAC address "00:19:F3:00:C4:33" connects to the network
    Then the device should not be assigned any IP address

  Scenario: Assign IP address to a device after DHCP server restart
    Given the DHCP service is running
    And a device with MAC address "00:19:F3:00:C4:A4" is connected to the network
    When the DHCP server is restarted
    Then the device should be reassigned the IP address "192.168.1.23"

  Scenario: Discover devices on system switch
    Given the DHCP service is running
    When the system switch is scanned using SNMP
    Then the MAC addresses of connected devices should be discovered
    And the devices should be assigned IP addresses based on the network diagram

  Scenario: Discover devices on pack switch
    Given the DHCP service is running
    And the pack switch has been assigned an IP address
    When the pack switch is scanned using SNMP
    Then the MAC addresses of connected devices should be discovered
    And the devices should be assigned IP addresses based on the network diagram

  Scenario: Discover devices on row switch
    Given the DHCP service is running
    And the row switch has been assigned an IP address
    When the row switch is scanned using SNMP
    Then the MAC addresses of connected devices should be discovered
    And the devices should be assigned IP addresses based on the network diagram

  Scenario: Handle recursive device discovery
    Given the DHCP service is running
    When devices are discovered recursively through system, pack, and row switches
    Then all devices should be assigned IP addresses correctly
    And the DHCP server should be restarted as needed