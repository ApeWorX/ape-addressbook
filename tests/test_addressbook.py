from ape_addressbook import addressbook


def test_config(book, project_alias_unchecksummed, project_alias_no_quotes, project_address):
    """
    This test shows that we are able to read values from a
    project's config as well as handle checksumming them if needbe.
    """

    actual = book.config.entries
    assert len(actual) == 2
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_no_quotes] == project_address


def test_registry(
    book,
    global_alias,
    project_alias_unchecksummed,
    project_alias_no_quotes,
    project_address,
    global_address,
):
    actual = book.registry
    assert len(actual) == 3
    assert actual[global_alias] == global_address
    assert actual[project_alias_unchecksummed] == project_address
    assert actual[project_alias_no_quotes] == project_address


def test_aliases(book, global_alias, project_alias_unchecksummed, project_alias_no_quotes):
    """
    The aliases includes both project and global addresses.
    """

    assert list(addressbook.aliases) == [
        global_alias,
        project_alias_unchecksummed,
        project_alias_no_quotes,
    ]


def test_contains(
    book,
    global_alias,
    global_address,
    project_alias_unchecksummed,
    project_address,
    project_alias_no_quotes,
):
    assert global_alias in book
    assert project_alias_unchecksummed in book
    assert project_alias_no_quotes in book


def test_get_item(
    book,
    global_alias,
    global_address,
    project_alias_unchecksummed,
    project_address,
    project_alias_no_quotes,
):
    assert book[global_alias] == global_address
    assert book[project_alias_unchecksummed] == project_address
    assert book[project_alias_no_quotes] == project_address
