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


if __name__ == "__main__":

    ##############User inputs##############
    ACK_CRD_YAML_LOCATION = (
        # "code_gen/ack_crd/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
        "code_gen/ack_crd/sagemaker.services.k8s.aws_trainingjobs.yaml"
    )
    COMPONENT_CONTAINER_IMAGE = "rdpen/kfp-component-sagemaker:latest"
    ##############User inputs##############

    # From ACK CRD YAML, parse fields needed
    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
        ACK_CRD_YAML_LOCATION
    )

    ## prepare code snippet
    (
        spec_inputs_defi_snippet,
        spec_inputs_validators_snippet,
    ) = get_spec_input_snippets(input_spec_all, input_spec_required)

    (
        spec_outputs_defi_snippet,
        spec_outputs_validators_snippet,
    ) = get_spec_output_snippets(output_statuses)

    (
        input_class_name,
        output_class_name,
        spec_class_name,
        component_class_name,
    ) = get_class_names(crd_name)

    ## set up output file directory
    output_component_dir = "code_gen/components/" + crd_name + "/"
    output_src_dir = output_component_dir + "src/"
    output_spec_name = crd_name + "_spec.py"
    output_spec_path = output_src_dir + output_spec_name

    ## replace placeholders in templates with buffer, then write to file
    spec_replace = {
        "CRD_NAME": crd_name,
        "INPUT_CLASS_NAME": input_class_name,
        "OUTPUT_CLASS_NAME": output_class_name,
        "SPEC_CLASS_NAME": spec_class_name,
        "SPEC_INPUT_DEFINITIONS": spec_inputs_defi_snippet,
        "SPEC_OUTPUT_DEFINITIONS": spec_outputs_defi_snippet,
        "SPEC_INPUT_VALIDATORS": spec_inputs_validators_snippet,
        "SPEC_OUTPUT_VALIDATORS": spec_outputs_validators_snippet,
    }
    write_snippet_to_file(
        spec_replace,
        "code_gen/templates/*_spec.py.tpl",
        output_spec_path,
        output_src_dir,
    )
