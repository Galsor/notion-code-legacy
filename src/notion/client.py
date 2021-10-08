from typing import Optional
import functools
import logging
from omegaconf import DictConfig
from notion_client import Client, APIResponseError, APIErrorCode

from .config import NotionConfig


logger = logging.getLogger(__name__)


def notion_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                logging.error(f"An error occured while calling {func.__name__} with arguments {args} {kwargs}")
                raise APIResponseError
            else:
                logging.exception(error)
    return wrapper


class NotionClient(Client):

    def __init__(self, auth, config: DictConfig=None):
        if config is None:
            self._config = NotionConfig()
        else:
            self._config = NotionConfig(ROOT_URL=config.ROOT_URL, LOG_LEVEL=config.LOG_LEVEL)
        super(NotionClient, self).__init__(auth=auth,
                                           log_level=self._config.LOG_LEVEL)
        logger.info("Notion client initilized")


    @notion_request
    def retrieve_db(self, database_id: str):
        return self.databases.retieve(database_id=database_id)

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
        return self.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )