import logging
import os
import hydra
from omegaconf import DictConfig, OmegaConf
from dotenv import load_dotenv
import functools

from notion.client import NotionClient

logger = logging.getLogger(__name__)


def load_env(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv()
        return func(*args, **kwargs)
    return wrapper


@load_env
@hydra.main(config_path="../config", config_name="config")
def run_app(cfg: DictConfig):
    logging.basicConfig(level=cfg.LOG_LEVEL)
    logger.debug("Debug mode is turned on")
    logger.info(OmegaConf.to_yaml(cfg))
    nc = NotionClient(config=cfg, auth=os.environ.get("NOTION_KEY"))
    from pprint import pprint
    pprint(nc.retrieve_db("5fa76a72f4f84db1b46a46e0978c3b2c"))


if __name__ == "__main__":
    run_app()
