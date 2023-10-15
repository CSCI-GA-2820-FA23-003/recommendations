"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import json
from unittest import TestCase
from service import app
from service.models import db
from service.common import status  # HTTP Status Codes


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_post_recommendation(self):
        # Define a sample JSON data to send in the POST request
        data = {
            "id": "sampleRecommId",
            "name": "Sample Recommendation",
            "recommendation_id": 12345,
            "recommendation_name": "Another Sample Recommendation",
            "type": "CROSSSELL",
            "number_of_likes": 25,
            "number_of_dislikes": 5,
        }

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendation", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        # Verify that the response data matches the expected data
        expected_data = {
            "id": "sampleRecommId",
            "name": "Sample Recommendation",
            "recommendation_id": 12345,
            "recommendation_name": "Another Sample Recommendation",
            "type": 0,
            "number_of_likes": 25,
            "number_of_dislikes": 5,
        }
        self.assertEqual(response_data, expected_data)

    def test_post_recommendation_for_no_type(self):
        # Define a sample JSON data to send in the POST request
        data = {
            "id": "sampleRecommId",
            "name": "Sample Recommendation",
            "recommendation_id": 12345,
            "recommendation_name": "Another Sample Recommendation",
            "number_of_likes": 25,
            "number_of_dislikes": 5,
        }

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendation", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        # Verify that the response data matches the expected data
        expected_data = {
            "id": "sampleRecommId",
            "name": "Sample Recommendation",
            "recommendation_id": 12345,
            "recommendation_name": "Another Sample Recommendation",
            "type": 0,
            "number_of_likes": 25,
            "number_of_dislikes": 5,
        }
        self.assertEqual(response_data, expected_data)

    def test_bad_path_post_recommendation(self):
        # Define a sample JSON data to send in the POST request
        data = {
            "id": "sampleRecommId",
            "name": "Sample Recommendation",
            "recommendation_id": 12345,
            "recommendation_name": "Another Sample Recommendation",
            "number_of_likes": 25,
            "number_of_dislikes": 5,
        }

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendations", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 404)
