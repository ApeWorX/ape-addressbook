from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from .addresses import AddressBookConfig

    return AddressBookConfig


@plugins.register(plugins.ConversionPlugin)
def converters():
    from ape.types import AddressType

    from .converters import AddressBookConverter

    return AddressType, AddressBookConverter


def __getattr__(name: str):
    if name == "addressbook":
        from ape_addressbook.addresses import addressbook

        return addressbook

    import ape_addressbook.addresses as module

    return getattr(module, name)


___all__ = ["addressbook"]
