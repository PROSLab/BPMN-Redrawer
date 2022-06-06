from bpmn_redrawer_backend.bpmn.bpmn_elements import Element
from bpmn_redrawer_backend.bpmn.predictions import ObjectPrediction
from bpmn_redrawer_backend.commons import utils


def test_generate_id():
    idd = utils.generate_id("process")
    assert idd.startswith("process_")
    assert len(idd) == 15


def test_get_nearest_element():
    c = (50, 50)
    e1 = Element("e1", ObjectPrediction(0, 10, 10, 30, 30))
    e2 = Element("e2", ObjectPrediction(0, 70, 70, 80, 80))
    e3 = Element("e3", ObjectPrediction(0, 90, 90, 100, 100))
    n = utils.get_nearest_element(c, [e1, e2, e3])
    assert n == e2


def test_here():
    p = utils.here("./test_commons.py")
    assert all(s in p for s in ["backend", "tests", "test_commons.py"])
