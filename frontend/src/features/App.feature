Feature: Button presence in the app header

  Scenario: The button is visible
    Given the App is loaded
    When I look at the header
    Then I should see a button with text "bbb"

  Scenario: The word is visible
    Given the App is loaded
    When I look at the header
    Then I should see a word with text "bbb"