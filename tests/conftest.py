import ape
import pytest
from ape.managers.config import CONFIG_FILE_NAME
from ape.utils import create_tempdir
from eth_utils import to_checksum_address

PROJECT_ALIAS_UNCHECKSUMMED = "project_entry_quotes"
PROJECT_ALIAS_NO_QUOTES = "project_entry_no_quotes"
PROJECT_ADDRESS_NON_CHECKSUMMED = "0xbc8563cb0eedbd1b95ccafd0c156e2daf5e18c29"
PROJECT_ADDRESS = to_checksum_address(PROJECT_ADDRESS_NON_CHECKSUMMED)

APE_CONFIG = rf"""
addressbook:
    # This address purposely is not checksummed.
    {PROJECT_ALIAS_UNCHECKSUMMED}: '{PROJECT_ADDRESS_NON_CHECKSUMMED}'

    # This address is read-in as an int since it has no quotes.
    {PROJECT_ALIAS_NO_QUOTES}: {PROJECT_ADDRESS}
"""


@pytest.fixture(autouse=True, scope="session")
def madeup_project():
    """
    Prevents actually affecting global addressbook
    and sets a temporary project.
    """

    with create_tempdir() as path:
        # Create the config file with address entries.
        config_file = path / CONFIG_FILE_NAME
        config_file.touch()
        config_file.write_text(APE_CONFIG)

        with ape.config.using_project(path):
            yield

        # Clean up.
        if config_file.is_file():
            config_file.unlink()


@pytest.fixture
def project_alias_unchecksummed():
    return PROJECT_ALIAS_UNCHECKSUMMED


@pytest.fixture
def project_alias_no_quotes():
    return PROJECT_ALIAS_NO_QUOTES


@pytest.fixture
def project_address():
    return PROJECT_ADDRESS
