from hydra import initialize, compose
import pytest


@pytest.fixture(scope="session")
def mock_config():
    with initialize(config_path="."):
        cfg = compose(config_name="test_config", overrides=["app.user=test_user"])
    return cfg


def test_mock_config(mock_config) -> None:
        assert mock_config == {
            "app": {"user": "test_user", "num1": 10, "num2": 20},
            "db": {"host": "localhost", "port": 3306},
        }
