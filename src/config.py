from omegaconf import OmegaConf
from pydantic import BaseModel
from typing import List


class ClassifierConfig(BaseModel):
    onnx_path: str
    provider: str
    width: int
    height: int
    threshold: float
    labels: List[str]

    @classmethod
    def from_yaml(cls, path: str) -> 'ClassifierConfig':
        cfg = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**cfg)
