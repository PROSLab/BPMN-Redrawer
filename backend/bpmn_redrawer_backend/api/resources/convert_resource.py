import time
from flask import request
from flask_restful import Resource
from bpmn_redrawer_backend.bpmn.element_factories import DiagramFactory
from bpmn_redrawer_backend.api.services import (
    predict_service as ps,
    ocr_service as os,
    convert_service as cs,
    storage_service as ss,
)
from bpmn_redrawer_backend.commons.utils import sample_bpmn, here


class ConvertApi(Resource):
    """Class Resource to manage the Api of the conversion"""

    def post(self):
        """Post method to manage the conversion of an image to its corresponding
        bpmn models. The request should contains form fields that tells whether
        elements detection, flow detection and OCR should be performed on the images

        Returns
        -------
        str
            The converted bpmn model
        """

        files = request.files
        if len(files) != 1:
            return "Uploaded file error!", 400
        file = files.get('image')
        t = int(time.time_ns())
        path = here("../../temp_files/img_{}_{}".format(t, file.filename))
        file.save(path)
        ocr_img, predict_img = ss.get_ocr_and_predict_images(path)

        if ocr_img is None or predict_img is None:
            return {"image": file.filename, "model": ''}, 200

        if "elements" in request.form and request.form["elements"] == 'true':
            obj_predictions = ps.predict_object(predict_img)
            elements = cs.convert_object_predictions(obj_predictions)

            if "flows" in request.form and request.form["flows"] == 'true':
                kp_predictions = ps.predict_keypoint(ocr_img)
                flows = cs.convert_keypoint_prediction(kp_predictions)
                cs.link_flows(flows, elements)
                elements.extend(flows)

            if "ocr" in request.form and request.form["ocr"] == 'true':
                text = os.get_text_from_img(ocr_img)
                os.link_text(text, elements)

            bpmn_diagram = DiagramFactory.create_element(elements)
            rendered_bpmn_model = cs.render_diagram(bpmn_diagram)
        else:
            rendered_bpmn_model = sample_bpmn

        return rendered_bpmn_model, 200
