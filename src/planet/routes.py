import cv2
import numpy as np

from http import HTTPStatus
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from dependency_injector.wiring import Provide, inject
from src.planet.container import Container
from src.planet.services import PlanetImageClassifier
from src.planet.schemas import (
    PlanetClassifierLabelsOutput,
    PlanetClassifierPredictOutput,
    PlanetClassifierPredictProbaOutput,
)

router = APIRouter(prefix='/planet', tags=['planet'])


def _bytes2image(image: UploadFile):

    content_type = image.content_type
    if content_type not in {'image/jpeg', 'image/png'}:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Invalid file type')

    buffer = np.frombuffer(buffer=image.file.read(), dtype=np.uint8)

    return cv2.imdecode(buf=buffer, flags=cv2.IMREAD_COLOR)


@router.get(
    path='/labels',
    response_model=PlanetClassifierLabelsOutput,
    description='Return list of multilabel classification model`s labels',
)
@inject
def labels(
    classifier: PlanetImageClassifier = Depends(Provide[Container.classifier]),
) -> PlanetClassifierLabelsOutput:
    return PlanetClassifierLabelsOutput(labels=classifier.labels)


@router.post(
    path='/predict',
    response_model=PlanetClassifierPredictOutput,
    description='Run multilabel classification model on given image and return labels',
)
@inject
def predict(
    image: UploadFile = File(
        title='PlanetClassifierPredictInput',
        alias='image',
        description='Image for inference.',
    ),
    classifier: PlanetImageClassifier = Depends(Provide[Container.classifier]),
) -> PlanetClassifierPredictOutput:
    return PlanetClassifierPredictOutput(labels=classifier.predict(image=_bytes2image(image=image)))


@router.post(
    path='/predict_proba',
    response_model=PlanetClassifierPredictProbaOutput,
    description='Run multilabel classification model on given image and return probabilities of labels',
)
@inject
def predict_proba(
    image: UploadFile = File(
        title='PlanetClassifierPredictInput',
        alias='image',
        description='Image for inference.',
    ),
    classifier: PlanetImageClassifier = Depends(Provide[Container.classifier]),
) -> PlanetClassifierPredictProbaOutput:
    return PlanetClassifierPredictProbaOutput(probas=classifier.predict_proba(image=_bytes2image(image=image)))
