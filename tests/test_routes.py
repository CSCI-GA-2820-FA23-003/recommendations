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

logging.basicConfig(level=logging.DEBUG)
BASE_URL = "/recommendation"


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

    def _create_recommendations(self, n_count, *args):
        """Factory method to create n recommendations"""

        recommendations = []
        for i in range(n_count):
            test_recommendation = RecommendationFactory()
            if type(args[0]) == list and i < len(args[0]):
                test_recommendation.source_pid = args[0][i][0]
                test_recommendation.recommendation_id = args[0][i][1]
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test recommendation",
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        logging.debug("Test Recommendation: %s", len(recommendations))
        return recommendations

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

        self.assertEqual(
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

    def test_list_recommendations(self):
        """It should Get a list of recommendations filtered by source_pid"""

        """Use '._create_recommendations' to add dump data 
        and assign their source_pid, commendation_pid"""
        # recommendations = self._create_recommendations(
        #     5, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
        # )
        response = self.client.get(f"{BASE_URL}/list/{0}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        for recommendation in data:
            self.assertEqual(recommendation["source_pid"], 0)
        response = self.client.get(f"{BASE_URL}/list/12387128317293789")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_request(self):
        """It should return a bad request"""
        target = {}
        resp = self.client.get(BASE_URL, json=target)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_recommendation(self):
        # Choose an ID that is very unlikely to exist in your database
        nonexistent_id = 9999999

        # Send a DELETE request to the /recommendation/{id} route with the non-existent ID
        response = self.client.delete(f"{BASE_URL}/{nonexistent_id}")

        # Check that the response status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_nonexistent_recommendation(self):
        """It should return 404 when trying to update a non-existent recommendation"""
        # Choose an ID that is very unlikely to exist in your database
        nonexistent_id = 9999999

        # Define a sample JSON data for the update request
        update_data = {
            "field1": "new_value1",
            "field2": "new_value2",
            # Add other fields as needed
        }

        # Send a PUT request to the /recommendation/{id} route with the non-existent ID and update data
        response = self.client.put(f"{BASE_URL}/{nonexistent_id}", json=update_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
