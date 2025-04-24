Feature: Embedded - Validate retrieval and validation of site components

  Scenario: Verify retrieval and validation of site components for SIO address
    Given the test site is initialized
    When I retrieve the site components for the SIO address
    Then the retrieved site components should match the expected components

  Scenario: Verify retrieval and validation of site components for FP address
    Given I have a valid FP address
    When I set up the FP platform
    And I retrieve the site components for the FP address
    Then the retrieved site components should match the expected components
