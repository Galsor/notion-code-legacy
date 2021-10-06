import pytest

from ..conftest import test_filepath
from src.parser.code_analyser import AnalysedFile, run_static_analysis
from src.utils.types import CommentTypes
from src.parser.record import CodeRecord


@pytest.fixture
def testfile_comment_count() -> dict:
    count_dict = {}
    for comment_type in list(CommentTypes):
        count_dict[comment_type] = 1
    return count_dict


@pytest.fixture
def testfile_records_count(testfile_comment_count) -> int:
    return sum(list(testfile_comment_count.values()))


@pytest.fixture(scope="module")
def analysed_file(test_filepath):
    return AnalysedFile(test_filepath)


def test_has_attributes(analysed_file):
    for type in list(CommentTypes):
        assert hasattr(analysed_file, type)


def test_comment_count(analysed_file, testfile_comment_count):
    for type in list(CommentTypes):
        assert len(analysed_file.__getattribute__(type)) == testfile_comment_count[type]


def test_to_dict(analysed_file, testfile_comment_count):
    af_dict = analysed_file.to_dict()
    assert isinstance(af_dict, dict)
    # Has all expected keys
    assert sorted(list(af_dict.keys())) == sorted([e.value for e in CommentTypes])
    # Contains CodeRecords
    assert all([isinstance(record, CodeRecord) for record_list in af_dict.values() for record in record_list])
    # Contains all CodeRecords
    for comment_type, record_list in af_dict.items():
        assert len(record_list) == testfile_comment_count[comment_type]


def test_to_list(analysed_file, testfile_records_count):
    assert len(analysed_file.to_list()) == testfile_records_count


def test_run_static_analysis(test_filepath, testfile_records_count):
    # With
    test_file_dir_path = test_filepath.parent

    # When
    res = run_static_analysis(test_file_dir_path)

    # Assert
    assert isinstance(res, list)
    assert len(res) == testfile_records_count
    assert isinstance(res[0], CodeRecord)
