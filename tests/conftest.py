import pytest
import ape
import tempfile

from ape.managers.config import CONFIG_FILE_NAME
from ape_addressbook import addressbook


APE_CONFIG = r"""
addressbook:
  entries:
    friend_from_config_with_quotes: '0xBc8563cb0eeDbd1b95CCafD0c156e2daf5E18c29'
    friend_from_config_without_quotes: 0x1fC1FcEccD0d0cf092Dd11465f2e9Ce6BE3F62ac
"""


@pytest.fixture(autouse=True, scope="session")
def madeup_project_and_data_folder():
    """
    Prevents actually affecting global addressbook
    and sets a temporary project.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        with ape.config.using_project(temp_dir) as project:

            # Create the config file with address entries.
            config_file = project.path / CONFIG_FILE_NAME
            config_file.touch()
            config_file.write_text(APE_CONFIG)

            # Set the data folder to a temp dir as well so we can
            # create global entries.
            original = ape.config.DATA_FOLDER
            ape.config.DATA_FOLDER = tempfile.mkdtemp()

            yield

            # Clean up.
            ape.config.DATA_FOLDER = original
            if config_file.is_file():
                config_file.unlink()


@pytest.fixture
def alias():
    return "my_friends_address"


@pytest.fixture
def address():
    return "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"


@pytest.fixture
def addressbook_with_one_entry(alias, address):
    addressbook.set_global_entry(alias, address)
    yield addressbook
