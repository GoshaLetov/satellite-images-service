from dependency_injector import containers, providers
from src.planet.services import (
    ONNXPlanetImageClassifier,
    ONNXPlanetImageValidator,
    Service,
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    classifier = providers.Singleton(
        ONNXPlanetImageClassifier,
        config=config.planet
    )

    validator = providers.Singleton(
        ONNXPlanetImageValidator,
        config=config.planet
    )

    service = providers.Singleton(
        Service,
        classifier=classifier,
        validator=validator,
    )
