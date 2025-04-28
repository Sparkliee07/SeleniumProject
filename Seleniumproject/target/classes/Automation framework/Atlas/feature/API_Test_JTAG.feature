Feature: Embedded - JTAG API Testing

  Scenario: Verify JTAG Set Enable API with valid and invalid parameters
    Given the test site is initialized
    When JtagSetEnable() is called with different jtagId and enableState values
    Then the JTAG enable state should be set correctly
    When the FPGA register is read to verify the enable state
    Then the enable state should match the expected value
    When JtagSetEnable() is called with an invalid JTAG ID
    Then the API should throw an argument invalid exception

  Scenario: Verify JTAG Reset API with valid and invalid parameters
    Given the test site is initialized
    When JtagReset() is called with different reset types and durations
    Then the JTAG should be reset correctly
    When JtagReset() is called with an invalid JTAG ID or reset type
    Then the API should throw an argument invalid exception

  Scenario: Verify JTAG Instruction Register Data Transfer
    Given the test site is initialized
    When JtagWriteReadIR() is called with valid data
    Then the data sent should match the data received
    When JtagWriteReadIR() is called with invalid data length or bit count
    Then the API should throw an argument invalid exception

  Scenario: Verify JTAG Data Register Data Transfer
    Given the test site is initialized
    When JtagWriteReadDR() is called with valid data
    Then the data sent should match the data received
    When JtagWriteReadDR() is called with invalid data length or bit count
    Then the API should throw an argument invalid exception

  Scenario: Verify JTAG Clock Rate Setting
    Given the test site is initialized
    When the original clock divider value is retrieved using TestSiteInternal.GetRegisters
    And a new clock rate is set
    Then the clock rate should be set correctly and match the expected rate

  Scenario: Verify JTAG Write-Read IR Buffer Overflow
    Given the test site is initialized
    When the maximum byte of data is sent using JtagWriteReadIR()
    Then the data sent should match the data received
    When overflow data is sent using JtagWriteReadIR()
    Then the API should throw a buffer overflow exception

  Scenario: Verify JTAG Write-Read DR Buffer Overflow
    Given the test site is initialized
    When the maximum byte of data is sent using JtagWriteReadDR()
    Then the data sent should match the data received
    When overflow data is sent using JtagWriteReadDR()
    Then the API should throw a buffer overflow exception

  Scenario: Verify JTAG Write-Read IR Performance
    Given the test site is initialized
    When the maximum byte of data is continuously sent using JtagWriteReadIR()
    Then the data transfer should be correct
    When the delay time between write and read operations is measured
    Then it should match the expected clock rate timing
