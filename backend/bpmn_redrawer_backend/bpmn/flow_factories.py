from bpmn_redrawer_backend.bpmn.bpmn_flows import Flow, SequenceFlow, MessageFlow
from bpmn_redrawer_backend.bpmn.predictions import KeyPointPrediction
from bpmn_redrawer_backend.commons.utils import generate_id


class FlowFactory:
    """Parent class for the factories used to create the BPMN Flow that can either be SequenceFlow or MessageFlow
    objects. """
    generated_ids = []

    def create_flow(self, prediction: KeyPointPrediction):
        """Returns the corresponding flow associated to the factory"""


class GenericFlowFactory(FlowFactory):
    """A generic factory for Flow objects which creates a chosen Flow by extracting box information,
    text and id.

    Parameters
    ----------
    flow_class : type of Flow
        The actual subclass of Flow to create.
    """
    def __init__(self, flow_class: type(Flow)):
        self.flow_class = flow_class

    def create_flow(self, prediction: KeyPointPrediction) -> Flow:
        while (True):
            id = generate_id(self.flow_class.__name__)

            if id not in self.generated_ids:
                break

        self.generated_ids.append(id)

        return self.flow_class(id, prediction)


KEYPOINT_CATEGORIES = {
    0: "sequenceFLow",
    1: "dataAssociation",
    2: "messageFlow",
}
KEYPOINT_FACTORIES = {
    "sequenceFLow": GenericFlowFactory(SequenceFlow),
    "messageFlow": GenericFlowFactory(MessageFlow),
}


def get_keypoint_factory(category_id: int) -> FlowFactory:
    """Return the keypoint factory useful to create the flow, None if the category is not available."""
    category = KEYPOINT_CATEGORIES.get(category_id)
    return KEYPOINT_FACTORIES.get(category)
