from pydantic import BaseModel
from typing import List


class Config(BaseModel):
    onnx_path: str
    provider: str
    width: int
    height: int
    threshold: float
    labels: List[str]
