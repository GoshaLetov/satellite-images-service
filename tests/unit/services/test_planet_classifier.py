import copy
import numpy as np

from src.planet import Container


def test_predicts_not_fail(planet_container: Container, sample_image_numpy: np.ndarray):
    classifier = planet_container.classifier()
    classifier.predict(image=sample_image_numpy)
    classifier.predict_proba(image=sample_image_numpy)


def test_prob_less_or_equal_to_one(planet_container: Container, sample_image_numpy: np.ndarray):
    classifier = planet_container.classifier()
    planet2prob = classifier.predict_proba(image=sample_image_numpy)
    for prob in planet2prob.values():
        assert prob <= 1
        assert prob >= 0


def test_predict_dont_mutate_initial_image(planet_container: Container, sample_image_numpy: np.ndarray):
    classifier = planet_container.classifier()

    initial_image = copy.deepcopy(sample_image_numpy)
    classifier.predict(image=sample_image_numpy)

    assert np.allclose(initial_image, sample_image_numpy)
