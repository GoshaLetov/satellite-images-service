import numpy as np

from abc import ABC, abstractmethod
from src.planet.services.classifier import PlanetImageClassifier
from src.planet.services.validator import PlanetImageValidator
from typing import Dict, List, Tuple


class BasePlanetImageClassifier(ABC):

    @abstractmethod
    def predict(self, image: np.ndarray) -> Tuple[bool, List[str]]:
        ...

    @abstractmethod
    def predict_proba(self, image: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        ...

    @property
    @abstractmethod
    def labels(self) -> List[str]:
        ...


class PlanetImageAnalytics(BasePlanetImageClassifier):
    def __init__(self, classifier: PlanetImageClassifier, validator: PlanetImageValidator) -> None:
        self._classifier = classifier
        self._validator = validator

    def predict(self, image: np.ndarray) -> Tuple[bool, List[str]]:
        is_image_valid = self._validator.is_image_valid(image=image)

        if is_image_valid:
            image_labels = self._classifier.predict(image=image)
        else:
            image_labels = []

        return is_image_valid, image_labels

    def predict_proba(self, image: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        is_image_valid = self._validator.is_image_valid(image=image)

        if is_image_valid:
            image_labels_probas = self._classifier.predict_proba(image=image)
        else:
            image_labels_probas = {}

        return is_image_valid, image_labels_probas

    @property
    def labels(self) -> List[str]:
        return self._classifier.labels
