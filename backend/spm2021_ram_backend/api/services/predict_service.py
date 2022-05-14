from typing import List

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from numpy import ndarray

from spm2021_ram_backend.bpmn.element_factories import CATEGORIES
from spm2021_ram_backend.bpmn.predictions import (
    ObjectPrediction,
    KeyPointPrediction,
)

from spm2021_ram_backend.commons.utils import here


class ObjectPredictor:
    """Class used to represent a Detectron2 predictor trained with a faster_rcnn"""

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        )
        cfg.OUTPUT_DIR = "output"
        cfg.MODEL.WEIGHTS = here("../../detectron_model/final_model.pth")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(CATEGORIES)
        cfg.MODEL.DEVICE = "cpu"
        self._predictor = DefaultPredictor(cfg)

    def predict(self, img: ndarray):
        """Method used to predict and extract the bpmn elements from an image

        Parameters
        ----------

        img: ndarry
            The image used for the detection of the elements (as a ndaary)

        Returns
        -------
        dict
            The predictions of the elements
        """

        outs = self._predictor(img)

        # v = Visualizer(img[:, :, ::-1],
        #                scale=1.5,
        #                instance_mode=ColorMode.IMAGE_BW
        #                )
        # out = v.draw_instance_predictions(outs["instances"].to("cpu"))
        # cv2.imshow("", out.get_image()[:, :, ::-1])
        # cv2.waitKey(0)

        return outs


class KeyPointPredictor:
    """Class used to represent a Detectron2 predictor trained with a keypoint_faster_rcnn"""

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_1x.yaml")
        )
        cfg.OUTPUT_DIR = "output"
        cfg.MODEL.WEIGHTS = here("../../detectron_model/kp_final_model.pth")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
        cfg.MODEL.RETINANET.NUM_CLASSES = 3
        cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 2
        cfg.MODEL.DEVICE = "cpu"
        self._predictor = DefaultPredictor(cfg)

    def predict(self, img):
        """Method used to predict and extract the arrows from an image

        Parameters
        ----------
        img: ndarry
            The image used for the detection of the arrow (as a ndaary)

        Returns
        -------
        dict
            The predictions of the arrows
        """
        outs = self._predictor(img)

        # for kp in outs.get("instances").pred_keypoints.numpy():
        #     cv2.circle(img, (int(kp[0][0]), int(kp[0][1])), 4, (0, 255, 0), -1)
        #     cv2.circle(img, (int(kp[1][0]), int(kp[1][1])), 4, (0, 0, 255), -1)
        # cv2.imshow("", img)
        # cv2.waitKey(0)

        return outs


def predict_object(image: ndarray) -> List[ObjectPrediction]:
    """Pass an image to a trained object detection neural network model that returns the detected instances with the
    associated labels

    Parameters
    ----------
    image: ndarray
        The image used for the detection of the element (as a ndaary)

    Return
    ------
    List[ObjectPrediction]
        The list of ObjectPrediction
    """

    pred = ObjectPredictor()
    predictions = pred.predict(image)

    pred_boxes = predictions.get("instances").get("pred_boxes").tensor.numpy()
    pred_classes = predictions.get("instances").get("pred_classes").numpy()

    predictions = list(zip(pred_boxes, pred_classes))

    return [ObjectPrediction(label, *box) for box, label in predictions]


def predict_keypoint(image: ndarray) -> List[KeyPointPrediction]:
    """Pass an image to a trained keypoint detection neural network model that returns the associated predictions

    Parameters
    ----------
    image: ndarray
        The image used for the detection of the element (as a ndaary)

    Return
    ------
    List[KeyPointPrediction]
        The list of KeyPointPrediction
    """

    predictor = KeyPointPredictor()
    predictions = predictor.predict(image)

    boxes = predictions.get("instances").get("pred_boxes").tensor.numpy()
    classes = predictions.get("instances").get("pred_classes").numpy()
    keypoint = predictions.get("instances").pred_keypoints.numpy()

    predictions = list(zip(classes, boxes, keypoint))

    return [
        KeyPointPrediction(clazz, *box, key[0], key[1])
        for clazz, box, key in predictions
    ]
