"""Command line interface for clive."""

import logging

import click

from clive.loaders.sssom_loader import load_map_file

@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """CLI for clive.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    logger.info(f"Logger {logger.name} set to level {logger.level}")

@main.command()
@click.argument("input_arg", required=True, type=click.Path(exists=True))
def load_maps(
    input_arg: click.Path,
    **kwargs,
):
    """Load one or more SSSOM maps from a file or directory.

    Example:
    
    clive load-maps path/to/file.sssom.tsv

    clive load-maps path/to/directory/

    """

    # TODO: Add support for loading multiple files from a directory
    # TODO: Do something with the MSDF after loading it

    logging.info(f"Loading from {click.format_filename(input_arg)}")
    msdf = load_map_file(input_arg)
    

@main.command()
@click.argument("input_arg", required=True)
def load_maps_from_gsheet(
    input_arg: str,
    **kwargs,
):
    """Load one or more SSSOM maps from a Google Sheet.

    Example:
    
    clive load-maps [URL to Google Sheet]

    """

    # TODO: Add support for loading from a URL

    click.echo(click.format_filename(input_arg))