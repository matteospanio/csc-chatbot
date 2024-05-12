from pathlib import Path

import toml
from click.testing import CliRunner

from chatbot.cli.app import chatbot


class TestCLI:
    runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(chatbot, ["--help"])
        assert result.exit_code == 0
        assert "Usage: chatbot [OPTIONS] COMMAND [ARGS]..." in result.output
        assert "Manage the chatbot with memories." in result.output
        assert "Options:" in result.output
        assert "--help" in result.output
        assert "--config" in result.output
        assert "--version" in result.output
        assert "Commands:" in result.output

    def test_version(self):
        result = self.runner.invoke(chatbot, ["--version"])
        assert result.exit_code == 0
        with Path("pyproject.toml").open() as f:
            pyproject = toml.load(f)
            assert (
                f"chatbot, version {pyproject['tool']['poetry']['version']}"
                in result.output
            )

    def test_configure(self):
        result = self.runner.invoke(chatbot, ["configure"])
        assert result.exit_code == 0
        assert "Usage: chatbot configure [OPTIONS]" in result.output

    def test_show_configure(self):
        result = self.runner.invoke(chatbot, ["configure", "show"])
        assert result.exit_code == 0
        assert "chatbot.chat.sys-prompt" in result.output
        assert "{context}" in result.output
