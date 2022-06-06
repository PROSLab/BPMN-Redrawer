from bpmn_redrawer_backend.bpmn import element_factories as f
from bpmn_redrawer_backend.bpmn.bpmn_elements import (
    StartEvent,
    Gateway,
    Participant,
    Task, Process,
)
from bpmn_redrawer_backend.bpmn.bpmn_flows import MessageFlow
from bpmn_redrawer_backend.bpmn.element_factories import (
    ParticipantFactory,
    GenericElementFactory, extend_participants, DiagramFactory,
)
from bpmn_redrawer_backend.bpmn.predictions import ObjectPrediction, KeyPointPrediction


def test_diagram_factory():
    # TODO
    assert True


def test_generic_element_factory():
    f1 = GenericElementFactory(Gateway, "parallelGateway")
    p = ObjectPrediction(7, 50, 50, 60, 60)
    g = f1.create_element(p)
    assert isinstance(g, Gateway)
    assert g.prediction == p
    g.type == "parallelGateway"

    f2 = GenericElementFactory(Task, "subProcess")
    t = f2.create_element(p)
    assert isinstance(t, Task)
    assert t.prediction == p
    t.type == "subProcess"


def test_participant_factory():
    pf = ParticipantFactory()
    p = ObjectPrediction(1, 50, 50, 60, 60)
    part = pf.create_element(p)
    assert isinstance(part, Participant)
    assert part.prediction == p
    assert part.process.id.startswith("Process")


def test_calculate_width_height():
    wh = f.calculate_width_height(20.0, 20.0, 50.0, 50.0)
    assert wh == (30.0, 30.0)


def test_connect_participants():
    p = Participant("part", ObjectPrediction(0, 20, 20, 100, 100), None)
    t1 = Task("t1", ObjectPrediction(0, 50, 50, 60, 60), "task")
    t2 = Task("t2", ObjectPrediction(0, 10, 10, 5, 5), "task")
    s1 = StartEvent("s1", ObjectPrediction(0, 70, 70, 80, 80), "startEvent")
    s2 = StartEvent("s2", ObjectPrediction(0, 110, 110, 120, 120), "startEvent")
    e = f.connect_participants(p, [t1, t2, s1, s2])
    assert len(e) == 2
    assert e[0] == t1
    assert e[1] == s1


def test_get_factory():
    part = f.get_factory(8)
    assert isinstance(part, ParticipantFactory)

    start = f.get_factory(19)
    assert isinstance(start, GenericElementFactory)
    assert start.element_type == "startEvent"
    assert start.element_class == StartEvent

    gate = f.get_factory(12)
    assert isinstance(gate, GenericElementFactory)
    assert gate.element_type == "parallelGateway"
    assert gate.element_class == Gateway


def test_extend_participant_bottom():
    participant_pred = ObjectPrediction(8, 0, 0, 500, 200)
    start_pred = ObjectPrediction(19, 70, 100, 106, 136)
    start_event = StartEvent("s1", start_pred, "startEvent")
    parallel_gate_pred = ObjectPrediction(12, 100, 230, 136, 266)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")
    process = Process("pr1", [start_event, parallel_gate])
    p = Participant("p1", participant_pred, process)

    extend_participants([p])

    assert p.prediction.top_left_x == 0 and p.prediction.top_left_y == 0 and p.prediction.bottom_right_x == 500 and p.prediction.bottom_right_y == 286


def test_extend_participant_right():
    participant_pred = ObjectPrediction(8, 0, 0, 500, 200)
    start_pred = ObjectPrediction(19, 70, 100, 106, 136)
    start_event = StartEvent("s1", start_pred, "startEvent")
    parallel_gate_pred = ObjectPrediction(12, 550, 100, 586, 136)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")
    process = Process("pr1", [start_event, parallel_gate])
    p = Participant("p1", participant_pred, process)

    extend_participants([p])

    assert p.prediction.top_left_x == 0 and p.prediction.top_left_y == 0 and p.prediction.bottom_right_x == 606 and p.prediction.bottom_right_y == 200


def test_extend_participant_top():
    participant_pred = ObjectPrediction(8, 0, 100, 500, 300)
    start_pred = ObjectPrediction(19, 70, 200, 106, 236)
    start_event = StartEvent("s1", start_pred, "startEvent")
    parallel_gate_pred = ObjectPrediction(12, 100, 40, 136, 76)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")
    process = Process("pr1", [start_event, parallel_gate])
    p = Participant("p1", participant_pred, process)

    extend_participants([p])

    assert p.prediction.top_left_x == 0 and p.prediction.top_left_y == 20 and p.prediction.bottom_right_x == 500 and p.prediction.bottom_right_y == 300


def test_extend_participant_bottom_y():
    participant_pred = ObjectPrediction(8, 100, 0, 500, 200)
    start_pred = ObjectPrediction(19, 170, 100, 206, 136)
    start_event = StartEvent("s1", start_pred, "startEvent")
    parallel_gate_pred = ObjectPrediction(12, 50, 100, 86, 136)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")
    process = Process("pr1", [start_event, parallel_gate])
    p = Participant("p1", participant_pred, process)

    extend_participants([p])

    assert p.prediction.top_left_x == 30 and p.prediction.top_left_y == 0 and p.prediction.bottom_right_x == 500 and p.prediction.bottom_right_y == 200


def test_diagram_extending_participant():
    participant_pred = ObjectPrediction(8, 0, 0, 500, 200)
    start_pred = ObjectPrediction(19, 70, 100, 106, 136)
    start_event = StartEvent("s1", start_pred, "startEvent")
    process = Process("pr1")
    p = Participant("p1", participant_pred, process)
    parallel_gate_pred = ObjectPrediction(12, 100, 230, 136, 266)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")
    message_flow_pred = KeyPointPrediction(2, 80, 136, 106, 351, [90, 136], [90, 351])
    message_flow = MessageFlow("mf1", message_flow_pred)

    diagram = DiagramFactory.create_element([start_event, parallel_gate, p, message_flow])

    assert len(diagram.processes) == 1 and len(diagram.collaboration.participants) == 1 and len(diagram.collaboration.message_flows) == 1 and all(el in diagram.collaboration.participants[0].process.elements for el in [start_event, parallel_gate])


def test_diagram_empty_participant():
    participant_pred = ObjectPrediction(8, 0, 0, 500, 200)
    start_pred = ObjectPrediction(19, 70, 100, 106, 136)
    empty_part_pred = ObjectPrediction(8, 0, 300, 500, 350)
    start_event = StartEvent("s1", start_pred, "startEvent")
    process1 = Process("pr1")
    p1 = Participant("p1", participant_pred, process1)
    process2 = Process("pr2")
    p2 = Participant("p2", empty_part_pred, process2)

    DiagramFactory.create_element([start_event, p1, p2])

    assert start_event in p1.process.elements and not p2.process.elements and p2.process.id == ""


def test_diagram_no_participant():
    start_pred = ObjectPrediction(19, 70, 100, 106, 136)
    start_event = StartEvent("s1", start_pred, "startEvent")
    parallel_gate_pred = ObjectPrediction(12, 100, 230, 136, 266)
    parallel_gate = Gateway("g1", parallel_gate_pred, "parallelGateway")

    diagram = DiagramFactory.create_element([start_event, parallel_gate])

    assert len(diagram.processes) == 1 and diagram.collaboration is None
