import logging
import token as token_types
import tokenize
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Union

from src.parser.record import CodeRecord
from src.utils.types import CommentTypes

logger = logging.getLogger(__name__)


class AnalysedFile:
    _path: Union[str, Path]
    _records: List[CodeRecord]

    def __init__(self, filepath: Union[str, Path]):
        self._path = Path(filepath)
        self._records = []
        self._analyse_tokens()
        self._configure_properties()

    def _analyse_tokens(self):
        with tokenize.open(self._path) as f:
            tokens = tokenize.generate_tokens(f.readline)
            logger.debug(f"Starting analysis of {self._path.name}")
            record = None
            next_skip = False
            for token in tokens:
                logger.debug(token)

                # Skip newlines following comments as they stop the recording process
                if next_skip and token.type == token_types.NL:
                    next_skip = False
                    continue
                elif next_skip and token.type != token_types.NL:
                    next_skip = False

                # Recording process
                if token.type == token_types.COMMENT and record is None:
                    logger.debug("Start code recording")
                    record = CodeRecord(
                        filepath=self._path, line=token.start[0], comment=token.string
                    )
                    if record.type is not None:
                        # Next value is "NL" which is an end of part and a stopping trigger
                        next_skip = True
                    else:
                        # No CommentType found in comment, drop record
                        record = None
                elif token.type == token_types.COMMENT and not record.code:
                    # No code has been registered and a new comment appear.
                    # So the comment is pursuing after a newline.
                    record.comment += token.string
                    next_skip = True
                elif record is not None and token.type in [
                    token_types.NL,
                    token_types.ENDMARKER,
                ]:
                    logger.debug("End code recording")
                    self._records.append(record)
                    record = None
                elif record is not None:
                    record.record(token.string)

    def _configure_properties(self):
        for comment_type in CommentTypes:
            record_list = [
                r for r in self._records if CommentTypes(r.type) is comment_type
            ]
            setattr(self, comment_type.value, record_list)

    def to_dict(self) -> Dict[str, List[CodeRecord]]:
        """
        Return a dictionary structure by filenames and comment type:
        { filename: {
                    commment_type: List[CodeRecord]
                    }}
        """
        return {
            attr: self.__getattribute__(attr)
            for attr in dir(self)
            if not attr.startswith("_")
            and not callable(self.__getattribute__(attr))
            and self.__getattribute__(attr)
        }

    def to_list(self) -> List[CodeRecord]:
        """Returns the list of CodeRecords collected in the file"""
        list_of_comment_types_list = [
            self.__getattribute__(attr)
            for attr in dir(self)
            if not attr.startswith("_")
            and not callable(self.__getattribute__(attr))
            and self.__getattribute__(attr)
        ]
        flatten_list = [r for r_list in list_of_comment_types_list for r in r_list]
        return flatten_list

    def is_empty(self):
        return len(self._records) == 0

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self.to_dict())


def run_static_analysis(starting_path: str) -> List[CodeRecord]:
    """
    Crawl the file tree recursivly and analyse each file
    looking for comments including the keywords described in CommentTypes

    :param starting_path: str
        The path where the exploration starts.
    :return: dict
        List of CodeRecords collected after analysing all files.
    """
    res = []
    path = Path(starting_path)
    for python_file_path in path.rglob("**/*.py"):
        try:
            af = AnalysedFile(python_file_path)
            if not af.is_empty():
                res.extend(af.to_list())
        except Exception as e:
            logger.error(f"An error occured while analysing {python_file_path}")
            logger.error(repr(e))
    return res


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    # pprint(run_static_analysis("../../ddst"))
    pprint(run_static_analysis("."))
