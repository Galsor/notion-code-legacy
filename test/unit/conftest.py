import pytest
from pathlib import Path
import os


@pytest.fixture(scope="session")
def test_filepath():
    #path = Path.cwd() / "mock_files" / "dumm.py"
    path = os.path.join(
        os.path.join(
            os.path.dirname(__file__),
            "mock_files"),
        "dumm.py")
    return path