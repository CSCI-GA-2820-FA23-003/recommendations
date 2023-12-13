######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then  # pylint: disable=no-name-in-module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = "rec_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################


@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"), name
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    assert found


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


### BDD test for like button


@then("I should see content table")
def step_impl(context):
    # Wait for the content table to be present and visible
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, "content-table"))
    )
    # Find the content table
    content_table = context.driver.find_element(By.ID, "content-table")

    # Assert that the content table is present and visible
    assert (
        content_table.is_displayed()
    ), "Content table with ID 'content-table' is not visible."


@when('I press the "Like" button at index "{index}"')
def step_impl(context, index):
    # Find the element that displays the number of likes
    likes_id = f"like-{index}"
    likes_element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, likes_id))
    )
    context.initial_likes = int(likes_element.text)

    # Click the like button
    like_button_id = f"like-button-{index}"
    like_button = context.driver.find_element(By.ID, like_button_id)
    like_button.click()


@then('the number of likes at index "{index}" should increase by 1')
def step_impl(context, index):
    likes_id = f"like-{index}"
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.staleness_of(context.driver.find_element(By.ID, likes_id))
    )
    likes_element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, likes_id))
    )
    new_likes = int(likes_element.text)
    assert (
        new_likes == context.initial_likes + 1
    ), "Like count did not increase as expected."


@when('I press the "Dislike" button at index "{index}"')
def step_impl(context, index):
    dislikes_id = f"dislike-{index}"
    dislikes_element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, dislikes_id))
    )
    context.initial_dislikes = int(dislikes_element.text)

    dislike_button_id = f"dislike-button-{index}"
    dislike_button = context.driver.find_element(By.ID, dislike_button_id)
    dislike_button.click()


@then('the number of dislikes at index "{index}" should increase by 1')
def step_impl(context, index):
    dislikes_id = f"dislike-{index}"
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.staleness_of(
            context.driver.find_element(By.ID, dislikes_id)
        )
    )
    dislikes_element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, dislikes_id))
    )
    new_dislikes = int(dislikes_element.text)
    assert (
        new_dislikes == context.initial_dislikes + 1
    ), "Dislike count did not increase as expected."
