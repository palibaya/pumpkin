Feature:  Manage Project

  Scenario: List of Project by authentificated user

    Given a user
    When I log in
    Then I see list of project in assign by me
