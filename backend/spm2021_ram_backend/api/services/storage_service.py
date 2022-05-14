import os
import tempfile

from cv2 import cv2

import time
import numpy as np

from spm2021_ram_backend.api.repositories.storage_repository import (
    store_model,
    download_image,
)


def get_ocr_image(image_path: str):
    """Service that reads and returns an image suitable for an OCR task, given its path

    Parameters
    ----------
    image_path: str
        The path where to read the image

    Returns
    -------
    ndarray
        The image for the Object/KeyPoints detection
    """

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is not None and img.shape[2] == 4:
        trans_mask = img[:, :, 3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        img = (
            img.astype(np.uint16)
            + 255
            - np.repeat(np.expand_dims(img[:, :, 3], 2), 4, axis=2)
        )
        img = np.ndarray.clip(img, 0, 255)
        img = img[:, :, [0, 1, 2]]
        img = np.ascontiguousarray(img, dtype=np.uint8)
    return img


def get_predict_image(image_path: str):
    """Services that read and returns an image suitable for an Object/KeyPoints detection task, given its path

    Parameters
    ----------
    image_path: str
        The path where to read the image

    Returns
    -------
    ndarray
        The image for the Object/KeyPoints detection
    """

    img = cv2.imread(image_path)
    return img


def get_ocr_and_predict_images(image_name: str, token: str):
    """Service that returns the images for the OCR and Object/KeyPoints detection tasks. It retrieve the original
    image from Firebase storage given its name

    Parameters
    ----------
    image_name: str
        The name of the image stored in Firebase
    token: str
        The token of the user

    Returns
    -------
    tuple
        The two images for OCR and predictions

    """

    path = download_image(image_name, token)
    ocr_img = get_ocr_image(path)
    predict_img = get_predict_image(path)
    if ocr_img is not None and predict_img is not None:
        os.remove(path)
    return ocr_img, predict_img


def store_bpmn_model(bpmn_str, token):
    """Service that stores a bpmn model into Firebase given its string representation

    Parameters
    ----------
    bpmn_str: str
        The string of the bpmn model that has to be stored in Firebase
    token: str
        The token of the user

    Returns
    -------
    str
        The name/id of the stored model
    """

    t = int(time.time() * 1000)
    model_url = f"model_{t}.bpmn"
    with tempfile.TemporaryFile() as fp:
        fp.write(bytearray(bpmn_str, encoding="utf-8"))
        fp.seek(0)
        store_model(model_url, fp, token)
    return model_url
