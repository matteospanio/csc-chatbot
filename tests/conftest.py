import tempfile
from pathlib import Path

import pytest

from chatbot import config


@pytest.fixture()
def tmp_config():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        yield tmp_path


@pytest.fixture()
def default_config_fixture(tmp_config):
    config.create_default(tmp_config)
    return tmp_config
