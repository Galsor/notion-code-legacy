import os
from typing import Optional
import logging
from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


@dataclass
class NotionConfig:
    ROOT_URL: Optional[str] = "https://api.notion.com/v1"
    #NOTION_DATABASE_ID_LIST: List[str] = [os.environ.get("NOTION_DATABASE_ID")]
    LOG_LEVEL: Optional[int] = logging.INFO

def register_notion_config() -> None:
    cs = ConfigStore.instance()
    cs.store(group="notion", name="config", node=NotionConfig)