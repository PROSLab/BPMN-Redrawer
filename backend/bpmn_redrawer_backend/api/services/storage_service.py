import os
import numpy as np
from cv2 import cv2


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


def get_ocr_and_predict_images(path: str):
    """Service that returns the images for the OCR and Object/KeyPoints detection tasks. It retrieve the original
    image from Firebase storage given its name

    Parameters
    ----------
    path: str
        The local path where the image is downloaded

    Returns
    -------
    tuple
        The two images for OCR and predictions

    """

    ocr_img = get_ocr_image(path)
    predict_img = get_predict_image(path)
    if ocr_img is not None and predict_img is not None:
        os.remove(path)
    return ocr_img, predict_img
