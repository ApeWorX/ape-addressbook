from ape_addressbook import addressbook


def test_config(project_alias_unchecksummed, project_alias_int, project_address):
    """
    This test shows that we are able to read values from a
    project's config as well as handle checksumming them if needbe.
    """

    actual = addressbook.config
    assert len(actual) == 2
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_int] == project_address


def test_registry(project_alias_unchecksummed, project_alias_int, project_address):
    actual = addressbook.registry
    assert len(actual) == 2
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_int] == project_address


def test_aliases(project_alias_unchecksummed, project_alias_int):
    """
    The aliases includes both project and global addresses.
    """

    actual = list(addressbook.aliases)
    expected = [project_alias_int, project_alias_unchecksummed]
    assert actual == expected


def test_contains(project_alias_unchecksummed, project_alias_int):
    assert project_alias_unchecksummed in addressbook
    assert project_alias_int in addressbook


def test_get_item(project_alias_unchecksummed, project_address, project_alias_int):
    assert addressbook[project_alias_unchecksummed] == project_address
    assert addressbook[project_alias_int] == project_address
