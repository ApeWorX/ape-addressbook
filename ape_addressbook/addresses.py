from collections.abc import Iterator
from typing import TYPE_CHECKING, cast

from ape.api import PluginConfig
from ape.logging import logger
from ape.utils import ManagerAccessMixin
from cchecksum import to_checksum_address
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict

if TYPE_CHECKING:
    from ape.types import AddressType


def _validate_entries(entries: dict) -> dict:
    validated: dict[str, "AddressType"] = {}
    for k, v in entries.items():
        # Attempt to handle EVM-like addresses but if it fails,
        # let it be in case it is for a more unique ecosystem.
        try:
            v = to_checksum_address(v)
        except Exception as err:
            logger.debug(f"Unable to checksum '{k}={v}'. Error:\n{err}")

        validated[str(k)] = v

    return validated


class AddressBookConfig(PluginConfig):
    @model_validator(mode="before")
    @classmethod
    def validate_entries(cls, entries):
        return _validate_entries(entries)

    def __len__(self) -> int:
        return len(self.model_dump())

    model_config = SettingsConfigDict(extra="allow")


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
    def registry(self) -> dict[str, "AddressType"]:
        """
        The complete registry of addresses, including both global
        and project addresses.
        """

        data = self.config.model_dump()

        # Sorted for consistency's sake.
        return {k: data[k] for k in sorted(data)}

    @property
    def aliases(self) -> Iterator[str]:
        """
        An iterator over all aliases in the registry.
        """

        # NOTE: self.registry is sorted.
        for alias in self.registry:
            yield alias

    def __contains__(self, alias: str) -> bool:
        return alias in self.aliases

    def __getitem__(self, alias: str) -> "AddressType":
        if alias not in self.aliases:
            raise IndexError(f"Alias '{alias}' not in addressbook.")

        return self.registry[alias]

    def __iter__(self) -> Iterator[str]:
        yield from self.aliases  # dict like behavior


addressbook = AddressBook()
