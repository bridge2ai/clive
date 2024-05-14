"""Command line interface for clive."""

import logging
from pathlib import Path

import click

from clive.loaders.sssom_loader import init_map_dataframe, load_map_file, load_map_gsheet
from clive.validators.mapping_validator import validate_map

output_option = click.option(
    "-o",
    "--output",
    type=click.File(mode="w"),
    default="output.sssom.tsv",
    help="Output file path.",
)


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
@output_option
@click.argument("input_arg", required=True, type=click.Path(exists=True))
def load_maps(
    input_arg: click.Path,
    output: str,
    **kwargs,
):
    """Load one or more SSSOM maps from a file or directory.

    Example:

    clive load-maps path/to/file.sssom.tsv

    clive load-maps path/to/directory/

    """

    logging.info(f"Loading from {click.format_filename(input_arg)}")

    msdf = init_map_dataframe()

    # Check if input is a directory
    if Path(input_arg).is_dir():
        for file in Path(input_arg).iterdir():
            if file.suffix == ".tsv":
                logging.info(f"Found {file} - looks like SSSOM, loading.")
                new_msdf = load_map_file(file)
                msdf.merge(new_msdf)
            else:
                logging.info(f"Found {file} - does not look like SSSOM, skipping.")
    else:
        new_msdf = load_map_file(input_arg)
        msdf.merge(new_msdf)

    logging.info(f"Loaded {len(msdf.df)} mappings")

    logging.info(f"Performing SSSOM validation.")
    validate_map(msdf)

    logging.info(f"Writing to {output}")



@main.command()
@click.argument("input_arg", required=True)
def load_maps_from_gsheet(
    input_arg: str,
    **kwargs,
):
    """Load one or more SSSOM maps from a Google Sheet.

    Provide the full URL, including the part after the gid.

    Example:

    clive load-maps-from-gsheet [URL of Google Sheet]

    """

    # TODO: Enable loading multiple maps from tabs,
    # or from different documents

    logging.info(f"Will try to load from sheet with URL {input_arg}")

    msdf = load_map_gsheet(input_arg)

    logging.info(f"Loaded {len(msdf.df)} mappings")
