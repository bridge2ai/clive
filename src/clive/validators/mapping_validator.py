"""Validator functions for SSSOM."""

import logging

from sssom.validators import check_all_prefixes_in_curie_map

def validate_map(msdf):
    """Validate a SSSOM map."""
    logging.info("Checking prefixes in CURIE map.")
    check_all_prefixes_in_curie_map(msdf)