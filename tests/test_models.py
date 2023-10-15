"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest
from service.models import DataValidationError, db, Recommendation, RecommendationType
from tests.factories import RecommendationFactory

# def make_recommendation(
#     id,
#     name,
#     recommendation_id,
#     recommendation_name,
#     type,
#     number_of_likes,
#     number_of_dislikes,
# ):
#     "Generate a Recommendation by the given arguments"
#     rec = Recommendation()
#     rec.id = id
#     rec.name = name
#     rec.recommendation_id = recommendation_id
#     rec.recommendation_name = recommendation_name
#     rec.type = type
#     rec.number_of_likes = number_of_likes
#     rec.number_of_dislikes = number_of_dislikes
#     return rec


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceModel(unittest.TestCase):
    """Test Cases for YourResourceModel Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""

    def tearDown(self):
        """This runs after each test"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_serialize(self):
        """It should serialize a recommendation"""
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()
        self.assertNotEqual(data, None)
        self.assertEqual(data["id"], fake_rec.id)
        self.assertEqual(data["name"], fake_rec.name)
        self.assertEqual(data["recommendation_id"], fake_rec.recommendation_id)
        self.assertEqual(data["recommendation_name"], fake_rec.recommendation_name)
        self.assertEqual(data["type"], fake_rec.type)
        self.assertEqual(data["number_of_likes"], fake_rec.number_of_likes)
        self.assertEqual(data["number_of_dislikes"], fake_rec.number_of_dislikes)

    def test_deserialize(self):
        """It should de-serialize a recommendation"""
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()
        recommendation = Recommendation().deserialize(data)  #####
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.id, data["id"])
        self.assertEqual(recommendation.name, data["name"])
        self.assertEqual(recommendation.recommendation_id, data["recommendation_id"])
        self.assertEqual(
            recommendation.recommendation_name, data["recommendation_name"]
        )
        self.assertEqual(recommendation.type, data["type"])
        self.assertEqual(recommendation.number_of_likes, data["number_of_likes"])
        self.assertEqual(recommendation.number_of_dislikes, data["number_of_dislikes"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a recommendation with missing data"""
        data = {"id": 0, "name": "cookie"}
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)  ###

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "bad data"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_type(self):
        """It should not deserialize data with bad recommendation type"""
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()
        data["type"] = "hello"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)
