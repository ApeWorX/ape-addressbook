import shutil
import tempfile
from pathlib import Path

import ape
import pytest
from ape.managers.config import CONFIG_FILE_NAME
from eth_utils import to_checksum_address

from ape_addressbook import addressbook

PROJECT_ALIAS_UNCHECKSUMMED = "project_entry_quotes"
PROJECT_ALIAS_NO_QUOTES = "project_entry_no_quotes"
PROJECT_ADDRESS_NON_CHECKSUMMED = "0xbc8563cb0eedbd1b95ccafd0c156e2daf5e18c29"
PROJECT_ADDRESS = to_checksum_address(PROJECT_ADDRESS_NON_CHECKSUMMED)

APE_CONFIG = rf"""
addressbook:
  entries:
    # This address purposely is not checksummed.
    {PROJECT_ALIAS_UNCHECKSUMMED}: '{PROJECT_ADDRESS_NON_CHECKSUMMED}'

    # This address is read-in as an int since it has no quotes.
    {PROJECT_ALIAS_NO_QUOTES}: {PROJECT_ADDRESS}
"""


@pytest.fixture(autouse=True, scope="session")
def madeup_project_and_data_folder():
    """
    Prevents actually affecting global addressbook
    and sets a temporary project.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the config file with address entries.
        path = Path(temp_dir)
        config_file = path / CONFIG_FILE_NAME
        config_file.touch()
        config_file.write_text(APE_CONFIG)

        # Set the data folder to a temp dir as well so we can
        # create global entries.
        original = ape.config.DATA_FOLDER
        data_folder = path / "data"
        data_folder.mkdir()
        ape.config.DATA_FOLDER = data_folder

        with ape.config.using_project(Path(temp_dir)):
            yield

        # Clean up.
        ape.config.DATA_FOLDER = original
        if config_file.is_file():
            config_file.unlink()
        if data_folder.is_dir():
            shutil.rmtree(data_folder)


@pytest.fixture
def global_alias():
    return "global_address"


@pytest.fixture
def global_address():
    return "0x2192f6112a026bce4047CeD2A16553Fd31E798B6"


@pytest.fixture
def project_alias_unchecksummed():
    return PROJECT_ALIAS_UNCHECKSUMMED


@pytest.fixture
def project_alias_no_quotes():
    return PROJECT_ALIAS_NO_QUOTES


@pytest.fixture
def project_address():
    return PROJECT_ADDRESS


@pytest.fixture
def book(global_alias, global_address):
    address = global_address.lower()  # Use lower to show checksum works.
    addressbook.set_global_entry(global_alias, address)

    yield addressbook

    if addressbook.global_config_file.is_file():
        addressbook.global_config_file.unlink()
