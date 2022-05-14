import time

from flask_jwt_extended import decode_token

from spm2021_ram_backend.commons.utils import here
from spm2021_ram_backend.firebase.firebase import storage


def download_image(image_name: str, token: str):
    """Method that downloads an image that is stored in Firebase and returns the path

    Parameters
    ----------
    image_name: str
        The name of the image stored in Firebase
    token: str
        The token of the user

    Returns
    -------
    str
        The local path where the image is downloaded
    """

    t = int(time.time() * 1000)
    path = here("../../temp_files/img_{}.png".format(t))

    image_path = "anon/"
    if token:
        id_user = decode_token(token).get("user_id")
        image_path = f"images/{id_user}/"

    storage.child(image_path + image_name).download(image_name, path, token)
    return path


def store_model(model_url: str, model, token: str):
    """Methods that stores a bpmn model into Firebase storage given the corresponding url

    Parameters
    ----------
    model_url: str
        The name of the image stored in Firebase
    model: Any
        The object that has to be stored in Firebase
    token: str
        The token of the user
    """

    id_user = decode_token(token).get("user_id")
    storage.child(f"models/{id_user}/{model_url}").put(model, token)
