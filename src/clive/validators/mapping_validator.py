"""Validator functions for SSSOM."""

import logging

from jsonschema import ValidationError
from sssom.validators import check_all_prefixes_in_curie_map, validate_json_schema


def validate_map(msdf):
    """Validate a SSSOM map."""

    # TODO: refactor this a bit

    logging.info("Checking prefixes in CURIE map.")
    try:
        check_all_prefixes_in_curie_map(msdf)
    except ValidationError as e:
        logging.error(f"Validation error when checking CURIE map prefixes: {e}")
        raise e
    
    logging.info("Checking against SSSOM schema.")
    try:
        validate_json_schema(msdf)
    except ValidationError as e:
        logging.error(f"Validation error when validating against SSSOM schema: {e}")
        raise e
