import pytest
from pathlib import Path

@pytest.fixture(scope = "session")
def test_filepath() -> Path:
    return Path("../../mock_files/dumm.py")
