from typing import Any

from ape.api.convert import ConverterAPI
from ape.types import AddressType

from .addressbook import addressbook


class AddressBookConverter(ConverterAPI):
    def is_convertible(self, value: Any) -> bool:
        return isinstance(value, str) and value in addressbook

    def convert(self, alias: str) -> AddressType:
        return addressbook[alias]
