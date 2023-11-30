Feature: The Recommendation service back-end
    As a Recommendation Owner
    I need a RESTful recommendation service
    So that I can keep track of all my Recommendations

Background:
    Given the following recommendations
        |rec_id | source_pid | name         | recommendation_name  | type       | number_of_likes | number_of_dislikes |
        |1      | 1          | chocolate    | marshmellow          | CROSSSELL  | 0 | 0 |
        |2      | 2          | granola      | yogurt               | CROSSSELL  | 1 | 0 |
        |3      | 3          | blueberry    | strawberry           | CROSSSELL  | 2 | 1 |
        |4      | 4          | wine opener  | red wine             | ACCESSORY  | 3 | 2 |

# Scenario: The server is running
#     When I visit the "Home Page"
#     Then I should see "Recommendation RESTful Service" in the title
#     And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "rec_id" to "123"
    And I set the "source_pid" to "123"
    And I set the "name" to "Hippo"
    And I set the "recommendation_name" to "Sample 1"
    And I select "Upsell" in the "type" dropdown
    And I set the "number_of_likes" to "0"
    And I set the "number_of_dislikes" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    # When I copy the "Id" field
    # And I press the "Clear" button
    # Then the "Id" field should be empty
    # And the "Name" field should be empty
    # And the "Category" field should be empty
    # When I paste the "Id" field
    # And I press the "Retrieve" button
    # Then I should see the message "Success"
    # And I should see "Happy" in the "Name" field
    # And I should see "Hippo" in the "Category" field
    # And I should see "False" in the "Available" dropdown
    # And I should see "Male" in the "Gender" dropdown
    # And I should see "2022-06-16" in the "Birthday" field

# Scenario: List all Recommendations
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Search for dogs
#     When I visit the "Home Page"
#     And I set the "Category" to "dog"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should not see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Search for available
#     When I visit the "Home Page"
#     And I select "True" in the "Available" dropdown
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should see "sammy" in the results
#     And I should not see "leo" in the results

# Scenario: Update a Recommendation
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Loki"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the results
#     And I should not see "fido" in the results

# Scenario: Delete a Recommendation
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I press the "Delete" button
#     Then I should see the message "Recommendation has been Deleted!"
#     When I press the "Clear" button
#     When I press the "Search" button
#     Then I should see the message "Success"
#     And I should not see "fido" in the results
