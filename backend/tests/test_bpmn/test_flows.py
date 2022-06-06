from bpmn_redrawer_backend.bpmn.bpmn_flows import SequenceFlow, MessageFlow
from bpmn_redrawer_backend.bpmn.predictions import KeyPointPrediction


def test_sequence_flow():
    sf = SequenceFlow("sf", KeyPointPrediction(0, 20, 20, 100, 100, [40, 30], [20, 30]))
    sf.sourceRef = "source"
    sf.targetRef = "target"
    re = sf.render_element()
    ree = '<bpmn:sequenceFlow id="sf" name="" sourceRef="source" targetRef="target" />'
    assert re == ree
    rs = sf.render_shape()
    rse = """<bpmndi:BPMNEdge id="sf_di" bpmnElement="sf" >
        <di:waypoint x="20" y="30" />
        <di:waypoint x="40" y="30" />
      </bpmndi:BPMNEdge>
        """
    assert rs == rse


def test_message_flow():
    mf = MessageFlow("mf", KeyPointPrediction(0, 20, 20, 100, 100, [40, 30], [20, 30]))
    mf.sourceRef = "source"
    mf.targetRef = "target"
    re = mf.render_element()
    ree = '<bpmn:messageFlow id="mf" name="" sourceRef="source" targetRef="target" />'
    assert re == ree
    rs = mf.render_shape()
    rse = """<bpmndi:BPMNEdge id="mf_di" bpmnElement="mf" >
        <di:waypoint x="20" y="30" />
        <di:waypoint x="40" y="30" />
      </bpmndi:BPMNEdge>
        """
    assert rs == rse
