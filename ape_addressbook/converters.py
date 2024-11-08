from typing import TYPE_CHECKING, Any

from ape.api.convert import ConverterAPI

from ape_addressbook import addressbook

if TYPE_CHECKING:
    from ape.types import AddressType


class AddressBookConverter(ConverterAPI):
    def is_convertible(self, value: Any) -> bool:
        return isinstance(value, str) and value in addressbook

    def convert(self, alias: str) -> "AddressType":
        return addressbook[alias]
