import pytest

from bpmn_redrawer_backend.bpmn.bpmn_elements import (
    Task,
    StartEvent,
    EndEvent,
    Gateway,
    Element,
    Participant,
    IntermediateThrowEvent,
    IntermediateCatchEvent,
)
from bpmn_redrawer_backend.bpmn.predictions import ObjectPrediction, Text


@pytest.fixture
def params():
    yield ObjectPrediction(0, 20, 20, 100, 100), [
        Text("test", *[186, 35, 27, 9]),
        Text("text", *[186, 35, 27, 9]),
    ]


def test_get_name(params):
    p = Participant("part", params[0], None)
    p.name = params[1]
    assert p.get_name() == "test text"
    e = Element("elem", params[0])
    e.name = params[1]
    assert p.get_name() == "test text"


def test_start_event(params):
    s = StartEvent("start", params[0], "startEvent")
    s.name = params[1]
    re = s.render_element()
    ree = '<bpmn:startEvent id="start" name="test text" />'
    assert re == ree

    rs = s.render_shape()
    rse = """<bpmndi:BPMNShape id="start_di" bpmnElement="start" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse

    s.type = "newStart"
    re2 = s.render_element()
    ree2 = """<bpmn:startEvent id="start" name="test text">
      <bpmn:newStart />
    </bpmn:startEvent>
        """
    assert re2 == ree2


def test_end_event(params):
    e = EndEvent("end", params[0], "endEvent")
    e.name = params[1]
    re = e.render_element()
    ree = '<bpmn:endEvent id="end" name="test text"/>'
    assert re == ree

    rs = e.render_shape()
    rse = """<bpmndi:BPMNShape id="end_di" bpmnElement="end" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse

    e.type = "newEnd"
    re2 = e.render_element()
    ree2 = """<bpmn:endEvent id="end" name="test text">
      <bpmn:newEnd />
    </bpmn:endEvent>
        """
    assert re2 == ree2


def test_task(params):
    t = Task("task", params[0], "task")
    t.name = params[1]
    re = t.render_element()
    ree = '<bpmn:task id="task" name="test text"/>'
    assert re == ree

    rs = t.render_shape()
    rse = """<bpmndi:BPMNShape id="task_di" bpmnElement="task" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse

    t.type = "serviceTask"
    re2 = t.render_element()
    ree2 = '<bpmn:serviceTask id="task" name="test text"/>'
    assert re2 == ree2


def test_gateway(params):
    g = Gateway("gate", params[0], "exclusiveGateway")
    g.name = params[1]
    re = g.render_element()
    ree = '<bpmn:exclusiveGateway id="gate" name="test text" />'
    assert re == ree

    rs = g.render_shape()
    rse = """<bpmndi:BPMNShape id="gate_di" bpmnElement="gate" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse

    g.type = "parallelGateway"
    re2 = g.render_element()
    ree2 = '<bpmn:parallelGateway id="gate" name="test text" />'
    assert re2 == ree2


def test_intermediate_throw_event(params):
    i = IntermediateThrowEvent("ite", params[0], "intermediateThrowEvent")
    i.name = params[1]
    re = i.render_element()
    ree = '<bpmn:intermediateThrowEvent id="ite" name="test text" />'
    assert re == ree

    rs = i.render_shape()
    rse = """<bpmndi:BPMNShape id="ite_di" bpmnElement="ite" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse

    i.type = "newIte"
    re2 = i.render_element()
    ree2 = """<bpmn:intermediateThrowEvent id="ite" name="test text">
      <bpmn:newIte />
    </bpmn:intermediateThrowEvent>
        """
    assert re2 == ree2


def test_intermediate_catch_event(params):
    i = IntermediateCatchEvent("ice", params[0], "intermediateCatchEvent")
    i.name = params[1]
    re = i.render_element()
    ree = """<bpmn:intermediateCatchEvent id="ice" name="test text">
      <bpmn:intermediateCatchEvent />
    </bpmn:intermediateCatchEvent>
        """
    assert re == ree

    rs = i.render_shape()
    rse = """<bpmndi:BPMNShape id="ice_di" bpmnElement="ice" >
        <dc:Bounds x="20" y="20" width="80" height="80" />
      </bpmndi:BPMNShape>
        """
    assert rs == rse
