"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
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

# def delete(name):
#    app.logger.info("Delete a recommendation on the list")
#    
#    recommendation = Recommendation.find(name)
#    
    # If it exists delete it, if not delete is unsuccessful
#    if recommendation is None:
#        abort(status.HTTP_404_NOT_FOUND, "Recommendation {name} does not exist")
    
#    recommendation.delete()
    
    # Delete always returns 204
#    return "", status.HTTP_204_NO_CONTENT
