import albumentations
import cv2
import numpy as np

from abc import ABC, abstractmethod
from onnxruntime import InferenceSession
from src.config import ClassifierConfig
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

    def __init__(self, config: ClassifierConfig) -> None:
        self._config = config
        self._model = InferenceSession(path_or_bytes=config.get('onnx_path'), providers=[config.get('provider')])
        self._transform = albumentations.Compose([
            albumentations.Resize(height=config.get('height'), width=config.get('width')),
            albumentations.Normalize(),
        ])

    def predict(self, image: np.ndarray) -> List[str]:
        return self._postprocess_predict(self._predict(self._preprocess(image)))

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        return self._postprocess_predict_proba(self._predict(self._preprocess(image)))

    @property
    def labels(self) -> List[str]:
        return self._config.get('labels')

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
        image = self._transform(image=image)
        return image['image'][np.newaxis, :, :, :].transpose(0, 3, 1, 2)

    def _predict(self, image: np.ndarray) -> np.ndarray:
        return self._model.run(output_names=None, input_feed={'input': image})[0].ravel()

    def _postprocess_predict(self, predict) -> List[str]:
        return [
            self._config.get('labels')[label_idx]
            for label_idx, proba in enumerate(predict)
            if proba > self._config.get('threshold')
        ]

    def _postprocess_predict_proba(self, predict) -> Dict[str, float]:
        return dict(zip(self._config.get('labels'), predict))
