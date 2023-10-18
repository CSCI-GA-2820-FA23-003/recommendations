"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort, make_response
from service.common import status  # HTTP Status Codes
from service.models import Recommendation, RecommendationType
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...


@app.route("/recommendation", methods=["POST"])
def post():
    """Root URL response"""
    data = request.json

    recommendation = Recommendation()
    recommendation.deserialize(data)
    recommendation.create()

    return recommendation.serialize(), status.HTTP_201_CREATED


@app.route("/recommendation/<int:id>", methods=["DELETE"])
def delete(id):
    """This will delete a recommendation based on a given recommendation id"""
    app.logger.info("Delete a recommendation with id: %s", id)

    recommendation = Recommendation.find(id)

    # If it exists delete it, if not delete is unsuccessful
    if recommendation is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            "Recommendation {id} does not exist",
        )
    if recommendation:
        recommendation.delete()

    # Delete always returns 204
    return "", status.HTTP_204_NO_CONTENT


@app.route("/recommendation/<int:id>", methods=["PUT"])
def put(id):
    """This will update a recommendation given a recommendation id"""
    app.logger.info("Update a recommendation with id: %s", id)
    recommendation = Recommendation.find(id)
    if recommendation is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            "Recommendation {id} does not exist",
        )
    data = request.json
    recommendation.deserialize(data)
    recommendation.update()

    return recommendation.serialize(), status.HTTP_200_OK


@app.route("/recommendation/list/<int:source_pid>", methods=["GET"])
def list(source_pid):
    """This will list all recommendations related to given source_pid."""
    app.logger.info("Request for Account list")
    recommendation = Recommendation.find_by_source_pid(source_pid)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, f"Related recommendation not found")
    # make_response([], status.HTTP_200_OK)
    return make_response([r.serialize() for r in recommendation], status.HTTP_200_OK)
