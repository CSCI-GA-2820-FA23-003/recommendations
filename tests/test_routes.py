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
from service.models import db, Recommendation, init_db
from service.common import status  # HTTP Status Codes
from tests.factories import RecommendationFactory


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        """ It should delete a recommendation on the list """
        target = RecommendationFactory()
        target.create()
        resp = self.client.post(
            "/recommendations", json = recommendation.serialize()
            )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, "create success")

        recommendation = resp.get_json()

        self.assertEqual = (Recommendation.all(), [], "delete unsuccessful")
        recommendation.delete()
        self.assertEqual = (Recommendation.all(), [], "delete success")
