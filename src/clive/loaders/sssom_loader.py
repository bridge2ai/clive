"""Loader functions for SSSOM."""

from pathlib import Path
import re

import pandas as pd

from sssom.parsers import parse_sssom_table
from sssom.util import MappingSetDataFrame


def init_map_dataframe() -> MappingSetDataFrame:
    """Initialize an empty MappingSetDataFrame object.

    :return: An empty MappingSetDataFrame object.
    """
    df = pd.DataFrame()
    return MappingSetDataFrame(df)


def load_map_file(input_path: Path) -> MappingSetDataFrame:
    """Load a single local SSSOM TSV or other SSSOM-compatible format.

    :param  input_path: The path to the input file in one of the legal
      formats, eg obographs, aligmentapi-xml
    :return: A MappingSetDataFrame object.
    """
    msdf = parse_sssom_table(input_path)

    return msdf


def load_map_gsheet(sheet_url: str) -> MappingSetDataFrame:
    """Load a single SSSOM map from a Google Sheet.

    Saves a local copy of each sheet as a TSV file.

    :param sheet_id: The ID of the Google Sheet.
    :return: A MappingSetDataFrame object.
    """

    # Convert the URL to a sheet ID and a gid

    pattern = r"https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?"

    replacement = (
        lambda m: f"https://docs.google.com/spreadsheets/d/{m.group(1)}/export?"
        + (f"gid={m.group(3)}&" if m.group(3) else "")
        + "format=csv"
    )

    # Get the sheet ID alone
    match = re.match(pattern, sheet_url)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = None

    export_url = re.sub(pattern, replacement, sheet_url)

    # Load table from its HTML
    sheet_df = pd.read_csv(export_url)

    print(sheet_df)

    # Save a local copy
    sheet_df.to_csv(f"{sheet_id}.tsv", sep="\t", index=False)

    msdf = MappingSetDataFrame(sheet_df)

    return msdf
