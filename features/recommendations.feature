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

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation RESTful Service" in the title
    And I should not see "404 Not Found"

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
    When I copy the "rec_id" field
    And I press the "Clear" button
    Then the "rec_id" field should be empty
    And the "name" field should be empty
    And the "recommendation_name" field should be empty
    When I paste the "rec_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hippo" in the "name" field
    And I should see "Sample 1" in the "recommendation_name" field
    And I should see "Upsell" in the "type" dropdown
    And I should see "0" in the "number_of_likes" field
    And I should see "1" in the "number_of_dislikes" field

# Scenario: List all Recommendations
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results


Scenario: List all Recommendations
        When I visit the "home page"
        And I press the "Clear" button
        And I press the "Search" button
        Then I should see the message "Success"
        And I should see "yogurt" in the results
        And I should see "strawberry" in the results
        # And I should see "strawberry1" in the results


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

Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "marshmellow" in the "recommendation_name" field
    And I should see "chocolate" in the "name" field
    When I copy the "rec_id" field
    And I press the "Clear" button
    Then the "rec_id" field should be empty
    When I paste the "rec_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "chocolate" in the "name" field
    And I should see "marshmellow" in the "recommendation_name" field
    When I change "recommendation_name" to "oreo"
    And I press the "Update" button
    Then I should see the message "Success"
    And I should see "oreo" in the "recommendation_name" field

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "name" to "chocolate"
    And I set the "recommendation_name" to "marshmellow"
    And I set the "source_pid" to "1"
    And I set the "rec_id" to "1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "rec_id" field 
    And I press the "Clear" button                            
    Then the "rec_id" field should be empty                           
    And the "source_pid" field should be empty                       
    And the "name" field should be empty                             
    And the "recommendation_name" field should be empty              
    When I paste the "rec_id" field                                      
    And I press the "Delete" button                                  
    Then I should see the message "Recommendation has been Deleted!"   