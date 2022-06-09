import pytest
from cv2 import cv2

from bpmn_redrawer_backend.bpmn.bpmn_elements import Participant, Task
from bpmn_redrawer_backend.bpmn.predictions import Text, ObjectPrediction
from bpmn_redrawer_backend.api.services import ocr_service as os
from bpmn_redrawer_backend.commons.utils import here


@pytest.fixture
def text():
    text = [
        Text("prova", *[186, 35, 27, 9]),
        Text("task", *[218, 33, 23, 9]),
        Text("con", *[245, 35, 18, 7]),
        Text("due", *[200, 48, 19, 9]),
        Text("linee", *[224, 48, 25, 9]),
        Text("start", *[14, 73, 21, 8]),
    ]
    yield text


@pytest.fixture
def elements():
    elements = []

    texts = [
        Text("prova", *[25, 50, 10, 20]),
        Text("task", *[75, 75, 10, 5]),
        Text("con", *[80, 80, 10, 5]),
    ]

    part = Participant("p1", ObjectPrediction(0, 20, 20, 100, 100), None)
    task = Task("task", ObjectPrediction(1, 70, 70, 90, 90), "task")
    elements.append(part)
    elements.append(task)

    yield elements, texts


def test_get_text_from_img(text):
    image = cv2.imread(here("../fixtures/img.png"), cv2.IMREAD_UNCHANGED)
    txt = os.get_text_from_img(image)
    assert txt == text


def test_link_text(elements):
    elements = os.link_text(elements[1], elements[0])
    assert [txt.text for txt in elements[0].name] == ["prova"]
    assert [txt.text for txt in elements[1].name] == ["task", "con"]
