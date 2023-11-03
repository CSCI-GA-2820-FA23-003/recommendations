"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import logging
import json
from unittest import TestCase
from service import app
from service.models import RecommendationType
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

    def test_create_rec_no_content_type(self):
        """It should not Create a rec with no content"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

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

        """Use '._create_recommendations' to add dump data and assign their source_pid, commendation_pid"""
        # recommendations = self._create_recommendations(
        #     5, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
        # )
        response = self.client.get(f"{BASE_URL}/")
        data = response.get_json()
        if response.status_code == status.HTTP_200_OK:
            self.assertGreater(len(data), 0)
        else:
            self.assertEqual(len(data), 0)
        # for recommendation in data:
        #     self.assertEqual(recommendation["source_pid"], 0)
        # response = self.client.get(f"{BASE_URL}/list/12387128317293789")
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get(self):
        """It should Get a specific recommendation"""
        response = self.client.get(f"{BASE_URL}/")
        all_recommendations = response.get_json()
        if len(all_recommendations) == 0:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        else:
            id = all_recommendations[0]["id"]
            source_pid = all_recommendations[0]["source_pid"]
            recommendation_id = all_recommendations[0]["recommendation_id"]
            response = self.client.get(f"{BASE_URL}/{id}")
            data = response.get_json()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data["id"], id)
            self.assertEqual(data["source_pid"], source_pid)
            self.assertEqual(data["recommendation_id"], recommendation_id)

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_bad_request(self):
        """It should not create a recommendation with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed_handler(self):
        """It should trigger Method Not Allowed error handler"""
        resp = self.client.delete(f"{BASE_URL}")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # def test_rec_already_exists(self):
    #     """It should detect a recommendation that already exists"""
    #     fake_rec = RecommendationFactory()
    #     data = fake_rec.serialize()

    #     # Send a POST request to the /recommendation route with the sample data
    #     resp = self.client.post(
    #         "/recommendation", data=json.dumps(data), content_type="application/json"
    #     )
    #     resp = self.client.post(
    #         "/recommendation", data=json.dumps(data), content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
