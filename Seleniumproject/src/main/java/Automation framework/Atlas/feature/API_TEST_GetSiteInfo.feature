Feature: Embedded - Site Information Retrieval and Validation

  Scenario: Get Site Info Test
    Given the system has valid SIO and FP addresses
    When I retrieve the site information using GetSiteInfo()
    Then the site information should be retrieved successfully
    And I log the retrieved site information
    When I verify the site information using DoInfoVerification()
    Then the site information should be validated correctly
    When I check the site information with CheckSiteInfo()
    Then the information should be accurate and correctly checked

  Scenario: Get Site FP Info Test
    Given the system has valid SIO and FP addresses
    When I retrieve the functional processor address using GetFpAddress()
    Then the functional processor address should be retrieved successfully
    When I set up the FP platform with PlatformSetuFp()
    Then the FP platform should be initialized correctly
    When I retrieve the site info using TestFp.GetSiteInfo()
    Then the site information should be retrieved successfully
    And I log the retrieved site information
    When I verify the site info attributes
    Then the site information for the functional processor should be validated correctly
