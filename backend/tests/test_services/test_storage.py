from bpmn_redrawer_backend.api.services import storage_service as fs
from bpmn_redrawer_backend.commons.utils import here
from unittest import mock


@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.download_image",
    return_value=here("../fixtures/img_test.png"),
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.os.remove", return_value=None
)
def test_get_images(mock_down, mock_rem):
    orc, predict = fs.get_ocr_and_predict_images("img_test.png", None)
    assert orc is not None
    assert predict is not None
    eq = orc == predict
    assert not eq.all()


@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.download_image",
    return_value="non_existing.png",
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.os.remove", return_value=None
)
def test_get_images_fail(mock_down, mock_rem):
    orc2, predict2 = fs.get_ocr_and_predict_images("non_existing.png", None)
    assert orc2 is None
    assert predict2 is None


@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.store_model",
    return_value="ok",
)
def test_store_model(mock_store):
    m = fs.store_bpmn_model("bpmn_str", "token")
    assert m is not None
    assert "model_" in m and ".bpmn" in m
