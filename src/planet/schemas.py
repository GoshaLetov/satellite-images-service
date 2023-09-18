from pydantic import BaseModel
from typing import Dict, List


class LabelsOutput(BaseModel):
    labels: List[str]


class PredictOutput(BaseModel):
    is_image_valid: bool
    labels: List[str]


class PredictProbaOutput(BaseModel):
    is_image_valid: bool
    probas: Dict[str, float]
