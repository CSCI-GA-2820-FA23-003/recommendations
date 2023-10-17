"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest
from service.models import DataValidationError, db, Recommendation, RecommendationType
from tests.factories import RecommendationFactory


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
        self.assertEqual(data["source_pid"], fake_rec.source_pid)
        self.assertEqual(data["name"], fake_rec.name)
        self.assertEqual(data["recommendation_id"], fake_rec.recommendation_id)
        self.assertEqual(data["recommendation_name"], fake_rec.recommendation_name)
        self.assertEqual(data["type"], fake_rec.type.name)
        self.assertEqual(data["number_of_likes"], fake_rec.number_of_likes)
        self.assertEqual(data["number_of_dislikes"], fake_rec.number_of_dislikes)

    def test_deserialize(self):
        """It should de-serialize a recommendation"""
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()
        recommendation = Recommendation().deserialize(data)  #####
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.id, data["id"])
        self.assertEqual(recommendation.source_pid, data["source_pid"])
        self.assertEqual(recommendation.name, data["name"])
        self.assertEqual(recommendation.recommendation_id, data["recommendation_id"])
        self.assertEqual(
            recommendation.recommendation_name, data["recommendation_name"]
        )
        self.assertEqual(recommendation.type, RecommendationType[data["type"]])
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

    def test_find(self):
        """It should find a recommendation by id"""
        target = RecommendationFactory()
        target.create()

        self.assertEqual = (
            Recommendation.find(target.id),
            target.id,
            "find result unmatch",
        )

    def test_update(self):
        target = RecommendationFactory()
        target.create()

        new_source_pid = 312
        target.source_pid = new_source_pid
        target.update()

        fetched_target = Recommendation.find(target.id)
        self.assertEqual(fetched_target.source_pid, new_source_pid)
