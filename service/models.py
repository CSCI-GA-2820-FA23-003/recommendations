"""
Models for Recommendation

All of the models are stored in this module
"""
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

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
    Class that represents a Recommendation
    """

    app = None

    # Table Schema
    rec_id = db.Column(db.Integer, primary_key=True)  # this is a recommendation ID
    source_pid = db.Column(db.db.Integer)  # this is a product ID
    name = db.Column(db.String(63))  # this is a product name
    recommendation_name = db.Column(db.String(63))  # this is a recommendation name
    type = db.Column(
        db.Enum(RecommendationType),
        nullable=False,
        server_default=(RecommendationType.CROSSSELL.name),
    )
    number_of_likes = db.Column(db.Integer, default=0)
    number_of_dislikes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Recommendation {self.recommendation_name} id=[{self.rec_id}]>"

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating %s", self.recommendation_name)
        self.rec_id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving %s", self.recommendation_name)
        db.session.commit()

    def delete(self):
        """Removes a Recommendation from the data store"""
        logger.info("Deleting %s", self.recommendation_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Recommendation into a dictionary"""
        return {
            "rec_id": self.rec_id,
            "source_pid": self.source_pid,
            "name": self.name,
            "recommendation_name": self.recommendation_name,
            "type": self.type.name,
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
            self.source_pid = data["source_pid"]
            self.recommendation_name = data["recommendation_name"]
            self.number_of_likes = data["number_of_likes"]
            self.number_of_dislikes = data["number_of_dislikes"]

            if "type" not in data or data["type"] is None:
                self.type = RecommendationType["CROSSSELL"]
            else:
                self.type = RecommendationType[data["type"]]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Recommendation: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            ) from error
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
        """Returns all of the Recommendations in the database"""
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, rec_id):
        """Finds a Recommendation by it's ID"""
        logger.info("Processing lookup for id %d ...", rec_id)
        return cls.query.get(rec_id)

    @classmethod
    def find_by_name(cls, name) -> list:
        """Returns all Recommendations with the name of an associated product

        Args:
            name (string): the name of the Recommendations you want to match
        """
        logger.info("Processing lookup for name %s...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_rec_name(cls, recommendation_name) -> list:
        """Returns all Recommendations with its name

        Args:
            name (string): the name of the Recommendations you want to match
        """
        logger.info("Processing lookup for name %s...", recommendation_name)
        return cls.query.filter(cls.recommendation_name == recommendation_name)

    @classmethod
    def find_by_source_pid(cls, source_pid) -> list:
        """Returns all Recommendations with the given source_pid
        Args:
            source_pid (integer): the source_pid of the Recommendations you want to match
        """
        logger.info("Processing lookup for source_pid %d...", source_pid)
        return cls.query.filter(cls.source_pid == source_pid)

    @classmethod
    def find_by_type(
        cls, rec_type: RecommendationType = RecommendationType.CROSSSELL
    ) -> list:
        """Returns all Recommendations by their type

        :param gender: values are ['CROSSSELL', 'UPSELL', 'ACCESSORY']
        :type available: enum

        :return: a collection of Recommendations of that type
        :rtype: list

        """
        logger.info("Processing lookup for type %s...", rec_type.name)
        return cls.query.filter(cls.type == rec_type)
