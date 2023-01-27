from ape_addressbook import addressbook


def test_aliases(addressbook_with_one_entry, alias, address):
    addressbook.set_global_entry(alias, address)
    assert list(addressbook.aliases) == [alias]
