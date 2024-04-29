import click
from dotenv import load_dotenv

from chatbot.chat import main_loop
from chatbot.memory import create_memory


@click.group()
@click.version_option()
@click.help_option("-h", "--help")
def cli():
    """Manage the chatbot with memories."""
    load_dotenv()


@cli.command()
def chat():
    """Chat with the chatbot."""
    click.echo("Starting a chat session...")
    main_loop()


@cli.command()
@click.option("-p", "--with-pdf", is_flag=True, help="Load PDFs into memory.")
@click.option("-w", "--with-web", is_flag=True, help="Load web pages into memory.")
def setup(with_pdf, with_web):
    """Setup the chatbot."""
    click.echo("Setting up the chatbot memories...")
    create_memory(with_pdf, with_web)
