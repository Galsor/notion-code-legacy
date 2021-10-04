import re
import inspect
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict

from src.utils.types import CommentTypes

@dataclass
class CodeRecord:
    comment: str
    line: int
    filepath: Path
    _filepath: Path = field(init=False, repr=False)
    _code: List = None

    @property
    def type(self) -> str:
        comment_types_list = [e.value for e in CommentTypes]
        pattern = re.compile("^(?:\#\s*)(" + "|".join(comment_types_list) + ")")
        match = pattern.match(self.comment)
        if match is not None:
            match_type = match.group(1)
            return CommentTypes(match_type).value

    @property
    def code(self) -> str:
        if self._code is not None:
            return """ """.join(self._code)
        else:
            return """"""

    @property
    def filename(self) -> str:
        return self._filepath.name

    @property
    def filepath(self) -> str:
        return str(self._filepath)

    @filepath.setter
    def filepath(self, path: Path) -> None:
        self._filepath = path

    def record(self, code: str) -> None:
        if self._code is None:
            self._code = [code]
        else:
            self._code.append(code)

    def to_dict(self) -> Dict[str,str]:
        return {attr: self.__getattribute__(attr) for attr in dir(self) if
                not attr.startswith("_") and not callable(self.__getattribute__(attr))}

    @classmethod
    def get_schema(cls):
        #FIXME some attributes are missing
        # This function would enable to update table with missing fields
        attributes = inspect.getmembers(cls, lambda attr: not(inspect.isroutine(attr)))
        return [attr[0] for attr in attributes if not attr[0].startswith("_")]

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self.to_dict())
