
Feature: Verify various property functionalities

  Scenario: Verify None property functionality
    Given the None property is initialized
    When I mark the property as tested using MarkTested(PropertyType.TER_PropertyType_None)
    And I set the None property using TestSetProperty(PropertyType.TER_PropertyType_None, 0)
    And I get the None property using TestGetProperty(PropertyType.TER_PropertyType_None)
    Then the None property should be set and retrieved without any issues

  Scenario: Verify SpiConfiguration property for different SPI buses
    Given various SPI buses are available
    When I mark the SpiConfiguration property as tested using MarkTested(PropertyType.TER_PropertyType_SpiConfiguration)
    And I test the SpiConfiguration property using TestSpiConfigBus()
    Then the SpiConfiguration property should be set and retrieved correctly for different SPI buses

  Scenario: Verify FpgaRegLoopback property functionality
    Given the FpgaRegLoopback property is initialized
    When I mark the property as tested using MarkTested(PropertyType.TER_PropertyType_FpgaRegLoopback)
    And I set the property using TestSetProperty(PropertyType.TER_PropertyType_FpgaRegLoopback, 1)
    And I write and read fake registers to verify loopback functionality
    And I restore the property using TestSetProperty(PropertyType.TER_PropertyType_FpgaRegLoopback, 0)
    Then the FpgaRegLoopback property should be set, verified, and restored correctly

  Scenario: Verify FpBootMode property
    Given different FpBootMode values are available
    When I mark the property as tested using MarkTested(PropertyType.TER_PropertyType_FpBootMode)
    And I get the original property values using TestSiteInternal.GetProperty(PropertyType.TER_PropertyType_FpBootMode, 1)
    And I set and get the FpBootMode property for different values
    And I handle invalid values and verify the correct error is thrown
    And I restore the original property values
    Then the FpBootMode property should be set and retrieved correctly, and invalid values should return the correct error

  Scenario: Verify FpBootFlash property
    Given different FpBootFlash values are available
    When I mark the property as tested using MarkTested(PropertyType.TER_PropertyType_FpBootFlash)
    And I get the original property values using TestSiteInternal.GetProperty(PropertyType.TER_PropertyType_FpBootFlash, 1)
    And I set and get the FpBootFlash property for different values
    And I handle invalid values and verify the correct error is thrown
    And I restore the original property values
    Then the FpBootFlash property should be set and retrieved correctly, and invalid values should return the correct error
