"""
Methods to generate content in src/*_spec.py
"""

import re
from telnetlib import STATUS
from typing import Dict
from code_gen.generator.utils import (
    camel_to_snake,
    get_class_names,
    parse_crd,
    snake_to_camel,
    write_snippet_to_file,
)


CRD_TYPE_TO_ARGS_TYPE: Dict[str, str] = {
    "string": "str",
    "integer": "int",
    # "boolean": bool,
    # "string": SpecInputParsers.nullable_string_argument,
    "object": "SpecInputParsers.yaml_or_json_dict",
    "array": "SpecInputParsers.yaml_or_json_list",
    "boolean": "SpecInputParsers.str_to_bool",
}

## Generate src/*_spec.py content
def get_spec_input_snippets(_input_spec_all, _input_spec_required):
    """Generate the input section for src/*_spec.py."""
    _spec_inputs_defi_snippet = ""
    _spec_inputs_validators_snippet = ""

    for key in _input_spec_all:

        _spec_inputs_defi_snippet += """
    %s: Input""" % (
            camel_to_snake(key),
        )

        _spec_inputs_validators_snippet += """
        %s=InputValidator(
            input_type=%s,
            description="%s",
            required=%r
        ), """ % (
            camel_to_snake(key),
            CRD_TYPE_TO_ARGS_TYPE.get(_input_spec_all[key]["type"]),
            " ".join(
                re.split(r"\n", _input_spec_all[key]["description"][0:100].strip())
            ),
            key in _input_spec_required,
        )

    return (
        _spec_inputs_defi_snippet,
        _spec_inputs_validators_snippet,
    )


def get_spec_output_snippets(_output_statuses):
    """Generate the output section for src/*_spec.py."""
    _spec_outputs_defi_snippet = ""
    _spec_outputs_validators_snippet = ""

    for key in _output_statuses:
        _spec_outputs_defi_snippet += """
    %s: Output""" % (
            camel_to_snake(key),
        )

        _spec_outputs_validators_snippet += """
        %s=OutputValidator(
            description="%s",
        ), """ % (
            camel_to_snake(key),
            " ".join(
                re.split(r"\n", _output_statuses[key]["description"][0:100].strip())
            ),
        )

    return (
        _spec_outputs_defi_snippet,
        _spec_outputs_validators_snippet,
    )
