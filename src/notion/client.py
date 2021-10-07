from typing import Optional
import functools
import logging

from notion_client import Client, APIResponseError, APIErrorCode
from .config import NotionConfig


logger = logging.getLogger(__name__)

class NotionClient(Client):

    def __init__(self, auth=None, config=None):
        if config is None:
            self._config = NotionConfig()
        else:
            self._config = config

        if auth is None and self._config.NOTION_KEY is None:
            raise ValueError("NotionClient requires auth information to connect the API."\
                             "Please export NOTION_KEY value in your environment variables"\
                             "or add it in NotionClient auth argument.")

        elif auth is not None:
            # Overide NOTION KEY
            self._config.NOTION_KEY = auth

        super(NotionClient, self).__init__(auth=self._config.NOTION_KEY,
                                           log_level=self._config.LOG_LEVEL)


    @notion_request
    def retrieve_db(self, database_id: str):
        return self.databases.retieve(database_id=database_id)

    @notion_request
    def query_db(self, database_id: str, filters: Optional[dict] = {}):
        return self.databases.query(**{
            "databse_id": database_id,
            "filter": filters
        })

    @notion_request
    def add_page(self, database_id: str, properties: dict, children: dict):
        return self.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )


def notion_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                logging.error(f"An error occured while calling {func.__name__} with arguments {*args} {**kwargs}")
                raise APIResponseError
            else:
                logging.exception(error)
    return wrapper