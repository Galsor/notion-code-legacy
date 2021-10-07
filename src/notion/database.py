import json
import logging
from datetime import datetime

from src.notion.old_client import NotionClient
from src.notion.config import NotionConfig
from src.parser.record import CodeRecord

logger = logging.getLogger(__name__)


class NotionDatabase:
    """Database instance. Providing utils to interact with remote notion DB"""

    database_id: str
    created_time: datetime
    last_edited_time: datetime
    properties: dict
    url: str
    _connector: NotionClient
    _config: NotionConfig

    def __init__(self, database_id: str = None) -> None:
        self._config = NotionConfig()
        if database_id is not None:
            self.database_id = database_id
        else:
            try:
                self.database_id = os.environ["NOTION_DATABASE_ID"]
            except KeyError:
                raise ValueError(
                    "No database_id provided neither found in environments variables."
                )
        self._connector = NotionClient()
        self._sync()

    def _sync(self) -> None:
        json = self._connector.retrieve_db(self.database_id)
        self.database_id = json["id"]  # Fail if not
        self.created_time = json.get("created_time")
        self.last_edited_time = json.get("last_edited_time")
        self.properties = json.get("properties")
        self.url = json.get("url")
        try:
            self.__name__ = json["title"][0]["plain_text"]
        except KeyError:
            logger.warning("Impossible to retrieve database title plain_text attribute")
        logger.info(f"Notion database synced with remote {self.__dict__}")

    def add_item(self, data: dict) -> None:
        print(f"trying to add: {data} ")
        json_response = self._connector.create_page(self.database_id, data)
        print(json_response)
        return json_response


class CodeCommentNotionDatabase(NotionDatabase):
    def add_item(self, record: CodeRecord) -> None:
        print(f"trying to add: {record} ")
        data = self._create_page_creation_body(record)
        json_response = self._connector.create_page(self.database_id, data)
        print(json_response)
        return json_response

    # FIXME JSON payload is not valid. Set it as string
    # Investigate jsonschema or Notion python package
    def _create_page_creation_body(self, record: CodeRecord) -> dict:
        return json.dumps(
            {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "comment": {"title": {"text": {"content": record.comment}}},
                },
            }
        )


"""                 
                     "filename": {
                         'text':[
                             {"text": {"content": record.filename}}
                        ]
                     },
                     "filepath": {
                         'text':[
                             {"text": {"content": record.filepath}}
                        ]
                     },
                     "line": {
                         'number': record.line
                     },
                     "type": {
                         'text':[
                             {"text": {"content": record.filepath}}
                         ]
                     },
                "children": [
                     {
                         "object": "block",
                         "type": "code",
                         "code": {
                             "text": [{
                                 "type": "text",
                                 "text": {
                                     "content": record.code
                                 }
                         }],
                         "language": "python"
                        }
                     }
                 ]"""
