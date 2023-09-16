import albumentations
import cv2
import numpy as np

from abc import ABC, abstractmethod
from onnxruntime import InferenceSession
from src.planet import Config
from typing import Dict, List


class PlanetImageClassifier(ABC):

    @abstractmethod
    def predict(self, image: np.ndarray) -> List[str]:
        ...

    @abstractmethod
    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        ...

    @property
    @abstractmethod
    def labels(self) -> List[str]:
        ...


class ONNXPlanetImageClassifier(PlanetImageClassifier):

    def __init__(self, config: Config) -> None:
        self._model = InferenceSession(path_or_bytes=config.onnx_path, providers=[config.provider])
        self._width = config.width
        self._height = config.height
        self._labels = config.labels
        self._threshold = config.threshold
        self._transform = albumentations.Compose([
            albumentations.Resize(height=config.height, width=config.width),
            albumentations.Normalize(),
        ])

    def predict(self, image: np.ndarray) -> List[str]:
        return self._postprocess_predict(self._predict(self._preprocess(image)))

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        return self._postprocess_predict_proba(self._predict(self._preprocess(image)))

    @property
    def labels(self) -> List[str]:
        return self._labels

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
        image = self._transform(image=image)
        return image['image'][np.newaxis, :, :, :].transpose(0, 3, 1, 2)

    def _predict(self, image: np.ndarray) -> np.ndarray:
        return self._model.run(output_names=None, input_feed={'input': image})[0].ravel()

    def _postprocess_predict(self, predict) -> List[str]:
        return [self._labels[label_idx] for label_idx, proba in enumerate(predict) if proba > self._threshold]

    def _postprocess_predict_proba(self, predict) -> Dict[str, float]:
        return {label: proba for label, proba in zip(self._labels, predict)}


class FakePlanetImageClassifier(PlanetImageClassifier):

    def __init__(self, config: Config) -> None:
        ...

    def predict(self, image: np.ndarray) -> List[str]:
        return ['label']

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        return {'label': 0.6}

    @property
    def labels(self) -> List[str]:
        return ['label']
