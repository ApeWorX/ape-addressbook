import ape
import pytest
from eth_utils import to_checksum_address

PROJECT_ALIAS_UNCHECKSUMMED = "project_entry_quotes"
PROJECT_ALIAS_INT = "project_entry_no_quotes"
PROJECT_ADDRESS_NON_CHECKSUMMED = "0xbc8563cb0eedbd1b95ccafd0c156e2daf5e18c29"
PROJECT_ADDRESS = to_checksum_address(PROJECT_ADDRESS_NON_CHECKSUMMED)
CONFIG_ADDRESSBOOK = {
    # This address purposely is not checksummed.
    PROJECT_ALIAS_UNCHECKSUMMED: PROJECT_ADDRESS_NON_CHECKSUMMED,
    PROJECT_ALIAS_INT: int(PROJECT_ADDRESS, 16),
}


@pytest.fixture(autouse=True, scope="session")
def project():
    with ape.project.temp_config(addressbook=CONFIG_ADDRESSBOOK):
        yield ape.project


@pytest.fixture
def project_alias_unchecksummed():
    return PROJECT_ALIAS_UNCHECKSUMMED


@pytest.fixture
def project_alias_int():
    return PROJECT_ALIAS_INT


@pytest.fixture
def project_address():
    return PROJECT_ADDRESS
