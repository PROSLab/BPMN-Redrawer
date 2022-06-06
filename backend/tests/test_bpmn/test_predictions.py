import pytest

from bpmn_redrawer_backend.bpmn.predictions import (
    ObjectPrediction,
    KeyPointPrediction,
    Text,
)


def test_object_prediction():
    p = ObjectPrediction(1, 20, 20, 100, 100)
    assert p.width == 80
    assert p.height == 80
    assert p.center == (60, 60)
    assert p.get_box_coordinates() == [20, 20, 100, 100]


def test_keypoint_prediction():
    p = KeyPointPrediction(0, 20, 20, 100, 100, [], [])
    assert p.width == 80
    assert p.height == 80


def test_text_prediction():
    t = Text("prova", *[20, 20, 40, 40])
    assert t.center == (40, 40)
    with pytest.raises(Exception):
        t == 10
