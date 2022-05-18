import json

from flask import request, Response
from flask_restful import Resource
from requests import HTTPError

from spm2021_ram_backend.bpmn.element_factories import DiagramFactory
from spm2021_ram_backend.api.services import (
    predict_service as ps,
    ocr_service as os,
    convert_service as cs,
    storage_service as ss,
    database_service as ds,
)

from flask_jwt_extended import jwt_required
from spm2021_ram_backend.commons.utils import sample_bpmn


class ConvertApi(Resource):
    """Class Resource to manage the Api of the conversion"""

    @jwt_required(optional=True)
    def post(self):
        """Post method to manage the conversion of a image to a bpmn model.
        The body of the request should contains the path of the image.
        Optionally, a token can be used in the Header

        Returns
        -------
        dict
            The xml string related to the converted model.
        """

        body = request.get_json()
        image_id = body.get("imagePath")

        token = None
        if request.headers.get("Authorization") is not None:
            token = request.headers.get("Authorization").split()[1]

        orc_img, predict_img = ss.get_ocr_and_predict_images(image_id, token)

        if orc_img is None or predict_img is None:
            return Response("Image {} not found in storage".format(image_id), 404)

        if "elements" in body.keys() and body.get("elements"):
            obj_predictions = ps.predict_object(predict_img)
            elements = cs.convert_object_predictions(obj_predictions)

            if "flows" in body.keys() and body.get("flows"):
                kp_predictions = ps.predict_keypoint(orc_img)
                flows = cs.convert_keypoint_prediction(kp_predictions)
                cs.link_flows(flows, elements)
                elements.extend(flows)

                if "ocr" in body.keys() and body.get("ocr"):
                    text = os.get_text_from_png(orc_img)
                    os.link_text(text, elements)

            bpmn_diagram = DiagramFactory.create_element(elements)
            rendered_bpmn_model = cs.render_diagram(bpmn_diagram)
        else:
            rendered_bpmn_model = sample_bpmn

        if token:
            try:
                model_id = ss.store_bpmn_model(rendered_bpmn_model, token)
                ds.store_conversion(token, image_id, model_id)
            except HTTPError as e:
                er = json.loads(e.strerror).get("error")
                return {"msg": er.get("message")}, er.get("code")

            return {
                "model_id": model_id,
                "image_id": image_id,
                "xml": rendered_bpmn_model,
            }, 200

        return {"xml": rendered_bpmn_model}, 200
