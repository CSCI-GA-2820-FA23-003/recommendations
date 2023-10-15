"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Recommendation.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class RecommendationType(Enum):
    """Enumeration of valid Recommendation types"""

    CROSSSELL = 0
    UPSELL = 1
    ACCESSORY = 2


class Recommendation(db.Model):
    """
    Class that represents a YourResourceModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    recommendation_id = db.Column(db.Integer)
    recommendation_name = db.Column(db.String(63))
    type = db.Column(
        db.Enum(RecommendationType),
        nullable=False,
        default=RecommendationType.CROSSSELL,
    )
    number_of_likes = db.Column(db.Integer, default=0)
    number_of_dislikes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<YourResourceModel {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a YourResourceModel from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Recommendation into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "recommendation_id": self.recommendation_id,
            "recommendation_name": self.recommendation_name,
            "type": self.type.value,
            "number_of_likes": self.number_of_likes,
            "number_of_dislikes": self.number_of_dislikes,
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.id = data["id"]
            self.recommendation_id = data["recommendation_id"]
            self.recommendation_name = data["recommendation_name"]
            if "type" not in data or data["type"] is None:
                self.type = RecommendationType.CROSSSELL
            else:
                self.type = RecommendationType[data["type"]]
                if not isinstance(self.type, RecommendationType):
                    raise DataValidationError(
                        "invalid type for Recommendation Type:" + str(type(self.type))
                    )
            self.number_of_likes = data["number_of_likes"]
            self.number_of_dislikes = data["number_of_dislikes"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Recommendation: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            ) from error
        except ValueError as error:
            raise DataValidationError("Invalid value: " + error.args[0]) from error
        except AttributeError as error:
            raise DataValidationError("Invalid attribute " + error.args[0]) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the YourResourceModels in the database"""
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a YourResourceModel by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
