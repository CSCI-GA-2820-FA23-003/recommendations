"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Recommendation

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

@app.route("/recommendation/<int:id>", methods=['GET'])

def read(id):
    app.logger.info(f"Read the recommendation with ID: {id}")
    recommendation = Recommendation.find(id)

    if recommendation is None:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with ID {id} does not exist")

    #if the recommendation is a list of recomendation relation
    if isinstance(recommendation, list):
        output = []
        for r in recommendation:
            output.append({
                "recommendation id": r.recommendation_id,
                "recommendation name": r.recommendation_name,
                "type":str(r.type),
                'number of likes':r.number_of_likes,
                "number of dislikes":r.number_of_dislikes
            })
        return output
    else:
        
        output=[{
                "recommendation id": recommendation.recommendation_id,
                "recommendation name": recommendation.recommendation_name,
                "type":str(recommendation.type),
                'number of likes':recommendation.number_of_likes,
                "number of dislikes":recommendation.number_of_dislikes
            }]
        return output
    
