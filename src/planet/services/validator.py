import numpy as np
from abc import ABC, abstractmethod
from src.planet import Config


class PlanetImageValidator(ABC):

    @abstractmethod
    def is_image_valid(self, image: np.ndarray) -> bool:
        ...


class ONNXPlanetImageValidator(PlanetImageValidator):

    def __init__(self, config: Config) -> None:
        ...

    def is_image_valid(self, image: np.ndarray) -> bool:
        return True


class FakePlanetImageValidator(PlanetImageValidator):

    def is_image_valid(self, image: np.ndarray) -> bool:
        return True
