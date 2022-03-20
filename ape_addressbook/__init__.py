from ape import plugins
from ape.types import AddressType

from .addressbook import AddressBookConfig, addressbook  # noqa: F401
from .converters import AddressBookConverter


@plugins.register(plugins.Config)
def config_class():
    return AddressBookConfig


@plugins.register(plugins.ConversionPlugin)
def converters():
    return AddressType, AddressBookConverter


___all__ = [
    "addressbook",
]
