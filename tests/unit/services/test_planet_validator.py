import copy
import numpy as np

from src.planet import Container


def test_is_image_valid_not_fail(planet_container: Container, sample_image_numpy: np.ndarray):
    validator = planet_container.validator()
    validator.is_image_valid(image=sample_image_numpy)


def test_is_image_valid_type_bool(planet_container: Container, sample_image_numpy: np.ndarray):
    validator = planet_container.validator()
    is_image_valid = validator.is_image_valid(image=sample_image_numpy)

    assert isinstance(is_image_valid, bool)


def test_is_image_valid_dont_mutate_initial_image(planet_container: Container, sample_image_numpy: np.ndarray):
    validator = planet_container.validator()

    initial_image = copy.deepcopy(sample_image_numpy)
    validator.is_image_valid(image=sample_image_numpy)

    assert np.allclose(initial_image, sample_image_numpy)
