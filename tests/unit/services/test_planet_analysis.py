import copy
import numpy as np

from src.planet import Container
from src.planet.services import FakePlanetImageClassifier, FakePlanetImageValidator


def test_predicts_not_fail(planet_container: Container, sample_image_numpy: np.ndarray):
    with planet_container.reset_singletons():
        with planet_container.classifier.override(FakePlanetImageClassifier()), \
                planet_container.validator.override(FakePlanetImageValidator()):
            analytics = planet_container.analytics()
            analytics.predict(image=sample_image_numpy)
            analytics.predict_proba(image=sample_image_numpy)


def test_prob_less_or_equal_to_one(planet_container: Container, sample_image_numpy: np.ndarray):
    with planet_container.reset_singletons():
        with planet_container.classifier.override(FakePlanetImageClassifier()), \
                planet_container.validator.override(FakePlanetImageValidator()):
            analytics = planet_container.analytics()
            is_image_valid, genre2prob = analytics.predict_proba(image=sample_image_numpy)
            for prob in genre2prob.values():
                assert prob <= 1
                assert prob >= 0
            assert isinstance(is_image_valid, bool)


def test_predict_dont_mutate_initial_image(planet_container: Container, sample_image_numpy: np.ndarray):
    with planet_container.reset_singletons():
        with planet_container.classifier.override(FakePlanetImageClassifier()), \
                planet_container.validator.override(FakePlanetImageValidator()):
            analytics = planet_container.analytics()

            initial_image = copy.deepcopy(sample_image_numpy)
            analytics.predict(image=sample_image_numpy)

            assert np.allclose(initial_image, sample_image_numpy)
