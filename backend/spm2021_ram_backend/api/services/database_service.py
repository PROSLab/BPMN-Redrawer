from flask_jwt_extended import decode_token

from spm2021_ram_backend.api.schemas.bpmn_models import ConversionSchema

import time

from spm2021_ram_backend.firebase.firebase import database


def store_conversion(token: str, image_id: str, model_id: str):
    """Service that stores the information related to a model conversion in Firebase database

    Parameters
    ----------
    token: str
        The token of the user
    image_id: str
        The id of the converted image
    model_id: str
        The id of the converted model

    Returns
    -------
    str
        The id of the stored conversion

    """

    timestamp = int(time.time() * 1000)
    user_id = decode_token(token).get("user_id")
    conv = ConversionSchema().load(
        {"image_id": image_id.split("/")[-1], "model_id": model_id}
    )

    conv_id = database.child(f"{user_id}/{timestamp}").set(conv, token)

    return conv_id
