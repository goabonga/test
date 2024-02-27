import click

from playground import __version__

click.version_option(__version__)


@click.command()
@click.argument("name")
def hello(name):
    click.echo(f"Hello {name}!")
