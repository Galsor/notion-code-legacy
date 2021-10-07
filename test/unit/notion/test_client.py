import os
import pytest

from src.notion.client import NotionClient
from src.notion.config import NotionConfig

@pytest.fixture(scope="session")
def mock_notion_config():
    return NotionConfig(
        NOTION_KE=os.environ["notion_key_test"],

    )



@pytest.fixture(scope="session")
def mock_notion_client(mock_notion_config):
    return NotionClient()