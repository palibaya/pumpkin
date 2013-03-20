Feature: Authentifiacation

  Scenario: Logging in to our new Django site

    Given a user
    When I log in
    Then I see home page
