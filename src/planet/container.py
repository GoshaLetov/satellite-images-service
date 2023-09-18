from dependency_injector import containers, providers
from src.planet.services import (
    ONNXPlanetImageClassifier,
    ONNXPlanetImageValidator,
    PlanetImageAnalytics,
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    classifier = providers.Singleton(
        ONNXPlanetImageClassifier,
        config=config.planet,
    )

    validator = providers.Singleton(
        ONNXPlanetImageValidator,
        config=config.planet,
    )

    analytics = providers.Singleton(
        PlanetImageAnalytics,
        classifier=classifier,
        validator=validator,
    )
