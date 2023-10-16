"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db
from service.common import status  # HTTP Status Codes
from tests.factories import RecommendationFactory


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
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendation", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        if "id" in response_data:
            del response_data["id"]

        if "id" in data:
            del data["id"]

        self.assertEqual(response_data, data)

    def test_post_recommendation_for_no_type(self):
        # Define a sample JSON data to send in the POST request
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        if "type" in data:
            del data["type"]

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendation", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        # Since default type is CROSSSELL, the default will have CROSSSELL as its type
        expected_data = data
        expected_data["type"] = "CROSSSELL"

        # Verify that the response data matches the expected data
        self.assertEqual(response_data, expected_data)

    def test_bad_path_post_recommendation(self):
        # Define a sample JSON data to send in the POST request
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendations", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 404)
