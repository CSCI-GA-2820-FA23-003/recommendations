"""
My Service

Describe what your service does here
"""

# Import Flask application
from flask import jsonify, request, abort, url_for, make_response
from . import app
from service.common import status  # HTTP Status Codes
from service.models import Recommendation, RecommendationType
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="OK"), status.HTTP_200_OK)


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


######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_all():
    """This will list all recommendations in the database.
    Returns: a list of recommendations
    """
    app.logger.info("Request to list all recommendations...")

    recommendations = []
    #id = request.args.get("id")
    source_pid = request.args.get("source_pid")
    name = request.args.get("name")
    recommendation_name = request.args.get("recommendation_name")
    type = request.args.get("type")

    if name:
        app.logger.info("Find by source name: %s", name)
        recommendations = Recommendation.find_by_name(name)
    elif source_pid:
        app.logger.info("Find by recommendation id: %s", source_pid)
        recommendations = Recommendation.find_by_source_pid(source_pid)
    elif recommendation_name:
        app.logger.info("Find by recommendation name: %s", recommendation_name)
        recommendations = Recommendation.find_by_rec_name(recommendation_name)
    elif type:
        app.logger.info("Find by type: %s", type)
        # create enum from string
        type_value = getattr(RecommendationType, type.upper())
        recommendations = Recommendation.find_by_type(type_value)
    else:
        app.logger.info("Find all")
        recommendations = Recommendation.all()

    results = [recommendation.serialize() for recommendation in recommendations]

    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>", methods=["GET"])
def get(id):
    """This will retrieve a single recommendation based on its id"""
    app.logger.info("Request for recommendation with id [%s]", id)
    recommendation = Recommendation.find(id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND, f"Recommendation with id '{id}' was not found."
        )

    app.logger.info("Returning recommendation: %s", recommendation.recommendation_name)

    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE A RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def post():
    """This creates a new recommendation and stores it in the database"""

    data = request.json

    recommendation = Recommendation()
    recommendation.deserialize(data)
    recommendation.create()

    location_url = url_for("get", id=recommendation.id, _external=True)

    return (
        recommendation.serialize(),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>", methods=["DELETE"])
def delete(id):
    """This will delete a recommendation based on a given recommendation id"""
    app.logger.info("Delete a recommendation with id: %s", id)

    recommendation = Recommendation.find(id)

    # If it exists delete it, if not delete is unsuccessful
    recommendation.delete()

    # Delete always returns 204
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# UPDATE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>", methods=["PUT"])
def put(id):
    """This will update a recommendation given a recommendation id"""
    app.logger.info("Update a recommendation with id: %s", id)
    recommendation = Recommendation.find(id)
    if recommendation is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{id}' does not exist",
        )
    data = request.json
    recommendation.deserialize(data)
    recommendation.update()

    return recommendation.serialize(), status.HTTP_200_OK


######################################################################
# LIKE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>/like", methods=["PUT"])
def like_recommendation(id):
    """Liking a Recommendation increments its like count"""
    recommendation = Recommendation.find(id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND, f"recommendation with id '{id}' was not found."
        )
    recommendation.number_of_likes += 1
    recommendation.update()
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)


######################################################################
# DISLIKE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>/dislike", methods=["PUT"])
def dislike_recommendation(id):
    """Disliking a Recommendation decrements its like count"""
    recommendation = Recommendation.find(id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND, f"recommendation with id '{id}' was not found."
        )
    recommendation.number_of_likes -= 1
    recommendation.update()
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)
