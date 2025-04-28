Feature: Embedded - Validate various functionalities of embedded software

  Scenario: Backup and Restore TFTP Files
    Given a CustomDefault.json file exists
    When the file is backed up
    Then the backup file should be created successfully
    When the file is restored from backup
    Then the original file should be restored correctly
    And backup and restore operations should handle exceptions gracefully

  Scenario: Fetch Embedded Software Information
    Given the TestEmbSwInfoInterface is invoked
    When versions are fetched for application, bootloader, FPGA, and controller components
    Then the retrieved versions should be correct
    And regex patterns should match the expected outputs

  Scenario: Test XML Parser Functionality
    Given the TestXmlParser is invoked
    When a module is located in the TFTP path
    And values for application, FPGA, and default FPGA are fetched using regex patterns
    Then the retrieved values should match expected results

  Scenario: Update Customer Default Values (Boolean)
    Given a boolean key "TITANHP_IB_BB_PRESENT" in the customer default file
    When its value is toggled between true and false
    Then the updated value should be saved and retrieved successfully
    When performing the same operations for a non-existing key "TITANHP_IB_BB_PRESENT_NotExist"
    Then non-existing keys should be handled gracefully

  Scenario: Update Customer Default Values (Integer)
    Given an integer key "INT_TYPE_KEY_EXIST" in the customer default file
    When its value is updated to 32
    Then the updated value should be saved and retrieved successfully
    When performing the same operations for a non-existing key "INT_TYPE_KEY_NOT_EXIST"
    Then non-existing keys should be handled gracefully

  Scenario: Update Customer Default Values (Double)
    Given a double key "DOUBLE_TYPE_KEY_EXIST" in the customer default file
    When its value is updated to 32.3233
    Then the updated value should be saved and retrieved successfully
    When performing the same operations for a non-existing key "DOUBLE_TYPE_KEY_NOT_EXIST"
    Then non-existing keys should be handled gracefully

  Scenario: Update Customer Default Values (HEXINT)
    Given a hexadecimal integer key "Tmsk" in the customer default file
    When its value is updated to 0x1234
    Then the updated value should be saved and retrieved successfully
    When performing the same operations for a non-existing key "Tmsk_Not_Exist"
    Then non-existing keys should be handled gracefully

  Scenario: Update Customer Default Values (String)
    Given a string key "NAS_IP" in the customer default file
    When its value is updated to "I DO NOT KNOW JSON"
    Then the updated value should be saved and retrieved successfully
    When performing the same operations for a non-existing key "NAS_IP_NOT_EXIST"
    Then non-existing keys should be handled gracefully

  Scenario: Exception Handling for Backup and Restore
    Given no backup file exists
    When an attempt is made to back up a non-existing file
    Then an exception should be thrown and logged
    When an attempt is made to restore a non-existing file
    Then no crashes or unhandled errors should occur
    And appropriate exception messages should be logged