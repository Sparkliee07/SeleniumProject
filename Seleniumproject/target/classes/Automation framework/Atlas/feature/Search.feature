Feature: Search Feature
  Scenario: Search for a valid product
    Given I navigate to application
    When I enter valid product into Search box
    And I click on Search button
    Then Valid product should be displayed in Search results page

  Scenario: Search for a invalid product
    Given I navigate to application
    When I enter invalid product into Search box
    And I click on Search button
    Then Proper message should be displayed in Search results page
