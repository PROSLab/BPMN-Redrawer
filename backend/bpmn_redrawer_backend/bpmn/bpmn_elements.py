from dataclasses import dataclass, field
from typing import List

from jinja2 import Environment, BaseLoader

from bpmn_redrawer_backend.bpmn.predictions import ObjectPrediction, Text


class Element:
    """Parent class for all the elements that can be put within a BPMN Process.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    prediction : ObjectPrediction
        The prediction given by the object detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: ObjectPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.name = []
        self.jinja_environment = Environment(loader=BaseLoader())
        self.incoming = []
        self.outgoing = []

    def render_element(self):
        """Returns the xml string associated to this kind of element"""

    def get_name(self):
        """Returns the text of the element as a string"""
        return " ".join([text.text for text in self.name])

    def render_shape(self):
        """Returns the xml string containing the shape information of this kind of element"""
        template = """<bpmndi:BPMNShape id="{{ element.id }}_di" bpmnElement="{{ element.id }}" >
        <dc:Bounds x="{{ element.prediction.top_left_x }}" y="{{ element.prediction.top_left_y }}" width="{{ element.prediction.width }}" height="{{ element.prediction.height }}" />
      </bpmndi:BPMNShape>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(element=self)

        return data


class StartEvent(Element):
    """Represents a BPMN Start Event which can be of different types.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    prediction : ObjectPrediction
        The prediction given by the object detection predictor.
    type : str, {'startEvent', 'messageEventDefinition', 'timerEventDefinition', 'signalEventDefinition'}
        The type of start event.
    """
    def __init__(
        self,
        id: str,
        prediction: ObjectPrediction,
        type: str,
    ):
        super(StartEvent, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        if self.type == "startEvent":
            template = """<bpmn:startEvent id="{{ start_event.id }}" name="{{ start_event.get_name() }}" />"""
        else:
            template = """<bpmn:startEvent id="{{ start_event.id }}" name="{{ start_event.get_name() }}">
      <bpmn:{{ start_event.type }} />
    </bpmn:startEvent>
        """

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(start_event=self)

        return data


class EndEvent(Element):
    """Represents a BPMN End Event which can be of different types.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
        type : str, {'endEvent', 'messageEventDefinition', 'errorEventDefinition', 'escalationEventDefinition', 'terminateEventDefinition'}
            The type of end event.
        """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(EndEvent, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        if self.type == "endEvent":
            template = """<bpmn:endEvent id="{{ end_event.id }}" name="{{ end_event.get_name() }}"/>"""
        else:
            template = """<bpmn:endEvent id="{{ end_event.id }}" name="{{ end_event.get_name() }}">
      <bpmn:{{ end_event.type }} />
    </bpmn:endEvent>
        """

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(end_event=self)

        return data


class IntermediateThrowEvent(Element):
    """Represents a BPMN Intermediate Throw Event which can be of different types.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
        type : str, {'intermediateThrowEvent', 'messageEventDefinition', 'escalationEventDefinition'}
            The type of intermediate throw event.
        """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(IntermediateThrowEvent, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        if self.type == "intermediateThrowEvent":
            template = """<bpmn:intermediateThrowEvent id="{{ intermediate_event.id }}" name="{{ intermediate_event.get_name() }}" />"""
        else:
            template = """<bpmn:intermediateThrowEvent id="{{ intermediate_event.id }}" name="{{ intermediate_event.get_name() }}">
      <bpmn:{{ intermediate_event.type }} />
    </bpmn:intermediateThrowEvent>
        """

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(intermediate_event=self)

        return data


class IntermediateCatchEvent(Element):
    """Represents a BPMN Intermediate Catch Event which can be of different types.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
        type : str, {'messageEventDefinition', 'timerEventDefinition'}
            The type of intermediate catch event.
        """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(IntermediateCatchEvent, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        template = """<bpmn:intermediateCatchEvent id="{{ intermediate_event.id }}" name="{{ intermediate_event.get_name() }}">
      <bpmn:{{ intermediate_event.type }} />
    </bpmn:intermediateCatchEvent>
        """

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(intermediate_event=self)

        return data


class Gateway(Element):
    """Represents a BPMN Gateway which can be of different types.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
        type : str, {'inclusiveGateway', 'parallelGateway', 'exclusiveGateway', 'eventBasedGateway', 'complexGateway'}
            The type of gateway.
    """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(Gateway, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        template = """<bpmn:{{ gateway.type }} id="{{ gateway.id }}" name="{{ gateway.get_name() }}" />"""

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(gateway=self)

        return data


class Task(Element):
    """Represents a BPMN Task which can be of different types.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
        type : str, {'task', 'sendTask', 'subProcess', 'serviceTask', 'userTask'}
            The type of task.
    """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(Task, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        template = """<bpmn:{{ task.type }} id="{{ task.id }}" name="{{ task.get_name() }}"/>"""

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(task=self)

        return data


class TextAnnotation(Element):
    """Represents a BPMN Text Association.

        Parameters
        ----------
        id : str
            Unique identifier of the BPMN Element.
        prediction : ObjectPrediction
            The prediction given by the object detection predictor.
    """
    def __init__(self, id: str, prediction: ObjectPrediction, type: str):
        super(TextAnnotation, self).__init__(id, prediction)
        self.type = type

    def render_element(self):
        template = """<bpmn:textAnnotation id="{{ textAnnotation.id }}">
      <bpmn:text>{{ textAnnotation.get_name() }}</bpmn:text>
    </bpmn:textAnnotation>
        """

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(textAnnotation=self)

        return data


@dataclass()
class Process:
    """Represents a BPMN Process which contains the elements of the BPMN Diagram.
    If there exist a Participant then there will be one Process for each of them containing
    the elements associated to each Participant.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    elements : list of Element
        The list of BPMN Elements contained within this process.
    """
    id: str
    elements: List[Element] = field(default_factory=lambda: [])


@dataclass()
class Participant:
    """Represents a BPMN Participant which is associated to one and only one Process.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    prediction : ObjectPrediction
        The prediction given by the object detection predictor.
    process : Process
        The Process associated to this Participant
    name : list of Text
        The text, as a list, associated to the Participant.
    """
    id: str
    prediction: ObjectPrediction
    process: Process
    name: List[Text] = field(default_factory=lambda: [])

    def get_name(self):
        return " ".join([text.text for text in self.name])

    def __hash__(self):
        return hash((frozenset(self.id), frozenset(self.process.id)))


class Collaboration:
    """Represents a BPMN Collaboration which is the xml tag containing the Participants and the Message Flows.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    participants : list of Participant
        The list of Participant to include in the xml file.
    message_flows : list of MessageFlow
        The list of MessageFlow to include in the xml file.
    """
    def __init__(self, id: str, participants: List[Participant], message_flows):
        self.id = id
        self.participants = participants
        self.message_flows = message_flows


@dataclass()
class Diagram:
    """Represents a BPMN Diagram which contains all the information used to write the xml file.

    Parameters
    ----------
    id : str
        Unique identifier of the BPMN Element.
    definition_id : str
        Unique identifier of the BPMN Definition tag.
    processes : list of Process
        The list of Process to include in the xml file.
    collaboration : Collaboration
        The collaboration object to include in the xml file.
    """
    id: str
    definition_id: str
    processes: List[Process]
    collaboration: Collaboration = None
