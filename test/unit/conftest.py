import pytest
from shutil import copyfile
from pathlib import Path
from dotenv import load_dotenv
import os
from hydra import initialize, compose


@pytest.fixture(scope="session")
def test_notion_key():
    load_dotenv()
    key = os.environ["TEST_NOTION_KEY"]
    assert key
    return key

@pytest.fixture(scope="session")
def mock_config(test_notion_key):
    with initialize(config_path="."):
        cfg = compose(config_name="test_config")
    return cfg

@pytest.fixture(scope="session")
def test_filepath(tmpdir_factory):
    root_file_path = Path.cwd() / "test" / "unit" / "mock_files" / "dumm.py"
    tmp_file_path = tmpdir_factory.mktemp("mock_files").join("dumm.py")
    copyfile(root_file_path, tmp_file_path)
    return Path(tmp_file_path)
