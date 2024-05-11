from pathlib import Path

from chatbot import config


def test_create_default(default_config_fixture):
    with Path(default_config_fixture / config.CONFIG_FILE).open() as f:
        content = f.read()
        assert """# This is the chatbot configuration file.""" in content
