from typing import List


class ObjectPrediction:
    """Represents an Object Detection prediction made by the model.
    It contains information on the predicted box and its position.

    Parameters
    ----------
    predicted_label : int
        The predicted label of the box.
    top_left_x : float
        The x coordinate of the top left corner.
    top_left_y : float
        The y coordinate of the top left corner.
    bottom_right_x : float
        The x coordinate of the bottom right corner.
    bottom_right_y : float
        The y coordinate of the bottom right corner.
    """
    def __init__(
        self,
        predicted_label: int,
        top_left_x: float,
        top_left_y: float,
        bottom_right_x: float,
        bottom_right_y: float,
    ):
        self.center = None
        self.height = None
        self.width = None
        self.predicted_label = predicted_label
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
        self.calculate_box()

    def calculate_box(self):
        """Calculate additional information on the box: the width, the height and the center. """
        self.width = abs(self.bottom_right_x - self.top_left_x)
        self.height = abs(self.bottom_right_y - self.top_left_y)
        self.center = (
            self.top_left_x + self.width / 2,
            self.top_left_y + self.height / 2,
        )

    def get_box_coordinates(self) -> List[float]:
        """Returns the box coordinates as a list. """
        return [
            self.top_left_x,
            self.top_left_y,
            self.bottom_right_x,
            self.bottom_right_y,
        ]


class KeyPointPrediction:
    """Represents a Keypoint Detection prediction made by the model to recognize the flows.
    It contains information on the predicted box, its position and the keypoints.

    Parameters
    ----------
    predicted_label : int
        The predicted label of the box.
    top_left_x : float
        The x coordinate of the top left corner.
    top_left_y : float
        The y coordinate of the top left corner.
    bottom_right_x : float
        The x coordinate of the bottom right corner.
    bottom_right_y : float
        The y coordinate of the bottom right corner.
    head : list of float
        The coordinates of the flow head.
    tail : list of float
        The coordinates of the flow tail.
    """
    def __init__(
        self,
        predicted_label: int,
        top_left_x: float,
        top_left_y: float,
        bottom_right_x: float,
        bottom_right_y: float,
        head: list,
        tail: list,
    ):
        self.predicted_label = predicted_label
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
        self.width = abs(self.bottom_right_x - self.top_left_x)
        self.height = abs(self.bottom_right_y - self.top_left_y)
        self.head = head
        self.tail = tail
        self.center = (
            self.top_left_x + self.width / 2,
            self.top_left_y + self.height / 2,
        )


class Text:
    """Represents a Text recognized by the ocr.

    Parameters
    ----------
    text : str
        The text string recognized by the ocr.
    x : float
        The x coordinate of the top left corner.
    y : float
        The y coordinate of the top left corner.
    width : float
        The width of the box containing the text.
    height : float
        The height of the box containing the text.
    """
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width / 2, y + height / 2)

    def __eq__(self, other):
        if not isinstance(other, Text):
            raise Exception("Error")

        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
            and self.text == other.text
        )
