"""Configuration constants for the chatbot."""

from pathlib import Path

import toml

from chatbot.utils import depth_set

CONFIG_FILE = Path("config.toml")

PROMPT = """You are a very patient and funny helper, you attend the Center for Computational Sonology at the University of Padua and you know all the other people who work there. \
Your task is to provide information about the Computational Sonology Center, the people who are part of it and the plans for carrying out a thesis at the Center, don't answer questions about other topics. \
You always start an answer by telling a joke about the Center or the people who work there.
Answer the user's questions based on the below context, always answer in the language in which you are spoken to.
If the context does not contain information to answer the user's question, ask the user to provide more information in a funny way.

<context>
{context}
</context>
"""  # noqa: E501


DEFAULT_CONFIG = {
    "chatbot": {
        "openai_api_key": "",
        "embedding": "text-embedding-3-large",
        "chat": {"sys-prompt": PROMPT, "temperature": 0.6, "model": "gpt-4-turbo"},
        "ingest": {"chunk_size": 2500, "overlap": 150},
    },
}


def create_default(folder: Path):
    """Create the default configuration file."""
    comments = """# This is the chatbot configuration file.
#
# Modify the following fields as you want.
# This configuration file is written following the TOML syntax, for a quick refresher
# see https://toml.io/en/.
#
# To write multiline strings you can use triple quotes \""":
#   sys_prompt=\"""You are a multiline prompt
# useful when you want to write a really long prompt
# that end only after a few lines\"""\n
"""

    toml_config = toml.dumps(DEFAULT_CONFIG)
    with Path(folder / CONFIG_FILE).open("w") as f:
        f.write(comments + toml_config)


def load_config(folder: Path):
    """Load the configuration file."""
    with Path(folder / CONFIG_FILE).open("r") as f:
        return toml.load(f)


def set_config_value(folder: Path, key: str, value: str):
    """Set a configuration value."""
    config = load_config(folder)
    keys = key.split(".")
    depth_set(config, keys, value)
    with Path(folder / CONFIG_FILE).open("w") as f:
        toml.dump(config, f)
