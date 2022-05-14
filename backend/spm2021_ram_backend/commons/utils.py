import inspect
import math
import os
import random
import string
from typing import List, Union

from spm2021_ram_backend.bpmn.bpmn_elements import Element, Participant


def generate_id(prefix: str) -> str:
    """Utils that generate a random id given a string prefix

    Parameters
    ----------
    prefix: str
        The prefix of the id

    Returns
    -------
    str
        The random id with the given prefix
    """

    alphanumeric_str = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(7)
    )
    return f"{prefix}_{alphanumeric_str}"


def get_nearest_element(
    center: List[int], elements: List[Union[Element, Participant]]
) -> Union[Element, Participant]:
    """Utils that given a list of elements and the desired center, return the nearest element


    Parameters
    ----------
    center: List[int]
        A tuple with the coordinates of the desired center
    elements: List[Union[Element, Participant]]
        The list of objected to be considered for the nearest element

    Returns
    -------
    Union[Element, Participant]
        The nearest element to the given center
    """

    nearest = min(
        elements,
        key=lambda x: math.sqrt(
            pow(center[0] - x.prediction.center[0], 2)
            + pow(center[1] - x.prediction.center[1], 2)
        ),
    )

    return nearest


def here(resource: str):
    """Utils that given a relative path returns the corresponding absolute path, independently from the environment

    Parameters
    ----------
    resource: str
        The relative path of the given resource

    Returns
    -------
    str
        The absolute path of the give resource
    """
    stack = inspect.stack()
    caller_frame = stack[1][0]
    caller_module = inspect.getmodule(caller_frame)
    return os.path.abspath(
        os.path.join(os.path.dirname(caller_module.__file__), resource)
    )
