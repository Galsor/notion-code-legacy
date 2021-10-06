import pytest

from ..conftest import test_filepath
from src.parser.record import CodeRecord


@pytest.fixture(scope="module")
def sample() -> dict:
    return {
        "comment": "#TODO something important",
        "type": "TODO",
        "code": " def foo():",
        }


@pytest.fixture(scope = "module")
def code_record(test_filepath, sample) -> CodeRecord:
    return CodeRecord(
        comment=sample["comment"],
        line=42,
        filepath=test_filepath
    )


def test_type(code_record):
    assert code_record.type == "TODO"


def test_empty_code(code_record):
    assert code_record.code == """"""


def test_record(code_record, sample):
    # Given
    code_line = sample["code"]
    # When
    code_record.record(code_line)
    # Then
    assert len(code_record._code) == 1
    assert code_record.code == code_line


def test_record_filepath(code_record, test_filepath):
    assert code_record.filepath == str(test_filepath)


def test_filename(code_record, test_filepath):
    assert code_record.filename == test_filepath.name


def test_to_dict(code_record, test_filepath, sample):
    assert code_record.to_dict() == {
        "comment": sample["comment"],
        "line": 42,
        "filepath": str(test_filepath),
        "filename": test_filepath.name,
        "code": sample["code"],
        "type": "TODO",
    }