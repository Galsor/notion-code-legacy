import pytest
from shutil import copyfile
from pathlib import Path


@pytest.fixture(scope="session")
def test_filepath(tmpdir_factory):
    root_file_path = Path.cwd() / "test" / "unit" / "mock_files" / "dumm.py"
    tmp_file_path = tmpdir_factory.mktemp("mock_files").join("dumm.py")
    copyfile(root_file_path, tmp_file_path)
    return Path(tmp_file_path)