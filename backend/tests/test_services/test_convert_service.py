from bpmn_redrawer_backend.bpmn.bpmn_elements import Participant, Task
from bpmn_redrawer_backend.bpmn.bpmn_flows import SequenceFlow, MessageFlow
from bpmn_redrawer_backend.bpmn.predictions import (
    ObjectPrediction,
    KeyPointPrediction,
)
from bpmn_redrawer_backend.api.services import convert_service as cs


def test_convert_object_predictions():
    p1 = ObjectPrediction(8, 20, 20, 100, 100)
    p2 = ObjectPrediction(1, 70, 70, 90, 90)
    elements = cs.convert_object_predictions([p1, p2])
    assert elements
    assert isinstance(elements[0], Participant)
    assert isinstance(elements[1], Task)


def test_convert_keypoint_prediction():
    p1 = KeyPointPrediction(0, 20, 20, 100, 100, [], [])
    p2 = KeyPointPrediction(2, 70, 70, 90, 90, [], [])
    elements = cs.convert_keypoint_prediction([p1, p2])
    assert elements
    assert isinstance(elements[0], SequenceFlow)
    assert isinstance(elements[1], MessageFlow)


def test_link_flows():
    t1 = Task("task1", ObjectPrediction(11, 20, 20, 20, 20), "task")
    t2 = Task("task2", ObjectPrediction(11, 80, 20, 20, 20), "task")
    t3 = Task("task3", ObjectPrediction(11, 80, 0, 10, 10), "task")
    p = KeyPointPrediction(0, 20, 20, 100, 100, [80, 30], [40, 30])
    elements, flow = cs.link_flows([SequenceFlow("flow", p)], [t1, t2, t3])
    assert flow[0].sourceRef == t1.id
    assert flow[0].targetRef == t2.id
    assert elements[0].outgoing == ["flow"]
    assert elements[1].incoming == ["flow"]
    assert elements[2].incoming == []
    assert elements[2].outgoing == []


def test_render_diagram():
    # TODO
    assert True
