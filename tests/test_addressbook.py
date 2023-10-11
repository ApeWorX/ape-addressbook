from ape_addressbook import addressbook


def test_config(project_alias_unchecksummed, project_alias_no_quotes, project_address):
    """
    This test shows that we are able to read values from a
    project's config as well as handle checksumming them if needbe.
    """

    actual = addressbook.config.entries
    assert len(actual) == 2
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_no_quotes] == project_address


def test_registry(
    project_alias_unchecksummed,
    project_alias_no_quotes,
    project_address,
):
    actual = addressbook.registry
    assert len(actual) == 2
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_no_quotes] == project_address


def test_aliases(project_alias_unchecksummed, project_alias_no_quotes):
    """
    The aliases includes both project and global addresses.
    """

    assert list(addressbook.aliases) == [
        project_alias_unchecksummed,
        project_alias_no_quotes,
    ]


def test_contains(
    project_alias_unchecksummed,
    project_alias_no_quotes,
):
    assert project_alias_unchecksummed in addressbook
    assert project_alias_no_quotes in addressbook


def test_get_item(
    project_alias_unchecksummed,
    project_address,
    project_alias_no_quotes,
):
    assert addressbook[project_alias_unchecksummed] == project_address
    assert addressbook[project_alias_no_quotes] == project_address
