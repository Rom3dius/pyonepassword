"""
Miscellaneous classes for objects return by 'op get' other than item or document objects
"""
import json
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Union

from .py_op_exceptions import _OPAbstractException
from ._datetime import fromisoformat_z


class OPInvalidObjectException(_OPAbstractException):
    def __init__(self, msg, object_json):
        super().__init__(msg)
        self.object_json = object_json


class OPInvalidUserException(OPInvalidObjectException):
    def __init__(self, msg, user_json):
        super().__init__(msg, user_json)


class OPUser(dict):
    """
    A class that represents the result from an 'op get user' operation.
    This is a dictionary unserialized from the operation's JSON output, and can be treated
    as a normal dictionary. In addition, it has a convenience property for each key in the
    the dictionary.

    Note: date-related properties return parsed 'datetime' objects. To access the original
    date strings, use the corresponding dictionary key
    """

    def __init__(self, user_dict_or_json: Union[str, dict]):
        if isinstance(user_dict_or_json, str):
            try:
                user_dict = json.loads(user_dict_or_json)
            except JSONDecodeError as jdce:
                raise OPInvalidUserException(
                    f"Failed to unserialize user json: {jdce}", user_dict_or_json)
        else:
            user_dict = user_dict_or_json
        super().__init__(user_dict)

    @property
    def uuid(self):
        """
        str: The user object's UUID
        """
        return self["uuid"]

    @property
    def created_at(self) -> datetime:
        """
        datetime : The createdAt attribute parsed as a datetime object
        """
        created = self["createdAt"]
        created = fromisoformat_z(created)
        return created

    @property
    def updatedAt(self) -> datetime:
        """
        datetime : The updatedAt attribute parsed as a datetime object
        """
        updated = self["updatedAt"]
        updated = fromisoformat_z(updated)
        return updated

    @property
    def last_auth_at(self) -> datetime:
        """
        datetime : The lastAuthAt attribute parsed as a datetime object
        """
        last_auth = self["lastAuthAt"]
        last_auth = fromisoformat_z(last_auth)
        return last_auth

    @property
    def email(self) -> str:
        """
        str : The email attribute
        """
        return self["email"]

    @property
    def first_name(self) -> str:
        """
        str : The firstName attribute
        """
        return self["firstName"]

    @property
    def last_name(self) -> str:
        """
        str : The lastName attribute
        """
        return self["lastName"]

    @property
    def name(self) -> str:
        """
        str : The name attribute
        """
        return self["name"]

    @property
    def attr_version(self) -> int:
        return self["attrVersion"]

    @property
    def keyset_version(self) -> int:
        """
        str : The keysetVersion attribute
        """
        return self["keysetVersion"]

    @property
    def state(self) -> str:
        """
        str : The state attribute
        """
        return self["state"]

    @property
    def type(self) -> str:
        """
        str : The type attribute
        """
        return self["type"]

    @property
    def avatar(self) -> str:
        """
        str : The avatar attribute
        """
        return self["avatar"]

    @property
    def language(self) -> str:
        """
        str : The language attribute
        """
        return self["language"]

    @property
    def account_key_format(self) -> str:
        """
        str : The accountKeyFormat attribute
        """
        return self["accountKeyFormat"]

    @property
    def account_key_uuid(self) -> str:
        """
        str : The accountKeyUuid attribute
        """
        return self["accountKeyUuid"]

    @property
    def combined_permissions(self) -> str:
        """
        str : The combinedPermission attribute
        """
        return self["combinedPermissions"]
