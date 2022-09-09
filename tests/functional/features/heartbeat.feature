Feature: Heartbeat check
  As a user of the service
  I want to ensure that the heartbeat endpoint is functional
  So that I can confirm the service is running

  Scenario: Check heartbeat endpoint
    Given the base URL is "http://localhost:8000"
    When I make a GET request to "/heartbeat"
    Then the response status code should be 200
    And the response JSON should contain
      """
      {
        "status": "up"
      }
      """
