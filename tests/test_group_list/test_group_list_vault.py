from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

from pyonepassword.op_objects import OPGroupDescriptor

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP
    from ..fixtures.expected_group_data import (
        ExpectedGroupListData,
        ExpectedGroupListEntry
    )

from pyonepassword import OPGroupDescriptorList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")

TEST_DATA_VAULT = "Test Data"


def test_group_list_test_data_01(signed_in_op: OP, expected_group_list_data: ExpectedGroupListData):
    group_list_key = "vault-test-data"
    expected_group_list: List[ExpectedGroupListEntry]
    expected_group_list = expected_group_list_data.data_for_key(group_list_key)
    expected = expected_group_list[0]
    result = signed_in_op.group_list(vault=TEST_DATA_VAULT)
    group_entry = result[0]
    assert isinstance(result, OPGroupDescriptorList)
    assert isinstance(group_entry, OPGroupDescriptor)

    assert group_entry.unique_id == expected.unique_id


def test_group_list_test_data_02(signed_in_op: OP, expected_group_list_data: ExpectedGroupListData):
    group_list_key = "vault-test-data"
    expected_group_list: List[ExpectedGroupListEntry]
    expected_group_list = expected_group_list_data.data_for_key(group_list_key)
    expected = expected_group_list[1]
    result = signed_in_op.group_list(vault=TEST_DATA_VAULT)
    group_entry = result[1]
    assert isinstance(result, OPGroupDescriptorList)
    assert isinstance(group_entry, OPGroupDescriptor)

    assert group_entry.description == expected.description


def test_group_list_test_data_03(signed_in_op: OP, expected_group_list_data: ExpectedGroupListData):
    group_list_key = "vault-test-data"
    expected_group_list: List[ExpectedGroupListEntry]
    expected_group_list = expected_group_list_data.data_for_key(group_list_key)
    expected = expected_group_list[2]
    result = signed_in_op.group_list(vault=TEST_DATA_VAULT)
    group_entry = result[2]
    assert isinstance(result, OPGroupDescriptorList)
    assert isinstance(group_entry, OPGroupDescriptor)

    assert group_entry.state == expected.state


def test_group_list_test_data_04(signed_in_op: OP, expected_group_list_data: ExpectedGroupListData):
    group_list_key = "vault-test-data"
    expected_group_list: List[ExpectedGroupListEntry]
    expected_group_list = expected_group_list_data.data_for_key(group_list_key)
    expected = expected_group_list[2]
    result = signed_in_op.group_list(vault=TEST_DATA_VAULT)
    group_entry = result[2]
    assert isinstance(result, OPGroupDescriptorList)
    assert isinstance(group_entry, OPGroupDescriptor)

    assert group_entry.created_at == expected.created_at
