import pytest

from ..conftest import test_filepath
from src.parser.code_analyser import AnalysedFile, run_static_analysis
from src.utils.types import CommentTypes
from src.parser.record import CodeRecord

@pytest.fixture
def testfile_comment_count() -> dict:
    return {
        "TODO": 1,
        "FIXME": 1,
        "BUG": 1,
        }

@pytest.fixture(scope="module")
def analyed_file(test_filepath):
    return AnalysedFile(test_filepath)

def test_has_attributes(analyed_file):
    for type in list(CommentTypes):
        assert hasattr(analyed_file, type)

def test_comment_count(analyed_file, testfile_comment_count):
    for type in list(CommentTypes):
        assert len(analyed_file.__getattribute__(type))==testfile_comment_count[type]

def test_to_dict(analyed_file, testfile_comment_count):
    af_dict = analyed_file.to_dict()
    assert isinstance(af_dict, dict)
    # Has all expected keys
    assert list(af_dict.keys()) == list(CommentTypes)
    # Contains CodeRecords
    assert all([isinstance(record, CodeRecord) for record in af_dict.values()])
    # Contains all CodeRecords
    for comment_type, record_list in af_dict.values():
        assert len(record_list) == testfile_comment_count[comment_type]

def test_to_list(analyed_file, testfile_comment_count):
    comments_total_count = sum(testfile_comment_count.values())
    assert len(analyed_file.to_list()) == testfile_comment_count


def test_run_static_analysis(test_filepath):
    # With
    test_file_dir_path = test_filepath.parent

    # When
    res = run_static_analysis(test_file_dir_path)

    # Assert
    assert isinstance(res, list)
    assert len(res) == 1
    assert isinstance(res[0], CodeRecord)
