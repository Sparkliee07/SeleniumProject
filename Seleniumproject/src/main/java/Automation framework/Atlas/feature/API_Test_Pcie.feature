Feature: Embedded - PCIe Functionality Testing

  Scenario: Verify PCIe rescan functionality
    Given FP PCIe setup is enabled
    When I perform PCIe rescan
    Then PCIe rescan should complete successfully

  Scenario: Verify retrieval of PCIe functions
    Given FP PCIe setup is enabled
    When I get PCIe functions for PcieId.Pcie_1
    Then PCIe functions should be retrieved and logged successfully

  Scenario: Verify retrieval of PCIe information
    Given FP PCIe setup is enabled
    When I get PCIe information for PcieId.Pcie_1 function 0
    Then PCIe information should be retrieved and logged successfully

  Scenario: Verify retrieval of PCIe status
    Given FP PCIe setup is enabled
    When I get PCIe status for PcieId.Pcie_1 function 0
    Then PCIe status should be retrieved and logged successfully

  Scenario: Verify PCIe function reset
    Given FP PCIe setup is enabled
    When I perform PCIe function reset for PcieId.Pcie_1 function 0
    Then a ClientException with the correct error code should be thrown

  Scenario: Verify PCIe device removal
    Given FP PCIe setup is enabled
    When I perform PCIe device removal for PcieId.Pcie_1 function 0
    Then PCIe device should be removed successfully

  Scenario: Verify enabling and disabling of FP PCIe
    Given FP PCIe setup is enabled
    When I enable and disable FP PCIe for PcieId.Pcie_1 function 0
    Then FP PCIe should be enabled and disabled successfully

  Scenario: Verify handling of exceptions for enabling and disabling FP PCIe
    Given FP PCIe setup is enabled
    When I enable and disable FP PCIe for PcieId.Pcie_1 function 0
    Then a ClientException with the correct error code should be thrown

  Scenario: Verify retrieval of FP PCIe domain
    Given FP PCIe setup is enabled
    When I get PCIe domain for PcieId.Pcie_1
    Then PCIe domain should be retrieved and logged successfully

  Scenario: Verify retrieval of FP PCIe speed
    Given FP PCIe setup is enabled
    When I enable FP PCIe and get PCIe speed for PcieId.Pcie_1 function 0
    Then PCIe speed should be retrieved and logged successfully

  Scenario: Verify handling of exceptions for retrieving FP PCIe speed
    Given FP PCIe setup is enabled
    When I enable and disable FP PCIe and get PCIe speed for PcieId.Pcie_1 function 0
    Then a ClientException with the correct error code should be thrown

  Scenario: Verify retrieval of FP PCIe device ID
    Given FP PCIe setup is enabled
    When I enable FP PCIe and get PCIe device ID for PcieId.Pcie_1 function 0
    Then PCIe device ID should be retrieved and logged successfully

  Scenario: Verify handling of exceptions for retrieving FP PCIe device ID
    Given FP PCIe setup is enabled
    When I enable and disable FP PCIe and get PCIe device ID for PcieId.Pcie_1 function 0
    Then a ClientException with the correct error code should be thrown

  Scenario: Verify FP PCIe functionality after reboot
    Given FP PCIe setup is enabled
    When I enable FP PCIe, reboot the FP, reconnect to the FP MRPC server, and validate PCIe enable status and speed
    Then FP PCIe should be enabled and speed should be retrieved successfully after reboot
