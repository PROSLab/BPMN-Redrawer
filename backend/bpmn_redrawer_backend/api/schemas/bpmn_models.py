from marshmallow import Schema, fields


class ConversionSchema(Schema):
    """Schema representing the information related to a model conversion

    Attribute
    ----------
    image_id: str
        The id of the image
    model_id: str
        The id of the converted model
    """

    image_id = fields.String()
    model_id = fields.String()
