import pytest

from spm2021_ram_backend.bpmn.predictions import (
    ObjectPrediction,
    KeyPointPrediction,
)
from spm2021_ram_backend.api.services import predict_service as ps
from spm2021_ram_backend.api.services.storage_service import get_ocr_and_predict_images
from unittest import mock

from spm2021_ram_backend.commons.utils import here


@pytest.fixture
@mock.patch(
    "spm2021_ram_backend.api.services.storage_service.download_image",
    return_value=here("../fixtures/img_test.png"),
)
@mock.patch(
    "spm2021_ram_backend.api.services.storage_service.os.remove", return_value=None
)
def image(mock_down, mock_rem):
    return get_ocr_and_predict_images("img_test.png", None)


def test_object_prediction(image):
    predictions = ps.predict_object(image[1])
    assert predictions
    assert all(isinstance(p, ObjectPrediction) for p in predictions)


def test_keypoint_prediction(image):
    predictions = ps.predict_keypoint(image[0])
    assert predictions
    assert all(isinstance(p, KeyPointPrediction) for p in predictions)
