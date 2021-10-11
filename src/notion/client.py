from typing import Optional
import functools
import logging
from omegaconf import DictConfig
from notion_client import Client, APIResponseError, APIErrorCode
import httpx
import re

from .config import NotionConfig


logger = logging.getLogger(__name__)


def notion_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                logging.error(f"An error occured while calling {func.__name__} with arguments {args} {kwargs}")
                raise APIResponseError
            else:
                logging.exception(error)
        except httpx.ConnectError as connection_error:
            logger.exception(connection_error)
    return wrapper


class NotionClient:

    def __init__(self, auth, config: DictConfig=None):
        if config is None:
            self._config = NotionConfig()
        else:
            self._config = NotionConfig(ROOT_URL=config.ROOT_URL, LOG_LEVEL=config.LOG_LEVEL)
        try:
            self._client = Client(auth=auth, log_level=self._config.LOG_LEVEL)
            self._test_connection()
        except httpx.ConnectError as e:
            logger.warning(repr(e))
            print(str(e))
            if re.match(r".*SSL.*", str(e)) is not None:
                logger.warning("Setting connection without SSL verification")
                try:
                    logger.info("Initializing a new Notion Client with no ssl verifications")
                    self._client = Client(auth=auth,
                                          log_level=self._config.LOG_LEVEL,
                                          client=httpx.Client(verify=False)
                                          )
                    self._test_connection()
                except httpx.ConnectError as e_bis:
                    raise e_bis
        self._test_connection()
        logger.info("Notion client initialized")

    def _test_connection(self) -> None:
        assert self._client.users.me()

    @notion_request
    def retrieve_bot_user(self) -> dict:
        return self._client.users.me()

    @notion_request
    def retrieve_users_list(self) -> list:
        return self._client.users.list()["results"]

    @notion_request
    def retrieve_db(self, database_id: str):
        return self._client.databases.retrieve(database_id=database_id)

    @notion_request
    def query_db(self, database_id: str,
                 filters: Optional[dict] = None,
                 sorts: Optional[dict] = None,
                 start_cursor: Optional[str] = None,
                 page_size: Optional[int] = None
                 ):
        """POST request to query a given data base
        https://developers.notion.com/reference/post-database-query
        :param database_id: str
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
        body = {k: v for k, v in locals().items() if v is not None}
        logger.info(f" Database query based on body: {body}")
        return self.databases.query(**body)

    @notion_request
    def add_page(self, database_id: str, properties: dict, children: dict):
        return self._client.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )

    @notion_request
    def delete_page(self):
        #TODO
        pass