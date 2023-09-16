import numpy as np
from src.planet.services.classifier import PlanetImageClassifier
from src.planet.services.validator import PlanetImageValidator
from typing import Dict, List, Tuple


class Service:
    def __init__(self, classifier: PlanetImageClassifier, validator: PlanetImageValidator) -> None:
        self._classifier = classifier
        self._validator = validator

    def predict(self, image: np.ndarray) -> Tuple[bool, List[str]]:
        is_valid = self._validator.is_image_valid(image=image)

        if is_valid:
            image_labels = self._classifier.predict(image=image)
        else:
            image_labels = []

        return is_valid, image_labels

    def predict_proba(self, image: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        is_valid = self._validator.is_image_valid(image=image)

        if is_valid:
            image_labels_probas = self._classifier.predict_proba(image=image)
        else:
            image_labels_probas = {}

        return is_valid, image_labels_probas
