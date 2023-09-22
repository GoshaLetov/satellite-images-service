from dependency_injector import containers, providers
from src.planet.services import ONNXPlanetImageClassifier


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    classifier = providers.Singleton(ONNXPlanetImageClassifier, config=config)
