import json
from pathlib import Path
from typing import Dict, Iterator

from ape.api.config import PluginConfig
from ape.types import AddressType
from ape.utils import ManagerAccessMixin


class AddressBookConfig(PluginConfig):
    entries: Dict[str, AddressType] = {}


class AddressBook(ManagerAccessMixin):
    @property
    def global_config_file(self) -> Path:
        return self.config_manager.DATA_FOLDER / "addressbook.json"

    @property
    def global_config(self) -> Dict[str, AddressType]:
        if self.global_config_file.exists():
            global_config_raw_dict = json.loads(self.global_config_file.read_text())
            return {
                k: self.provider.network.ecosystem.decode_address(v)
                for k, v in global_config_raw_dict["entries"].items()
            }
        return {}

    @property
    def config(self) -> AddressBookConfig:
        return self.config_manager.get_config("addressbook")  # type: ignore

    @property
    def registry(self) -> Dict[str, AddressType]:
        registry = self.global_config
        registry.update(self.config.entries)
        return registry

    @property
    def aliases(self) -> Iterator[str]:
        for alias in self.registry:
            yield alias

    def __contains__(self, alias: str):
        return alias in self.aliases

    def __getitem__(self, alias: str) -> AddressType:
        if alias not in self.aliases:
            raise IndexError(f"Alias '{alias}' not in addressbook.")

        return self.registry[alias]

    def set_global_entry(self, alias: str, address: AddressType):
        if alias in self.aliases:
            raise Exception()

        global_config = self.global_config
        global_config[alias] = self.provider.network.ecosystem.decode_address(address)
        self.global_config_file.write_text(json.dumps({"entries": global_config}))


addressbook = AddressBook()
