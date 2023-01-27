import json
from pathlib import Path
from typing import Dict, Iterator, Optional, cast

from ape.api import PluginConfig
from ape.exceptions import AccountsError
from ape.logging import logger
from ape.types import AddressType, BaseModel
from ape.utils import ManagerAccessMixin
from eth_utils import is_checksum_address, to_checksum_address
from pydantic import validator


def _validate_entries(entries: Dict) -> Dict:
    validated: Dict[str, AddressType] = {}
    for k, v in entries.items():

        # Attempt to handle EVM-like addresses but if it fails,
        # let it be in case it is for a more unique ecosystem.
        try:
            if not is_checksum_address(v):
                v = to_checksum_address(v)

        except Exception as err:
            logger.debug(f"Unable to checksum '{k}={v}'. Error:\n{err}")

        validated[str(k)] = v

    return validated


class AddressBookConfig(PluginConfig):
    entries: Dict[str, AddressType] = {}

    @validator("entries", pre=True)
    def validate_entries(cls, entries):
        return _validate_entries(entries)


class GlobalAddressBook(BaseModel):
    entries: Dict[str, AddressType] = {}

    @validator("entries", pre=True)
    def validate_entries(cls, entries):
        return _validate_entries(entries)


class AddressBook(ManagerAccessMixin):
    """
    A class for managing unowned, common addresses,
    similar to a contacts list. Useful scripting without
    requiring hard-coding addresses.

    Usage example::

        from ape import accounts
        from ape_addressbook import addressbook

        me = accounts.load("me")
        bob = addressbook["bob"]
        me.transfer(bob, "1000 ETH")

    """

    @property
    def global_config_file(self) -> Path:
        """
        The file path to the global addressbook entries JSON file,
        located in Ape's data folder.
        """

        return self.config_manager.DATA_FOLDER / "addressbook.json"

    @property
    def global_config(self) -> GlobalAddressBook:
        """
        All of the entries stored in the global addressbook JSON file.
        """

        file = self.global_config_file
        cls = GlobalAddressBook
        return cls.parse_file(file) if file.is_file() else cls()

    @property
    def config(self) -> AddressBookConfig:
        """
        The config entry from your project's ``ape-config.yaml`` file, which
        may contain more addressbook entries.
        """

        config_obj = self.config_manager.get_config("addressbook")
        return cast(AddressBookConfig, config_obj)

    @property
    def registry(self) -> Dict[str, AddressType]:
        """
        The complete registry of addresses, including both global
        and project addresses.
        """

        registry = self.global_config.dict().get("entries", [])
        registry.update(self.config.dict().get("entries", []))
        return registry

    @property
    def aliases(self) -> Iterator[str]:
        """
        An iterator over all aliases in the registry.
        """

        for alias in self.registry:
            yield alias

    def __contains__(self, alias: str) -> bool:
        return alias in self.aliases

    def __getitem__(self, alias: str) -> AddressType:
        if alias not in self.aliases:
            raise IndexError(f"Alias '{alias}' not in addressbook.")

        return self.registry[alias]

    def set_global_entry(
        self, alias: str, address: AddressType, ecosystem_name: Optional[str] = None
    ):
        """
        Add an address in the global registry of the addressbook.

        Args:
            alias (str): An alias for the address.
            address (``AddressType``): The address.
            ecosystem_name (Optional[str]): The ecosystem the address belongs to.
              This is only used to help decode the address. The parameter defaults
              to ``None`` but will use the connected provider's ecosystem if is connected.
              Else, will attempt to use Ethereum, which should work for any EVM ecosystem.
        """

        if alias in self.aliases:
            raise AccountsError(f"Alias '{alias}' already in addressbook.")

        if ecosystem_name is None and self.network_manager.active_provider:
            ecosystem = self.provider.network.ecosystem
        elif ecosystem_name is not None:
            ecosystem = (
                self.network_manager.ecosystems.get(ecosystem_name) or self.network_manager.ethereum
            )
        else:
            # Default to ethereum
            ecosystem = self.network_manager.ethereum

        global_config = self.global_config.copy()
        global_config.entries[alias] = ecosystem.decode_address(address)
        self.global_config_file.write_text(json.dumps(global_config.dict()))


addressbook = AddressBook()
