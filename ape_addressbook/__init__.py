from ape import plugins

from .addressbook import AddressBook as _AddressBook
from .addressbook import AddressBookConfig


@plugins.register(plugins.Config)
def config_class():
    return AddressBookConfig


addressbook = _AddressBook()
