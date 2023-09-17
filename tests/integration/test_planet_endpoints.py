from fastapi.testclient import TestClient
from http import HTTPStatus


def test_labels_list(client: TestClient) -> None:
    response = client.get('/planet/labels')
    assert response.status_code == HTTPStatus.OK

    genres = response.json().get('labels')
    assert isinstance(genres, list)


def test_predict(client: TestClient, sample_image_bytes: bytes) -> None:
    files = {'image': sample_image_bytes}

    response = client.post(url='/planet/predict', files=files)
    assert response.status_code == HTTPStatus.OK

    predicted_genres = response.json().get('labels')
    assert isinstance(predicted_genres, list)


def test_predict_proba(client: TestClient, sample_image_bytes: bytes):
    files = {'image': sample_image_bytes}

    response = client.post(url='/planet/predict_proba', files=files)
    assert response.status_code == HTTPStatus.OK

    image_labels_probas = response.json().get('probas')
    assert isinstance(image_labels_probas, dict)

    for genre_prob in image_labels_probas.values():
        assert genre_prob <= 1
        assert genre_prob >= 0
