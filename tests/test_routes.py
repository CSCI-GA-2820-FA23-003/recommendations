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
from service.models import db, RecommendationType, Recommendation
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
        """It should post a sample recommendation"""
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
        """It should post a sample recommendation with no type"""
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
        expected_data["type"] = RecommendationType.CROSSSELL.name

        if "id" in response_data:
            del response_data["id"]

        if "id" in data:
            del data["id"]

        # Verify that the response data matches the expected data
        self.assertEqual(response_data, data)

    def test_bad_path_post_recommendation(self):
        """It should not post a sample recommendation with a bad path"""
        # Define a sample JSON data to send in the POST request
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendations", data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 404)

    def test_find(self):
        """It should find a recommendation by id"""
        target = RecommendationFactory()
        target.create()

        self.assertEqual = (
            Recommendation.find(target.id),
            target.id,
            "find result unmatch",
        )

    def test_delete(self):
        """It should delete a recommendation if it is in the DB"""
        target = RecommendationFactory()
        target.create()
        resp = self.client.post("/recommendation", json=target.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        recommendation = resp.get_json()

        resp = self.client.delete(f"/recommendation/{recommendation['id']}")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_recommendation(self):
        """It should update a recommendation"""
        target = RecommendationFactory()
        resp = self.client.post("/recommendation", json=target.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_target = resp.get_json()
        new_target["name"] = "ABC"
        response = self.client.put(
            f"/recommendation/{new_target['id']}", json=new_target
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_recommendation = response.get_json()
        self.assertEqual(update_recommendation["name"], "ABC")
