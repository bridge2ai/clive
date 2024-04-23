"""Loader functions for SSSOM."""

from pathlib import Path

from pandas import DataFrame
from sssom.parsers import parse_sssom_table
from sssom.util import MappingSetDataFrame


def init_map_dataframe() -> MappingSetDataFrame:
    """Initialize an empty MappingSetDataFrame object.

    :return: An empty MappingSetDataFrame object.
    """
    df = DataFrame()
    return MappingSetDataFrame(df)

def load_map_file(input_path: Path) -> MappingSetDataFrame:
    """Load a single local SSSOM TSV or other SSSOM-compatible format.

    :param  input_path: The path to the input file in one of the legal
      formats, eg obographs, aligmentapi-xml
    :return: A MappingSetDataFrame object.
    """
    msdf = parse_sssom_table(input_path)

    return msdf
