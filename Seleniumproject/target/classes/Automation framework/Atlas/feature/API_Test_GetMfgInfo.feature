@DEP_DHCP
#DHCP Client IP Assignment Validation
Feature: Get Manufacturing Info
  @critical
  @allure.label.owner:Muthu
  @allure.link:https:
  Scenario: Get Manufacturing Info
    Given I have a properly set up TestSiteInternal
    When I call the GetMfgInfo method
    Then it should return manufacturing information split into various components
    And it should log each component
    And it should verify each expected component and its attributes for the specified platform



