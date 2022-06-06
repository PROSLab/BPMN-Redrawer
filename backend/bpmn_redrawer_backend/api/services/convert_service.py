import jinja2
from typing import List, TYPE_CHECKING

from bpmn_redrawer_backend.bpmn.bpmn_elements import Participant, Element, Diagram
from bpmn_redrawer_backend.bpmn.bpmn_flows import Flow
from bpmn_redrawer_backend.bpmn.element_factories import get_factory
from bpmn_redrawer_backend.bpmn.flow_factories import get_keypoint_factory
from bpmn_redrawer_backend.commons.utils import get_nearest_element, here

if TYPE_CHECKING:
    from bpmn_redrawer_backend.bpmn.predictions import (
        ObjectPrediction,
        KeyPointPrediction,
    )


def convert_object_predictions(predictions: List["ObjectPrediction"]):
    """Method that converts the prediction of the detected bpmn object into Elements

    Parameters
    ----------
    predictions: List[ObjectPrediction]
        List of ObjectPrediction

    Returns
    -------
    List[Element]
        The list of converted bpmn Element
    """

    elements = []
    for prediction in predictions:
        factory = get_factory(prediction.predicted_label)
        if factory is not None:
            bpmn_element = factory.create_element(prediction)
            if bpmn_element is not None:
                elements.append(bpmn_element)

    return elements


def render_diagram(bpmn_diagram: Diagram):
    """Method that renders a Diagram class into the final bpmn string

    Parameters
    ----------
    bpmn_diagram: Diagram
        List of ObjectPrediction

    Returns
    -------
    str
        The string representing the final bpmn model
    """

    template_loader = jinja2.FileSystemLoader(
        searchpath=here("../../commons/templates/")
    )
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "bpmntemplate.jinja"
    template = template_env.get_template(template_file)
    output_text = template.render({"diagram": bpmn_diagram})

    return output_text


def convert_keypoint_prediction(predictions: List["KeyPointPrediction"]):
    """Method that converts the prediction of the keypoint into Flow

    Parameters
    ----------
    predictions: List[KeyPointPrediction]
        List of KeyPointPrediction

    Returns
    -------
    List[Flow]
        The list of converted bpmn Flow
    """

    flows = []
    for prediction in predictions:
        factory = get_keypoint_factory(prediction.predicted_label)
        if factory is not None:
            flow = factory.create_flow(prediction)
            if flow is not None:
                flows.append(flow)

    return flows


def link_flows(flows: List[Flow], elements: List[Element]):
    """Method that links the Flow to the corresponding Elements

    Parameters
    ----------
    flows: List[Flow]
        List of detected Flow
    elements: List[Element}
        List of Element to be linked

    Returns
    -------
    tuple: tuple[List[Element], List[Flow]]
        The list of updated Element and Flow

    """

    # try to find a better way to link them
    for flow in flows:
        head = flow.prediction.head
        tail = flow.prediction.tail

        near_head = get_nearest_element(head, elements)
        near_tail = get_nearest_element(tail, elements)

        flow.targetRef = near_head.id
        flow.sourceRef = near_tail.id

        if not isinstance(near_tail, Participant):
            near_tail.outgoing.append(flow.id)
        if not isinstance(near_head, Participant):
            near_head.incoming.append(flow.id)

    return elements, flows
