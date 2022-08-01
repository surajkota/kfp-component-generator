"""
Methods to generate content in src/*_request.yaml.tpl
"""

import random
from code_gen.generator.utils import parse_crd, snake_to_camel, write_snippet_to_file


def get_ack_job_request_outline_spec(_input_spec_all):
    """Populate spec section in a ACK job request YAML Return a code snippet
    waiting to be written to ack_job_request.yaml.tpl template."""
    _ack_job_request_outline_spec_snippet = ""

    for key in _input_spec_all:
        _ack_job_request_outline_spec_snippet += """  %s: \n""" % snake_to_camel(key)

    return _ack_job_request_outline_spec_snippet
