import logging

import hydra
from omegaconf import DictConfig, OmegaConf

logger = logging.getLogger(__name__)


@hydra.main(config_path="../config", config_name="config")
def run_app(cfg: DictConfig):
    logger.debug("Debug is printed")
    logger.info(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    run_app()
