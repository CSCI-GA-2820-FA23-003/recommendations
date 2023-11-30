######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Recommendation Steps

Steps file for recommendations.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given  # pylint: disable=no-name-in-module
from compare import expect
from enum import Enum

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


class RecommendationType(Enum):
    CROSSSELL = 0
    UPSELL = 1
    ACCESSORY = 2


@given("the following recommendations")
def step_impl(context):
    """Delete all Recommendations and load new ones"""

    # List all of the recommendations and delete them one by one
    rest_endpoint = f"{context.base_url}/recommendations"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for rec in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{rec['rec_id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new recommendations
    for row in context.table:
        payload = {
            "rec_id": row["rec_id"],
            "source_pid": row["source_pid"],
            "name": row["name"],
            "recommendation_name": row["recommendation_name"],
            "type": row["type"].upper(),
            "number_of_likes": row["number_of_likes"],
            "number_of_dislikes": row["number_of_dislikes"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        print("working3")
        expect(context.resp.status_code).to_equal(201)
        print("working4")
