import json
import unittest

import pytest
from requests import HTTPError

from bpmn_redrawer_backend.app import create_app
from bpmn_redrawer_backend.commons.utils import here
from unittest import mock

from bpmn_redrawer_backend.firebase.firebase import auth


@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client


@pytest.fixture
def token():
    yield auth.sign_in_with_email_and_password("test@test.it", "test00").get("idToken")


@unittest.SkipTest
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.download_image",
    return_value=here("../fixtures/img7.png"),
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.os.remove", return_value=None
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.store_bpmn_model",
    return_value="model_7",
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.database_service.store_conversion",
    return_value=None,
)
def test_post_conversion(mock_down, mock_rem, mock_bpmn, mock_conv, client):
    r = client.post("/api/v1/convert", json={"imagePath": "img7.png", "ocr": True})
    data = r.json
    # assert data.get("model_id").startswith("model_")
    # assert data.get("image_id") == "img7.png"
    assert data.get("xml")
    assert all(
        x in data.get("xml")
        for x in [
            "xml",
            "definitions",
            "participant",
            "processRef",
            "targetRef",
            "sourceRef",
            "bpmn:",
            "collaboration",
            "name",
            "id",
            "BPMNDiagram",
            "BPMNPlane",
            "BPMNShape",
            "x=",
            "y=",
            "width",
            "height",
            "bpmnElement",
            "dc:Bounds",
            "di:waypoint",
            "task",
            "Gateway",
        ]
    )


@unittest.SkipTest
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.download_image",
    return_value=here("../fixtures/img7.png"),
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.os.remove", return_value=None
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.store_bpmn_model",
    return_value="model_7",
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.database_service.store_conversion",
    return_value=None,
)
def test_post_conversion_token(
    mock_down, mock_rem, mock_bpmn, mock_conv, client, token
):
    r = client.post(
        "api/v1/convert",
        json={"imagePath": "img7.png", "ocr": True},
        headers={"Authorization": "Bearer {}".format(token)},
    )
    data = r.json
    assert data.get("model_id").startswith("model_")
    assert data.get("image_id") == "img7.png"
    assert data.get("xml")
    assert all(
        x in data.get("xml")
        for x in [
            "xml",
            "definitions",
            "participant",
            "processRef",
            "targetRef",
            "sourceRef",
            "bpmn:",
            "collaboration",
            "name",
            "id",
            "BPMNDiagram",
            "BPMNPlane",
            "BPMNShape",
            "x=",
            "y=",
            "width",
            "height",
            "bpmnElement",
            "dc:Bounds",
            "di:waypoint",
            "task",
            "Gateway",
        ]
    )


def http_error():
    http_err = HTTPError()
    http_err.strerror = json.dumps({"error": {"message": "Unauthorized", "code": 401}})
    return http_err


@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.download_image",
    return_value=here("../fixtures/img7.png"),
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.os.remove", return_value=None
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.storage_service.store_bpmn_model",
    side_effect=http_error(),
)
@mock.patch(
    "bpmn_redrawer_backend.api.services.database_service.store_conversion",
    side_effect=http_error(),
)
def test_post_conversion_error(
    mock_down, mock_rem, mock_bpmn, mock_conv, client, token
):
    r = client.post(
        "api/v1/convert",
        json={"imagePath": "img7.png", "ocr": True},
        headers={"Authorization": "Bearer {}".format(token)},
    )
    assert r.status_code == 401 and r.json.get("msg") == "Unauthorized"


def test_post_conversion_fail_img(client):
    r = client.post("api/v1/convert", json={"imagePath": "fail_img.png", "ocr": True})
    assert r.status_code == 404
