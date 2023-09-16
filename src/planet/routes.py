import cv2
import numpy as np

from fastapi import APIRouter, Depends, File
from dependency_injector.wiring import Provide, inject
from src.planet.container import Container
from src.planet.services import PlanetImageClassifier, Service
from src.planet.schemas import LabelsOutput, PredictOutput, PredictProbaOutput

router = APIRouter(prefix='/planet', tags=['planet'])


def _bytes2image(image: bytes):
    return cv2.imdecode(buf=np.frombuffer(buffer=image, dtype=np.uint8), flags=cv2.IMREAD_COLOR)


@router.get(path='/labels')
@inject
def labels(
    classifier: PlanetImageClassifier = Depends(Provide[Container.classifier]),
) -> LabelsOutput:
    return LabelsOutput(labels=classifier.labels)


@router.post(path='/predict')
@inject
def predict(image: bytes = File(), service: Service = Depends(Provide[Container.service])) -> PredictOutput:
    image = _bytes2image(image=image)
    is_valid, image_labels = service.predict(image=image)
    return PredictOutput(is_valid=is_valid, labels=image_labels)


@router.post(path='/predict_proba')
@inject
def predict_proba(image: bytes = File(), service: Service = Depends(Provide[Container.service])) -> PredictProbaOutput:
    image = _bytes2image(image=image)
    is_valid, image_labels_probas = service.predict_proba(image=image)
    return PredictProbaOutput(is_valid=is_valid, probas=image_labels_probas)
