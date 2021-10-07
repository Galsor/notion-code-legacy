import os
from typing import List
import logging

from pydantic import BaseModel


class NotionConfig(BaseModel):
    ROOT_URL: str = "https://api.notion.com/v1"
    NOTION_KEY: str = os.environ.get("NOTION_KEY")
    NOTION_DATABASE_ID_LIST: List[str] = [os.environ.get("NOTION_DATABASE_ID")]
    LOG_LEVEL: int = logging.INFO
