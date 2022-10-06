from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items._new_fields import (
    OPNewStringField,
    OPNewUsernameField
)
from pyonepassword.op_items.item_section import OPItemField

if TYPE_CHECKING:
    from ..fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ..fixtures.valid_data import ValidData


def test_new_username_field_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.value == expected.value


def test_new_username_field_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.field_id == expected.field_id


def test_new_username_field_03(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.label == expected.label


def test_new_username_field_04(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.purpose == expected.purpose


def test_new_username_field_05(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.value == expected.value


def test_new_username_field_06(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.field_id == expected.field_id


def test_new_username_field_07(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.label == expected.label


def test_new_username_field_08(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.purpose == expected.purpose


def test_new_field_generate_uuid_01(valid_data: ValidData):
    """
    Create a new field from an existing field that has a hex UUID for field ID
    Verify the new field has a newly generated ID that is not the same as the original
    """
    field_dict = valid_data.data_for_name("example-field-with-uuid")
    existing_field = OPItemField(field_dict)

    new_field = OPNewStringField.from_field(existing_field)
    print(existing_field.field_id)
    print(new_field.field_id)
    assert new_field.field_id != existing_field.field_id
