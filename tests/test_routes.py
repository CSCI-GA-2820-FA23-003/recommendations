"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import json
from urllib.parse import quote_plus
from unittest import TestCase
from service import app
from service.models import Recommendation, RecommendationType, db, init_db
from service.common import status  # HTTP Status Codes
from tests.factories import RecommendationFactory

logging.basicConfig(level=logging.DEBUG)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/api/recommendations"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""

    ############################################################
    # Utility functions
    ############################################################
    def _create_recommendations(self, count: int = 1) -> list:
        """Factory method to create n recommendations"""

        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test recommendation",
            )
            new_recommendation = response.get_json()
            test_recommendation.rec_id = new_recommendation["rec_id"]
            recommendations.append(test_recommendation)
        return recommendations

    # def get_rec_count(self):
    #     """save the current number of recommendations"""
    #     response = self.client.get(BASE_URL)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = response.get_json()
    #     # logging.debug("data = %s", data)
    #     return len(data)

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["message"], "OK")

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_list_all(self):
        """It should Get a list of recommendations"""
        self._create_recommendations(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get(self):
        """It should Get a specific recommendation"""
        # get the id of a recommendation
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_recommendation.rec_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(
            data["recommendation_name"], test_recommendation.recommendation_name
        )

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------

    def test_post_recommendation(self):
        """It should post a sample recommendation"""
        # Define a sample JSON data to send in the POST request
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            BASE_URL, data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        if "rec_id" in response_data:
            del response_data["rec_id"]

        if "rec_id" in data:
            del data["rec_id"]

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
            BASE_URL, data=json.dumps(data), content_type="application/json"
        )

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Deserialize the response JSON
        response_data = json.loads(response.data.decode("utf-8"))

        # Since default type is CROSSSELL, the default will have CROSSSELL as its type
        expected_data = data
        expected_data["type"] = RecommendationType.CROSSSELL.name

        if "rec_id" in response_data:
            del response_data["rec_id"]

        if "rec_id" in data:
            del data["rec_id"]

        # Verify that the response data matches the expected data
        self.assertEqual(response_data, data)

    def test_bad_path_post_recommendation(self):
        """It should not post a sample recommendation with a bad path"""
        # Define a sample JSON data to send in the POST request
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()

        # Send a POST request to the /recommendation route with the sample data
        response = self.client.post(
            "/recommendations_bad",
            data=json.dumps(data),
            content_type="application/json",
        )

        # Check the response status code
        self.assertEqual(response.status_code, 404)

    def test_create_rec_no_content_type(self):
        """It should not Create a rec with no content"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------

    def test_delete(self):
        """It should delete a recommendation"""
        recommendations = self._create_recommendations(5)
        # rec_count = self.get_rec_count()
        test_rec = recommendations[0]
        resp = self.client.delete(f"{BASE_URL}/{test_rec.rec_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------

    def test_update_recommendation(self):
        """It should update a recommendation"""
        target = RecommendationFactory()
        resp = self.client.post(BASE_URL, json=target.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_target = resp.get_json()
        new_target["name"] = "ABC"
        response = self.client.put(
            f"{BASE_URL}/{new_target['rec_id']}", json=new_target
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_recommendation = response.get_json()
        self.assertEqual(update_recommendation["name"], "ABC")

    def test_bad_request(self):
        """It should not create a recommendation with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed_handler(self):
        """It should trigger Method Not Allowed error handler"""
        resp = self.client.delete(f"{BASE_URL}")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_product_name(self):
        """It should Query Recommendations by a source product name"""
        recommendations = self._create_recommendations(5)
        test_name = recommendations[0].name
        name_count = len([rec for rec in recommendations if rec.name == test_name])
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["name"], test_name)

    def test_query_by_recommendation_name(self):
        """It should Query Recommendations by its name"""
        recommendations = self._create_recommendations(5)
        test_name = recommendations[0].recommendation_name
        name_count = len(
            [rec for rec in recommendations if rec.recommendation_name == test_name]
        )
        response = self.client.get(
            BASE_URL, query_string=f"recommendation_name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["recommendation_name"], test_name)

    def test_query_by_type(self):
        """It should Query Recommendations by its type"""
        recommendations = self._create_recommendations(10)
        test_type = recommendations[0].type
        type_recs = [rec for rec in recommendations if rec.type == test_type]
        type_count = len(type_recs)
        logging.debug("Recommendation Type [%d] %s", type_count, type_recs)

        # test for available
        response = self.client.get(
            BASE_URL, query_string=f"type={quote_plus(test_type.name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), type_count)
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["type"], test_type.name)

    # ----------------------------------------------------------
    # TEST LIKE
    # ----------------------------------------------------------
    def test_like(self):
        """It should like a Recommendation"""
        recommendations = self._create_recommendations(1)
        rec = recommendations[0]
        response = self.client.put(f"{BASE_URL}/{rec.rec_id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{rec.rec_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["number_of_likes"], 1)

    def test_like_bad(self):
        """It should not like a Recommendation that does not exist"""
        response = self.client.put(f"{BASE_URL}/000/like")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_dislike(self):
        """It should dislike a Recommendation"""
        recommendations = self._create_recommendations(1)
        rec = recommendations[0]
        response = self.client.put(f"{BASE_URL}/{rec.rec_id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(f"{BASE_URL}/{rec.rec_id}/dislike")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{rec.rec_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["number_of_dislikes"], 1)

    def test_dislike_bad(self):
        """It should not dislike a Recommendation that does not exist"""
        response = self.client.put(f"{BASE_URL}/000/dislike")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_k8s_health(self):
        """Checking health of local k8s cluster"""
        response = self.client.get("/health")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, {"message": "OK", "status": 200})
