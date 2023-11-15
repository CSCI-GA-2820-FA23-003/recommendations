"""
Test cases for Recommendations Model

"""
import unittest
from service.models import DataValidationError, Recommendation, RecommendationType
from tests.factories import RecommendationFactory


######################################################################
#  Recommendation  M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestRecommendationModel(unittest.TestCase):
    """Test Cases for Recommendation Model"""

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
        self.assertEqual(data["rec_id"], fake_rec.rec_id)
        self.assertEqual(data["source_pid"], fake_rec.source_pid)
        self.assertEqual(data["name"], fake_rec.name)
        self.assertEqual(data["recommendation_name"], fake_rec.recommendation_name)
        self.assertEqual(data["type"], fake_rec.type.name)
        self.assertEqual(data["number_of_likes"], fake_rec.number_of_likes)
        self.assertEqual(data["number_of_dislikes"], fake_rec.number_of_dislikes)

    def test_deserialize(self):
        """It should de-serialize a recommendation"""
        fake_rec = RecommendationFactory()
        data = fake_rec.serialize()
        recommendation = Recommendation().deserialize(data)
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.rec_id, data["rec_id"])
        self.assertEqual(recommendation.source_pid, data["source_pid"])
        self.assertEqual(recommendation.name, data["name"])
        self.assertEqual(
            recommendation.recommendation_name, data["recommendation_name"]
        )
        self.assertEqual(recommendation.type, RecommendationType[data["type"]])
        self.assertEqual(recommendation.number_of_likes, data["number_of_likes"])
        self.assertEqual(recommendation.number_of_dislikes, data["number_of_dislikes"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a recommendation with missing data"""
        data = {"rec_id": 0, "name": "cookie"}
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

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
        """It should find a recommendation by its id"""
        target = RecommendationFactory()
        target.create()
        fetched_target = Recommendation.find(target.rec_id)
        self.assertIsNot(fetched_target, None)
        self.assertEqual(fetched_target.rec_id, target.rec_id)

    def test_update(self):
        target = RecommendationFactory()
        target.create()

        new_source_pid = 312
        target.source_pid = new_source_pid
        target.update()

        fetched_target = Recommendation.find(target.rec_id)
        self.assertEqual(fetched_target.source_pid, new_source_pid)
