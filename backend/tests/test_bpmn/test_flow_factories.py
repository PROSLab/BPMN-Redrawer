from bpmn_redrawer_backend.bpmn import flow_factories as ff
from bpmn_redrawer_backend.bpmn.bpmn_flows import SequenceFlow, MessageFlow
from bpmn_redrawer_backend.bpmn.flow_factories import GenericFlowFactory
from bpmn_redrawer_backend.bpmn.predictions import KeyPointPrediction


def test_get_keypoint_factory():
    a = ff.get_keypoint_factory(0)
    b = ff.get_keypoint_factory(2)
    assert a.flow_class == SequenceFlow
    assert b.flow_class == MessageFlow


def test_generic_flow_factory():
    f1 = GenericFlowFactory(SequenceFlow)
    f2 = GenericFlowFactory(MessageFlow)
    p = KeyPointPrediction(0, 20, 20, 100, 100, [], [])
    sf = f1.create_flow(p)
    assert isinstance(sf, SequenceFlow)
    assert sf.prediction == p
    mf = f2.create_flow(p)
    assert isinstance(mf, MessageFlow)
    assert mf.prediction == p
