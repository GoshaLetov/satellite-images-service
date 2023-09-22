from pydantic import BaseModel
from typing import Dict, List


class PlanetClassifierLabelsOutput(BaseModel):
    labels: List[str]


class PlanetClassifierPredictOutput(BaseModel):
    labels: List[str]


class PlanetClassifierPredictProbaOutput(BaseModel):
    probas: Dict[str, float]
