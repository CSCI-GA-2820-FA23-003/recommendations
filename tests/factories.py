import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """It creates a fake recommendation for testing"""

    class Meta:
        model = Recommendation

    id = factory.Sequence(lambda n: n)
    source_pid = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    recommendation_name = factory.Faker("name")
    type = FuzzyChoice(
        choices=[
            RecommendationType.UPSELL,
            RecommendationType.CROSSSELL,
            RecommendationType.ACCESSORY,
        ]
    )
    number_of_likes = 0
    number_of_dislikes = 0
