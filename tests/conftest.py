import cv2
import pytest

from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src import planet
from src.config import ClassifierConfig

TESTS_DIR = Path(__file__).parent


@pytest.fixture(scope='function')
def sample_image_bytes():
    with open(TESTS_DIR / 'images' / 'sample.jpg', 'rb') as image:
        yield image


@pytest.fixture
def sample_image_numpy():
    return cv2.cvtColor(
        src=cv2.imread(filename=str(TESTS_DIR / 'images' / 'sample.jpg')),
        code=cv2.COLOR_BGR2RGB,
    )


@pytest.fixture(scope='session')
def app_config():
    return ClassifierConfig.from_yaml(path='src/config.yaml')


@pytest.fixture
def planet_container(app_config):
    container = planet.Container()
    container.config.from_dict(options=app_config)
    return container


@pytest.fixture
def wired_planet_container(app_config):
    container = planet.Container()
    container.config.from_dict(app_config)
    container.wire([planet.routes])
    yield container
    container.unwire()


@pytest.fixture
def test_app(wired_planet_container):
    app = FastAPI()
    app.include_router(router=planet.router)
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
