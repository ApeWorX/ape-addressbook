from typing import Dict, Iterator, cast

from ape._pydantic_compat import root_validator
from ape.api import PluginConfig
from ape.logging import logger
from ape.types import AddressType
from ape.utils import ManagerAccessMixin
from eth_utils import is_checksum_address, to_checksum_address


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
    __root__: Dict[str, AddressType] = {}

    @root_validator(pre=True)
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

        return self.config.dict()

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


addressbook = AddressBook()
