from unittest import mock

import pytest
from marshmallow import ValidationError

from spm2021_ram_backend.api.services import database_service as ds
from spm2021_ram_backend.firebase.firebase import database


@mock.patch(
    "spm2021_ram_backend.api.services.database_service.decode_token",
    return_value={"user_id": "id"},
)
@mock.patch(
    "spm2021_ram_backend.api.services.database_service.database.child",
    return_value=database,
)
@mock.patch(
    "spm2021_ram_backend.api.services.database_service.database.set", return_value="id"
)
def test_store_conversion(mock_token, mock_child, mock_set):
    id1 = ds.store_conversion("token", "img", "mdl")
    assert id1 is not None


@mock.patch(
    "spm2021_ram_backend.api.services.database_service.decode_token",
    return_value={"user_id": "id"},
)
def test_store_conversion_fail(mock_token):
    with pytest.raises(ValidationError):
        ds.store_conversion("token", "mdl", 111)
