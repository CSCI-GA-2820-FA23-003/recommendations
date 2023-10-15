"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Recommendation, RecommendationType

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return {"status": status.HTTP_200_OK}
    # return (
    #     "Reminder: return some useful information in json format about the service here",
    #     status.HTTP_200_OK,
    # )


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

    return recommendation.serialize(), status.HTTP_200_OK
