Feature: Embedded - UART API Testing

  Scenario: Verify the SetProperty API with valid and invalid parameters
    Given the test site is initialized
    When the loopback mode and data generator mode are tested for valid UARTs
    And invalid UARTs and properties are tested
    Then the API should handle valid and invalid parameters correctly, throwing appropriate exceptions

  Scenario: Verify the UartSetBaudRate API with valid and invalid parameters
    Given the test site is initialized
    When baud rate configuration is tested for valid UARTs
    And invalid : <UART_ID> and <Baud_Rate> are tested
    Then the API should configure baud rates correctly for valid UARTs and throw exceptions for invalid parameters

    Examples:
      | UART_ID   | Baud_Rate |
      | 1         | 1   |
      | 2         | 2   |


  Scenario: Verify the UartSetEnable API with valid and invalid parameters
    Given the test site is initialized
    When enabling and disabling UARTs is tested
    And UART configuration register values are verified
    And invalid UARTs are tested
    Then the API should enable/disable UARTs correctly and handle invalid parameters with exceptions

  Scenario: Verify the UartSend API with valid and invalid parameters
    Given the test site is initialized
    When data is sent to valid UARTs
    And invalid UARTs and data sizes are tested
    Then the API should send data correctly to valid UARTs and handle invalid parameters with exceptions

  Scenario: Verify the UartReceive API with valid and invalid parameters
    Given the test site is initialized
    When data is received from valid UARTs
    And invalid UARTs and data sizes are tested
    Then the API should receive data correctly from valid UARTs and handle invalid parameters with exceptions

  Scenario: Verify the UART logging functionality
    Given the test site is initialized
    When logging is started, synced, and stopped for valid UARTs
    And log file creation and data integrity are verified
    And invalid UARTs are tested
    Then logging should work correctly for valid UARTs and handle invalid parameters with exceptions

  Scenario: Verify the UartGetStatus API with valid and invalid parameters
    Given the test site is initialized
    When getting status for valid UARTs is tested
    And invalid UARTs are tested
    Then the API should return correct status for valid UARTs and handle invalid parameters with exceptions

  Scenario: Verify UART send and receive functionality with no timeout
    Given the test site is initialized
    When data is sent and received in loopback mode
    Then data should be sent and received correctly with no timeout
    And data integrity and performance should be validated

  Scenario: Verify UART send and receive functionality with timeout
    Given the test site is initialized
    When data is sent and received in loopback mode with timeout
    Then data should be sent and received correctly within the timeout period
    And data integrity and performance should be validated

  Scenario: Verify UART partial receive functionality
    Given the test site is initialized
    When partial data is sent and received
    Then partial data should be received correctly
    And data integrity and performance should be validated

  Scenario: Verify UART logging functionality during operations
    Given the test site is initialized
    When logging is tested during UART operations
    Then logging should work correctly during UART operations
    And log file creation and data integrity should be verified

  Scenario: Verify UART status functionality during operations
    Given the test site is initialized
    When UART status is tested after various operations
    Then UART status should be correct after operations
    And status values and error handling should be validated
