"""
Recommendation Service


Our recommendation service creates, lists, updates, deletes,

likes, and dislikes a recommendation for a product.

"""

# Import Flask application
from flask import jsonify, abort, make_response
from flask_restx import (
    Resource,
    fields,
    reqparse,
)
from flask_sqlalchemy import SQLAlchemy
from service.common import status  # HTTP Status Codes
from service.models import Recommendation, RecommendationType
from . import app, api

db = SQLAlchemy()


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="OK"), status.HTTP_200_OK)


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    """Index page"""
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Recommendation",
    {
        "source_pid": fields.Integer(
            required=True, description="The id of the associated product"
        ),
        "name": fields.String(
            required=True, description="The name of the associated product"
        ),
        "recommendation_name": fields.String(
            required=True, description="The name of the Recommendation"
        ),
        # pylint: disable=protected-access
        "type": fields.String(
            enum=RecommendationType._member_names_,
            description="The type of the Recommendation",
        ),
        "number_of_likes": fields.Integer(
            required=False, description="The number of likes of the Recommendation"
        ),
        "number_of_dislikes": fields.Integer(
            required=False, description="The number of dislikes"
        ),
    },
)

rec_model = api.inherit(
    "RecommendationModel",
    create_model,
    {
        "rec_id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
rec_args = reqparse.RequestParser()
rec_args.add_argument(
    "name",
    type=str,
    location="args",
    required=False,
    help="List Recommendations by their source product name",
)
rec_args.add_argument(
    "source_pid",
    type=int,
    location="args",
    required=False,
    help="List Recommendations by their source product id",
)
rec_args.add_argument(
    "recommendation_name",
    type=str,
    location="args",
    required=False,
    help="List Recommendations by its name",
)
rec_args.add_argument(
    "type",
    type=str,
    location="args",
    required=False,
    help="List Recommendations by its type",
)


######################################################################
#  PATH: /recommendations/{id}
######################################################################
@api.route("/recommendations/<rec_id>")
@api.param(
    "rec_id", "The Recommendation identifier"
)  # this is just in here for the docs.
class RecommendationResource(Resource):
    """
    RecommendationResource class

    Allows the manipulation of a single Recommendation
    GET /rec{id} - Returns a Recommendation with the id
    PUT /rec{id} - Update a Recommendation with the id
    DELETE /rec{id} -  Deletes a Recommendation with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc("get_recs")
    @api.response(404, "Recommendation not found")
    @api.marshal_with(rec_model)
    def get(self, rec_id):
        """This will retrieve a single recommendation based on its id"""
        app.logger.info("Request for recommendation with id [%s]", rec_id)
        recommendation = Recommendation.find(rec_id)
        if not recommendation:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Recommendation with id '{rec_id}' was not found.",
            )

        app.logger.info(
            "Returning recommendation: %s", recommendation.recommendation_name
        )

        return recommendation.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc("update_recs")
    @api.response(404, "Recommendation not found")
    @api.response(400, "The posted Recommendation data was not valid")
    @api.expect(rec_model)
    @api.marshal_with(rec_model)
    def put(self, rec_id):
        """This will update a recommendation given a recommendation id"""
        app.logger.info("Update a recommendation with id: %s", rec_id)
        recommendation = Recommendation.find(rec_id)
        if recommendation is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Recommendation with id '{rec_id}' does not exist",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        recommendation.deserialize(data)
        recommendation.rec_id = rec_id
        recommendation.update()
        return recommendation.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc("delete_recs")
    @api.response(204, "Recommendation deleted")
    def delete(self, rec_id):
        """This will delete a recommendation based on a given recommendation id"""
        app.logger.info("Delete a recommendation with id: %s", rec_id)

        recommendation = Recommendation.find(rec_id)

        # If it exists delete it, if not delete is unsuccessful
        if recommendation:
            recommendation.delete()
            app.logger.info("Recommendation with id [%s] was deleted", rec_id)

        # Delete always returns 204
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /recommendations
######################################################################
@api.route("/recommendations", strict_slashes=False)
class RecommendationCollection(Resource):
    """Handles all interactions with collections of Recommendations"""

    # ------------------------------------------------------------------
    # LIST ALL RECOMMENDATIONS
    # ------------------------------------------------------------------
    @api.doc("list_recs")
    @api.expect(rec_args, validate=True)
    @api.marshal_list_with(rec_model)
    def get(self):  # this was list_all
        """This will list all recommendations in the database.
        Returns: a list of recommendations
        """
        app.logger.info("Request to list all recommendations...")

        recommendations = []
        args = rec_args.parse_args()

        if args["name"]:
            app.logger.info("Find by source product name: %s", args["name"])
            recommendations = Recommendation.find_by_name(args["name"])
        elif args["source_pid"]:
            app.logger.info("Find by source product id: %s", args["source_pid"])
            recommendations = Recommendation.find_by_source_pid(args["source_pid"])
        elif args["recommendation_name"]:
            app.logger.info(
                "Find by recommendation name: %s", args["recommendation_name"]
            )
            recommendations = Recommendation.find_by_rec_name(
                args["recommendation_name"]
            )
        elif args["type"]:
            app.logger.info("Find by type: %s", args["type"])
            # create enum from string
            type_value = getattr(RecommendationType, args["type"].upper())
            recommendations = Recommendation.find_by_type(type_value)
        else:
            app.logger.info("Find all")
            recommendations = Recommendation.all()

        results = [recommendation.serialize() for recommendation in recommendations]

        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # CREATE A NEW RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc("create_recs")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(rec_model, code=201)
    def post(self):
        """This creates a new recommendation and stores it in the database"""

        app.logger.info("Request to Create a Recommendation...")
        recommendation = Recommendation()
        app.logger.debug("Payload = %s", api.payload)
        recommendation.deserialize(api.payload)
        recommendation.create()
        app.logger.info("Recommendation with new id [%s] saved!", recommendation.rec_id)

        location_url = api.url_for(
            RecommendationResource, rec_id=recommendation.rec_id, _external=True
        )

        return (
            recommendation.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )


######################################################################
#  PATH: /recommendations/{id}/like
######################################################################
@api.route("/recommendations/<rec_id>/like")
@api.param("rec_id", "The Recommendation identifier")
class LikeResource(Resource):
    """Like actions on a Recommendation"""

    @api.doc("like_recommendations")
    @api.response(200, "Action recorded")
    @api.response(404, "Recommendation not found")
    def put(self, rec_id):
        """Liking a Recommendation increments its like count"""
        app.logger.info("Request to Like a Recommendation")
        recommendation = Recommendation.find(rec_id)
        if not recommendation:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"recommendation with id '{rec_id}' was not found.",
            )
        recommendation.number_of_likes += 1
        recommendation.update()
        app.logger.info(
            "Recommendation with id [%s] has been liked!", recommendation.rec_id
        )
        return recommendation.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /recommendations/{id}/dislike
######################################################################
@api.route("/recommendations/<rec_id>/dislike")
@api.param("rec_id", "The Recommendation identifier")
class DislikeResource(Resource):
    """Dislike actions on a Recommendation"""

    @api.doc("dislike_recommendations")
    @api.response(200, "Action recorded")
    @api.response(404, "Recommendation not found")
    def put(self, rec_id):
        """Disliking a Recommendation decrements its like count"""
        app.logger.info("Request to Dislike a Recommendation")
        recommendation = Recommendation.find(rec_id)
        if not recommendation:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"recommendation with id '{rec_id}' was not found.",
            )
        recommendation.number_of_dislikes += 1
        recommendation.update()
        app.logger.info(
            "Recommendation with id [%s] has been disliked!", recommendation.rec_id
        )
        return recommendation.serialize(), status.HTTP_200_OK
