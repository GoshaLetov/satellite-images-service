from omegaconf import OmegaConf
from pydantic import BaseModel

from src import planet


class ServiceConfig(BaseModel):
    planet: planet.Config

    @classmethod
    def from_yaml(cls, path: str) -> 'ServiceConfig':
        cfg = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**cfg)
