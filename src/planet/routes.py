import cv2
import numpy as np

from fastapi import APIRouter, Depends, File
from dependency_injector.wiring import Provide, inject
from src.planet.container import Container
from src.planet.services import PlanetImageAnalytics
from src.planet.schemas import LabelsOutput, PredictOutput, PredictProbaOutput

router = APIRouter(prefix='/planet', tags=['planet'])


def _bytes2image(image: bytes):
    buf = np.frombuffer(buffer=image, dtype=np.uint8)
    return cv2.imdecode(buf=buf, flags=cv2.IMREAD_COLOR)


@router.get(path='/labels')
@inject
def labels(
    analytics: PlanetImageAnalytics = Depends(Provide[Container.analytics]),
) -> LabelsOutput:
    return LabelsOutput(labels=analytics.labels)


@router.post(path='/predict')
@inject
def predict(
    image: bytes = File(),
    analytics: PlanetImageAnalytics = Depends(Provide[Container.analytics]),
) -> PredictOutput:
    is_image_valid, image_labels = analytics.predict(image=_bytes2image(image=image))
    return PredictOutput(is_image_valid=is_image_valid, labels=image_labels)


@router.post(path='/predict_proba')
@inject
def predict_proba(
    image: bytes = File(),
    analytics: PlanetImageAnalytics = Depends(Provide[Container.analytics]),
) -> PredictProbaOutput:
    is_image_valid, image_labels_probas = analytics.predict_proba(image=_bytes2image(image=image))
    return PredictProbaOutput(is_image_valid=is_image_valid, probas=image_labels_probas)
