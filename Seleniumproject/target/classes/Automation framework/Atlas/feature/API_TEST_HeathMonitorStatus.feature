Feature: Embedded - Site Status Verification

  Scenario: Verify the alarm bits of the site
    Given the site is operational
    When I call testHalosAlarmBits()
    Then the alarm bits should be as expected

  Scenario: Verify the status bits of the site
    Given the site is operational
    When I call testHalosStatusBits()
    Then the status bits should be as expected

  Scenario: Verify the thermal status of the site
    Given the site is operational
    When I call testHalosThermalStatus()
    Then the thermal status should be as expected

  Scenario: Verify the power status of the site
    Given the site is operational
    When I call testHalosPowerStatus()
    Then the power status should be as expected

  Scenario: Verify the Teradyne status of the site
    Given the site is operational
    When I call testHalosTeradyneStatus()
    Then the Teradyne status should be as expected

  Scenario: Verify the board temperature sensor readings
    Given the site is operational
    When I call testHalosBoardTempSensor()
    Then the temperature sensor readings should be within the expected range

  Scenario: Verify the baseboard ADC channel readings
    Given the site is operational
    When I call testHalosBaseBoardAdcChannels()
    Then the ADC channel readings should be within the expected range

  Scenario: Verify the lid status of the site
    Given the site is operational
    When I call testHalosLidStatus()
    Then the lid status should be as expected

  Scenario: Verify the power board power status
    Given the site is operational
    When I call testHalosPbPowerStatusInternal()
    Then the power status should be as expected

  Scenario: Verify the TCB power status
    Given the site is operational
    When I call testHalosTCBPowerStatusInternal()
    Then the power status should be as expected

  Scenario: Verify the internal thermal status
    Given the site is operational
    When I call testHalosThermalStatusInternal()
    Then the thermal status should be as expected

  Scenario: Verify the DUT I/O status
    Given the site is operational
    When I call testHalosDutIOStatusInternal()
    Then the DUT I/O status should be as expected

  Scenario: Verify the FP DUT I/O status
    Given the site is operational
    When I call testFpHalosDutIOStatusInternal()
    Then the FP DUT I/O status should be as expected

  Scenario: Verify the site fan status
    Given the site is operational
    When I call testSiteFanStatusInternal()
    Then the fan status should be as expected

  Scenario: Verify the alarm and status handling
    Given the site is operational
    When I call AlarmAndStatusTest()
    Then the alarm and status handling should be as expected

  Scenario: Verify the status bits handling
    Given the site is operational
    When I call StatusBitsTest()
    Then the status bits handling should be as expected

  Scenario: Verify the thermal status handling
    Given the site is operational
    When I call ThermalStatusTest()
    Then the thermal status handling should be as expected

  Scenario: Verify the power status handling
    Given the site is operational
    When I call PowerStatusTest()
    Then the power status handling should be as expected

  Scenario: Verify the temperature readings
    Given the site is operational
    When I call TemperatureTest()
    Then the temperature readings should be within the expected range

  Scenario: Verify the FP temperature readings
    Given the site is operational
    When I call TemperatureFpTest()
    Then the FP temperature readings should be within the expected range

  Scenario: Verify the lid status handling
    Given the site is operational
    When I call LidStatusTest()
    Then the lid status handling should be as expected

  Scenario: Verify the power board power status handling
    Given the site is operational
    When I call PowerBoardPowerStatusInternalTest()
    Then the power board power status handling should be as expected

  Scenario: Verify the thermal board power status handling
    Given the site is operational
    When I call ThermalBoardPowerStatusInternalTest()
    Then the thermal board power status handling should be as expected
