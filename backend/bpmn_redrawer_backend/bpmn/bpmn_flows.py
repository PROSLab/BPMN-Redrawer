from jinja2 import Environment, BaseLoader

from bpmn_redrawer_backend.bpmn.predictions import KeyPointPrediction


class Flow:
    """Parent class for all the flows that can be put within a BPMN Diagram.

    Parameters
    ----------
    id : str
        Unique identifier of the Flow.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.name = []
        self.jinja_environment = Environment(loader=BaseLoader())
        self.sourceRef = None
        self.targetRef = None

    def render_element(self):
        """Returns the xml string associated to this kind of flow"""

    def get_name(self):
        """Returns the text of the flow as a string"""
        return " ".join([text.text for text in self.name])

    def render_shape(self):
        """Returns the xml string containing the shape information of this kind of flow"""
        template = """<bpmndi:BPMNEdge id="{{ element.id }}_di" bpmnElement="{{ element.id }}" >
        <di:waypoint x="{{ element.prediction.tail[0] }}" y="{{ element.prediction.tail[1] }}" />
        <di:waypoint x="{{ element.prediction.head[0] }}" y="{{ element.prediction.head[1] }}" />
      </bpmndi:BPMNEdge>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(element=self)

        return data


class SequenceFlow(Flow):
    """Represents a BPMN Sequence Flow.

    Parameters
    ----------
    id : str
        Unique identifier of the Flow.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        super(SequenceFlow, self).__init__(id, prediction)

    def render_element(self):
        """Returns the xml string associated to a SequenceFLow"""

        template = """<bpmn:sequenceFlow id="{{ flow.id }}" name="{{ flow.get_name() }}" sourceRef="{{ flow.sourceRef }}" targetRef="{{ flow.targetRef }}" />"""
        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(flow=self)

        return data


class MessageFlow(Flow):
    """Represents a BPMN Message Flow.

    Parameters
    ----------
    id : str
        Unique identifier of the Flow.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        super(MessageFlow, self).__init__(id, prediction)

    def render_element(self):
        """Returns the xml string associated to MessageFlow"""

        template = """<bpmn:messageFlow id="{{ flow.id }}" name="{{ flow.get_name() }}" sourceRef="{{ flow.sourceRef }}" targetRef="{{ flow.targetRef }}" />"""
        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(flow=self)

        return data
