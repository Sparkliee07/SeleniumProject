Feature: User management

  Scenario Outline: Registration
    When I go to the registration form
    And I enter my details: <login>, <password>, <name>, <birthday>
    Then the profile should be created

    Examples:
      | login   | password | name     | birthday   |
      | johndoe | qwerty   | John Doe | 1970-01-01 |
      | janedoe | 123456   | Jane Doe | 1111-11-11 |