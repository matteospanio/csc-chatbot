"""The main entry point for the chatbot CLI application."""

import logging
from pathlib import Path
from typing import Annotated

import click
import click_extra
from rich.console import Console
from rich.prompt import Confirm, Prompt

from chatbot.chat import main_loop
from chatbot.cli import __app_name__
from chatbot.cli.constants import HEADER, LICENSE
from chatbot.cli.custom_decorators import docstring_decorator
from chatbot.config import create_default, load_config, set_config_value
from chatbot.memory import create_memory
from chatbot.utils import flatten_dict

APP_DIR = Path(click.get_app_dir(__app_name__))


@click.group(
    context_settings={"show_default": True},
    epilog=LICENSE,
)
@click.version_option()
@click.help_option("-h", "--help")
@click.option(
    "-e",
    "--embedding",
    help="The model used to encode and retrieve embeddings.",
)
@click.option(
    "-api",
    "--openai-api-key",
    help="The OpenAI api key.",
)
@click_extra.verbosity_option
@click_extra.config_option
@click.pass_context
def chatbot(ctx: click.Context, embedding: str, openai_api_key: str) -> None:
    """Manage the chatbot with memories."""
    ctx.ensure_object(dict)
    ctx.obj["embedding"] = embedding

    logger = logging.getLogger("app_logger")
    logger.debug("API_KEY: %s", openai_api_key)

    if not APP_DIR.exists():
        APP_DIR.mkdir(parents=True)
        create_default(APP_DIR)
        logger.info("Configuration file created at %s/config.toml.", APP_DIR)

    if openai_api_key == "":
        openai_api_key = Prompt.ask("Insert OpenAI API key")
        if openai_api_key == "":
            logger.critical("OpenAI API key is has not been set correctly.")
            msg = "Invalid OpenAI API key"
            raise click.Abort(msg)
        if Confirm.ask("Do you want to save the OpenAI API key?"):
            set_config_value(APP_DIR, "chatbot.openai_api_key", openai_api_key)

    ctx.obj["openai_api_key"] = openai_api_key
    logger.debug("OpenAI API key set.")


@chatbot.command()
@click.help_option("-h", "--help")
@click.option("-m", "--model", help="The model to chat with.")
@click.option(
    "-t",
    "--temperature",
    help="The randomness of the model, ",
    type=click.FloatRange(
        min=0.0,
        max=1.0,
    ),
)
@click.option(
    "-s",
    "--sys-prompt",
    help="The prompt given to the model.",
)
@click.pass_context
def chat(
    ctx: click.Context,
    model: str,
    temperature: float,
    sys_prompt: str,
) -> None:
    """Chat with the chatbot."""
    embedding = ctx.obj["embedding"]
    api_key = ctx.obj["openai_api_key"]

    click.echo(HEADER)
    click.echo("Starting a chat session...")
    main_loop(
        model,
        embedding,
        temperature,
        sys_prompt,
        api_key,
    )


@chatbot.command()
@click.argument(
    "resource",
    type=click.Path(
        exists=True,
        path_type=Path,
        readable=True,
    ),
)
@click.option(
    "-f",
    "--file-format",
    type=click.Choice(["pdf", "web"]),
    help="The resource format type.",
)
@click.option(
    "--chunk-size",
    help="The number of chars for each chunk.",
    type=click.IntRange(min=0),
    metavar="<size>",
)
@click.option(
    "-o",
    "--overlap",
    help="The number of characters each chunk overlaps with the previous.",
    type=click.IntRange(min=0),
    metavar="<int>",
)
@click.help_option("-h", "--help")
@click.pass_context
@docstring_decorator(help_text="Setup the chatbot.")
def ingest(  # noqa: D103
    ctx: click.Context,
    resource: Annotated[
        Path,
        "The path to the resource (could be a file or a folder).",
    ],
    file_format: str,
    chunk_size: int,
    overlap: int,
) -> None:
    click.echo("Setting up the chatbot memories...")
    api_key = ctx.obj["openai_api_key"]
    create_memory(api_key, resource, file_format, chunk_size, overlap)


@chatbot.group()
@click.help_option("-h", "--help")
def configure() -> None:
    """Handle chatbot configuration."""


@configure.command()
@click.help_option("-h", "--help")
@click.argument("key", type=str)
@click.argument("value", type=str)
@docstring_decorator(
    help_text="Set a configuration value.\n\n"
    "Example: chatbot configure set chatbot.chat.temperature 0.7.",
)
def set(  # noqa: D103, A001
    key: Annotated[str, "The configuration key. Use dot notation for nested keys."],
    value: Annotated[str, "The configuration value."],
) -> None:
    set_config_value(APP_DIR, key, value)


@configure.command()
@click.help_option("-h", "--help")
def show() -> None:
    """Display to stdout the chatbot configuration file."""
    console = Console()

    configuration = load_config(APP_DIR)
    flat_config = flatten_dict(configuration)

    for key, value in flat_config.items():
        console.print(f"[cyan]{key}[/cyan]: [bold white]{value}")


@configure.command()
@click.help_option("-h", "--help")
def edit() -> None:
    """Edit the chatbot configuration file."""
    logger = logging.getLogger("app_logger")
    click.edit(filename=str(APP_DIR / "config.toml"))
    logger.debug("Edited config file.")
