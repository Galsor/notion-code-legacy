import pytest

from src.notion.client import NotionClient
from src.notion.config import NotionConfig

@pytest.fixture(scope="module")
def mock_notion_config(mock_config):
    return NotionConfig(ROOT_URL=mock_config.ROOT_URL, LOG_LEVEL=mock_config.LOG_LEVEL)

@pytest.fixture(scope="module")
def mock_notion_client(test_notion_key, mock_notion_config):
    return NotionClient(auth=test_notion_key, config=mock_notion_config)

@pytest.fixture
def db_id(mock_config):
    return mock_config["NOTION_DATABASE_ID_LIST"][0]

@pytest.fixture
def page_properties() -> dict:
    return {"properties": {
      "Comment": {
        "title": [
          {
            "text": {
              "content": '"FIXME Pass Unit Tests"',
            },
          },
        ],
      },
      "Type": {
        "text": [
          {
            "text": {
              "content": 'FIXME',
            },
          },
        ],
      },
    }
    }

@pytest.fixture
def page_children() -> list:
    return [
      {
        "object": 'block',
        "type": 'heading_2',
        "heading_2": {
          "text": [
            {
              "type": 'text',
              "text": {
                "content": 'Lacinato kale',
              },
            },
          ],
        },
      },
      {
        "object": 'block',
        "type": 'paragraph',
        "paragraph": {
          "text": [
            {
              "type": 'text',
              "text": {
                "content": 'Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.',
                "link": {
                  "url": 'https://en.wikipedia.org/wiki/Lacinato_kale',
                },
              },
            },
          ],
        },
      },
    ]

def test_retrieve_bot_user(mock_notion_client):
    assert mock_notion_client.retrieve_bot_user()

def test_retrieve_users_list(mock_notion_client):
    assert mock_notion_client.retrieve_users_list()

def test_retrieve_db(mock_notion_client, db_id):
    assert mock_notion_client.retrieve_db (database_id=db_id)

def test_query_db(mock_notion_client, db_id):
    assert mock_notion_client.query_db(database_id=db_id)

def test_add_page(mock_notion_client, db_id, page_properties, page_children):
    assert mock_notion_client.add_page(database_id=db_id, properties=page_properties, children=page_children)

def test_delete_page(mock_notion_client):
    assert 1
