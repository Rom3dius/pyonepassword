import logging
from os import environ as env

from ._py_op_commands import _OPCommandInterface
from .account import OPAccountList
from .op_items._item_list import OPItemList
from .op_items._op_item_type_registry import OPItemFactory
from .op_items._op_items_base import OPAbstractItem
from .op_items.login import OPLoginItem
from .op_items.totp import OPTOTPItem
from .op_objects import (
    OPGroup,
    OPGroupDescriptorList,
    OPUser,
    OPUserDescriptorList,
    OPVault,
    OPVaultDescriptorList
)
from .py_op_exceptions import (
    OPCmdFailedException,
    OPDocumentGetException,
    OPForgetException,
    OPInvalidDocumentException,
    OPSignoutException
)


class OP(_OPCommandInterface):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    def __init__(self,
                 vault: str = None,
                 account_shorthand: str = None,
                 password: str = None,
                 logger: logging.Logger = None,
                 op_path: str = 'op',
                 use_existing_session: bool = False,
                 password_prompt: bool = True):
        """
        Create an OP object. The 1Password sign-in happens during object instantiation.

        Authentication is attempted in the following order:
        - If use_existing_session is True and a session token is found
          in an OP_SESSION_<user UUID> environment variable, that session is verified
          and used
        - If biometric authentication is enabled, it will be used
        - If 'password' is provided, it will be provided to the 'op' command
        - If no password is provided, but password_prompt is True, 'op' will be allowed to prompt for a password
        - If authentication is attempted and failed (password or biometric), OPSigninException is raised
        - If no authentication is attempted and (no password, no password prompt, biometric not enabled), and no
          valid session is found, OPNotSignedInException is raised

        Parameters
        ----------
        vault : str, optional
            If set, this becomes the default argument to the --vault flag
            for future queries.
        account_shorthand : str, optional
            The shorthand name for the account on this device. You may choose this
            during initial signin, otherwise 1Password converts it from your account
            address. See 'op signin --help' for more information.
        password : str, optional
            If provided, the password will be piped to the 'op' command over stdin
        logger : logging.Logger
            A logging object. If not provided a basic logger is created and used
        op_path : str, optional
            Optional path to the `op` command, if it's not at the default location
        use_existing_session : bool
            Whether an existing login session should be used if possible
        password_prompt : bool
            Whether an interactive password prompt on the console should be presented if necessary

        Raises
        ------
        OPSigninException
            If 1Password sign-in fails for any reason.
        OPNotSignedInException
            if:
                - No session is available for reuse (or session reuse not requested), and
                - no password provided,
                - interactive password prompt is supressed, and
                - biometric authenticaiotn is disabled
        OPNotFoundException
            If the 1Password command can't be found
        """
        super().__init__(vault=vault,
                         account_shorthand=account_shorthand,
                         password=password,
                         logger=logger,
                         op_path=op_path,
                         use_existing_session=use_existing_session,
                         password_prompt=password_prompt)

    def item_get(self, item_name_or_uuid, vault=None) -> OPAbstractItem:
        """
        Get an 'item' object from a 1Password vault by name or UUID.
        The returned object may be any of the item types extending OPAbstractItem.
        These currently include:
        - OPLoginItem (template id 1)
        - OPCreditCardItem (template id 2)
        - OPSecureNoteItem (template id 3)
        - OPPasswordItem (template id 5)
        - OPDocumentItem (template id 6)
        - OPServerItem (template id 110)

        Note that getting a document item is not the same as getting the document itself. The
        item only contains metadata about the document such as filename.

        Parameters
        ----------
        item_name_or_uuid: str
            Name or UUID of the item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        OPGetItemException
            If the lookup fails for any reason during command execution
        OPInvalidItemException
            If the item JSON fails to decode
        OPUnknownItemType
            If the item object returned by 1Password isn't a known type
        OPNotFoundException
            If the 1Password command can't be found
        Returns
        -------
        item: OPAbstractItem
            An item object of one of the types listed above
        """

        output = super()._item_get(item_name_or_uuid, vault=vault, decode="utf-8")
        op_item = OPItemFactory.op_item(output)
        return op_item

    def item_get_totp(self, item_name_or_uuid: str, vault=None) -> OPTOTPItem:
        """
        Get a TOTP code from the item specified by name or UUID.

        Note: Items in the Archive are ignored by default. To get the TOTP for an
        item in the Archive, specify the item by UUID.

        Parameters
        ----------
        item_name_or_uuid: str
            Name or UUID of the item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        OPGetItemException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        totp_code: str
            A string representing the TOTP code
        """
        output = super()._item_get_totp(item_name_or_uuid, vault=vault, decode="utf-8")
        # strip newline
        totp = OPTOTPItem(output)
        return totp

    def user_get(self, user_name_or_uuid: str) -> OPUser:
        """
        Return the details for the user specified by name or UUID.

        Parameters
        ----------
        user_name_or_uuid: str
            Name or UUID of the user to look up
        Raises
        ------
        OPUserGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPuser
            An object representing the details of the requested user
        """
        user_json = super()._user_get(user_name_or_uuid)
        user = OPUser(user_json)
        return user

    def user_list(self, group_name_or_id=None, vault=None) -> OPUserDescriptorList:
        user_list: OPUserDescriptorList
        user_list = self._user_list(
            group_name_or_id=group_name_or_id, vault=vault)
        user_list = OPUserDescriptorList(user_list)
        return user_list

    def vault_get(self, vault_name_or_uuid: str) -> OPVault:
        """
        Return the details for the vault specified by name or UUID.

        Parameters
        ----------
        vault_name_or_uuid: str
            Name or UUID of the vault to look up
        Raises
        ------
        OPVaultGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        vault: OPVault
            An object representing the details of the requested vault
        """
        vault_json = super()._vault_get(vault_name_or_uuid, decode="utf-8")
        vault = OPVault(vault_json)
        return vault

    def vault_list(self, group_name_or_id=None, user_name_or_id=None) -> OPVaultDescriptorList:
        vault_list_json = super()._vault_list(
            group_name_or_id=group_name_or_id, user_name_or_id=user_name_or_id)
        vault_list = OPVaultDescriptorList(vault_list_json)
        return vault_list

    def group_get(self, group_name_or_uuid: str) -> OPGroup:
        """
        Return the details for the group specified by name or UUID.

        Parameters
        ----------
        group_name_or_uuid: str
            Name or UUID of the group to look up
        Raises
        ------
        OPGroupGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPGroup
            An object representing the details of the requested group
        """
        group_json = super()._group_get(group_name_or_uuid, decode="utf-8")
        group = OPGroup(group_json)
        return group

    def group_list(self, user_name_or_id=None, vault=None) -> OPUserDescriptorList:
        group_list: OPUserDescriptorList
        group_list = self._group_list(
            user_name_or_id=user_name_or_id, vault=vault)
        group_list = OPGroupDescriptorList(group_list)
        return group_list

    def item_get_password(self, item_name_or_uuid, vault=None) -> str:
        """
        Get the value of the password field from the item specified by name or UUID.

        Parameters
        ----------
        item_name_or_uuid: str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute.
        OPGetItemException
            If the lookup fails for any reason.
        OPNotFoundException
            If the 1Password command can't be found.

        Returns
        -------
        password: str
            Value of the item's 'password' attribute
        """
        item: OPLoginItem
        item = self.item_get(item_name_or_uuid, vault=vault)
        password = item.password
        return password

    def item_get_filename(self, item_name_or_uuid, vault=None):
        """
        Get the fileName attribute a document item from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_name_or_uuid : str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute
        OPGetItemException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name: str
            Value of the item's 'fileName' attribute
        """
        item = self.item_get(item_name_or_uuid, vault=vault)
        # Will raise AttributeError if item isn't a OPDocumentItem
        file_name = item.file_name

        return file_name

    def document_get(self, document_name_or_uuid, vault=None):
        """
        Download a document object from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_name_or_uuid : str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        OPInvalidDocumentException
            If the retrieved item isn't a document object or lacks a documents expected attributes
        OPDocumentGetException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name, document bytes: Tuple[str, bytes]
            A tuple consisting of the filename and bytes of the specified document
        """
        try:
            file_name = self.item_get_filename(
                document_name_or_uuid, vault=vault)
        except AttributeError as ae:
            raise OPInvalidDocumentException(
                "Item has no 'fileName' attribute") from ae
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        try:
            document_bytes = super()._document_get(document_name_or_uuid, vault=vault)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        return (file_name, document_bytes)

    def item_list(self, categories=[], include_archive=False, tags=[], vault=None):
        item_list_json = self._item_list(
            categories, include_archive, tags, vault)
        item_list = OPItemList(item_list_json)
        return item_list

    def signed_in_accounts(self, decode="utf-8") -> OPAccountList:
        account_list_json = super()._signed_in_accounts(decode)
        account_list = OPAccountList(account_list_json)
        return account_list

    def signout(self, forget=False):
        """
        Sign out of the account used to create this OP instance
        This is equivalent to the command 'op signout'
        Parameters
        ----------
        forget: bool, optional
            Optionally remove details for this 1Password account from this device.
            This is equivalent to the command 'op signout --forget'

        Raises
        ------
        OPSignoutException
            If the signout operation fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        None
        """
        account = self.account_shorthand
        token = self.token
        if not token and not self.uses_bio:
            return

        try:
            super()._signout(account, token, forget=forget)
        except OPCmdFailedException as ocfe:
            raise OPSignoutException.from_opexception(ocfe) from ocfe

        # drop any reference to op session token identifier from this
        # instance and from environment variables
        self._sanitize()

    @classmethod
    def forget(cls, account: str, op_path=None):
        """
        Remove details for the specified account from this device
        This is equivalent to the command 'op forget <account>'

        Note: this is a class method, so there is no need to have an OP instance or to have
        an active, signed-in session

        Parameters
        ----------
        account : str
            The account shorthand to forget
        op_path: str, optional
            Path to an 'op' executable to use for this action

        Raises
        ------
        OPForgetException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        None
        """

        try:
            cls._forget(account, op_path=op_path)
        except OPCmdFailedException as ocfe:
            raise OPForgetException.from_opexception(ocfe) from ocfe

    def _sanitize(self):
        self._token = None
        sess_var_name = 'OP_SESSION_{}'.format(self.account_shorthand)
        try:
            env.pop(sess_var_name)
        except KeyError:
            pass
