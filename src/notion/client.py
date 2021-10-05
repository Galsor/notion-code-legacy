import logging
from typing import List

import requests
from pydantic import BaseModel

from src.notion.config import NotionConfig
from src.notion.database import CodeCommentNotionDatabase
from src.parser.record import CodeRecord

logger = logging.getLogger(__name__)


class CommentItem(BaseModel):
    type: str
    comment: str
    code: str
    filename: str
    filepath: str
    line: int

    @property
    def valid_json(self):
        return {}


class NotionClient:
    """Provides connectivity utils enabling interaction with Notion.so"""

    _config: NotionConfig

    def __init__(self, config: NotionConfig = None):
        self._config = config if config is not None else NotionConfig()
        self.default_headers = {
            "Authorization": f"Bearer {self._config.NOTION_KEY}",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json",
        }

    def retrieve_db(self, db_id: str) -> dict:
        """GET request enabling to collect database object regarding its id.
        More info on database object: https://developers.notion.com/reference/database

        :param db_id: str
            The ID of the database
        :return: json
            The response body
        """
        response = requests.get(
            f"{self._config.ROOT_URL}/databases/{db_id}", headers=self.default_headers
        )
        if response.status_code == 200:
            json_response = response.json()
            return json_response
        elif response.status_code == 404:
            raise ValueError(
                f"[{response.status_code}] Database {db_id} doesn't exist,\
             or your Notion's integration doesn't have access to the database."
            )
        else:
            raise ConnectionError(
                f"[{response.status_code}] Impossible to Retieve db {db_id}.\
             Response body: {response.json()}"
            )

    def query_db(self, db_id: str, data: dict) -> dict:
        """POST request to query a given data base
        https://developers.notion.com/reference/post-database-query
        :param db_id: str
            The database id to query
        :param data: dict
            The request body.
            data can contain :
            - 'filter': json
                When supplied, limits which pages are returned based on the filter conditions.
            - 'sorts': array
                When supplied, orders the results based on the provided sort criteria.
            - 'start_cursor': string
                When supplied, returns a page of results starting after the cursor provided.
                If not supplied, this endpoint will return the first page of results.
            - 'page_size': int32
                The number of items from the full list desired in the response. Maximum: 100

        :return: json
            Response body
        """
        response = requests.post(
            f"{self._config.ROOT_URL}/databases/{db_id}/query",
            headers=self.default_headers,
            data=data,
        )

        if response.status_code == 200:
            logger.info(f"[{response.status_code}] Successfully queried {db_id}")
            json_response = response.json()
            return json_response
        elif response.status_code == 404:
            raise ValueError(
                f"[{response.status_code}] Database {db_id} doesn't exist,\
                    or your Notion's integration doesn't have access to the database."
            )
        else:
            raise ConnectionError(
                f"[{response.status_code}] Impossible to Retieve db {db_id}.\
            \nResponse body: {response.json()}"
            )

        return json_response

    def update_database(self, db_id: str, data: dict) -> dict:
        response = requests.patch(
            f"{self._config.ROOT_URL}/databases/{db_id}",
            headers=self.default_headers,
            data=data,
        )

        if response.status_code == 200:
            logger.info(f"[{response.status_code}] Successfully updated  {db_id}")
            json_response = response.json()
            return json_response
        elif response.status_code == 404:
            raise ValueError(
                f"[{response.status_code}] Database {db_id} doesn't exist,\
                    or your Notion's integration doesn't have access to the database."
            )
        else:
            raise ConnectionError(
                f"[{response.status_code}] Impossible to Retieve db {db_id}.\
            \nResponse body: {response.json()}"
            )

    def create_page(self, db_id: str, data: dict) -> dict:
        response = requests.post(
            f"{self._config.ROOT_URL}/pages", headers=self.default_headers, data=data
        )

        if response.status_code == 200:
            logger.info(f"[{response.status_code}] Successfully queried {db_id}")
            json_response = response.json()
            return json_response
        elif response.status_code == 404:
            raise ValueError(
                f"[{response.status_code}] Database {db_id} doesn't exist,\
                    or your Notion's integration doesn't have access to the database."
            )
        else:
            raise ConnectionError(
                f"[{response.status_code}] Impossible to Retieve db {db_id}.\
            \nResponse body: {response.json()}"
            )

        return json_response


def inject_code_records_in_database(
    ndb: CodeCommentNotionDatabase, parsing_results: List[CodeRecord]
):
    for record in parsing_results:
        ndb.add_item(record)
        # FIXME for debug purpose
        break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    db_id = NotionConfig().NOTION_DATABASE_ID_LIST[0]
    ndb = CodeCommentNotionDatabase(db_id)
    from pprint import pprint

    pprint(ndb.properties)

    from src.parser.code_analyser import run_static_analysis

    records_list = run_static_analysis(".")
    print(records_list)
    inject_code_records_in_database(ndb, records_list)
