import json
import yaml
from string import Template
import string
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast
from spec_input_parsers import SpecInputParsers


# type conversion table

# KFP_TYPE_FROM_ARGS: Dict[Callable, str] = {
#         str: "String",
#         int: "Integer",
#         bool: "Bool",
#         SpecInputParsers.nullable_string_argument: "String",
#         SpecInputParsers.yaml_or_json_dict: "JsonObject",
#         SpecInputParsers.yaml_or_json_list: "JsonArray",
#         SpecInputParsers.str_to_bool: "Bool",
#     }

CRD_TYPE_TO_KFP_TYPE: Dict[str, str] = {
        "string": "String",
        "integer": "Integer",
        "boolean": "Bool",
        # SpecInputParsers.nullable_string_argument: "String", # todo
        "object": "JsonObject",
        "array": "JsonArray",
        # SpecInputParsers.str_to_bool: "Bool",
    }

CRD_TYPE_TO_ARGS_TYPE: Dict[str, str] = {
        "string": "str",
        "integer": "int",
        # "boolean": bool,
        # "string": SpecInputParsers.nullable_string_argument,
        "object": "SpecInputParsers.yaml_or_json_dict",
        "array": "SpecInputParsers.yaml_or_json_list",
        "boolean": "SpecInputParsers.str_to_bool",
    }

# Read in files
def parse_crd(file_name):
            
    # crd_file = open("code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml", 'r')
    crd_file = open(file_name, 'r')
    crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

    input_spec_required = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['required']
    input_spec_all = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
    output_statuses = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['status']['properties']
    crd_name = crd_dict['spec']['names']['kind']

    return input_spec_required, input_spec_all, output_statuses, crd_name

def get_py_add_argument(_input_spec_all, _input_spec_required):

    py_add_argument_buffer = ""

    for key in _input_spec_all:
        py_add_argument_buffer += """
    parser.add_argument(
        "--%s",
        type = %s,
        help = "%s",
        required = %r
    )""" % (key, 
                CRD_TYPE_TO_ARGS_TYPE.get(_input_spec_all[key]['type']),
                _input_spec_all[key]['description'][0:50], 
                key in _input_spec_required)

    return py_add_argument_buffer

def get_yaml_inputs(_input_spec_all):

    yaml_inputs_buffer = ""

    for key in _input_spec_all:
        yaml_inputs_buffer += """
  - {
      name: %s,
      type: %s,
      description: "%s",
    }""" % (key, 
        CRD_TYPE_TO_KFP_TYPE.get(_input_spec_all[key]['type']), 
        _input_spec_all[key]['description'][0:50])

    return yaml_inputs_buffer

def get_yaml_args(_input_spec_all):

    yaml_args_buffer = ""

    for key in _input_spec_all:
        yaml_args_buffer += ("""
      - --%s
      - { inputValue: %s }""" % (key, key))

    return yaml_args_buffer

def get_yaml_outputs(_input_spec_all):

    yaml_outputs_buffer = ""

    for key in output_statuses:
        yaml_outputs_buffer += """
  - {
      name: %s,
      type: %s,
      description: "%s",
    }""" % (key, 
            CRD_TYPE_TO_KFP_TYPE.get(output_statuses[key]['type']), 
            output_statuses[key]['description'][0:50])
    
    return yaml_outputs_buffer

##############################

if __name__ == "__main__":

    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd("code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml")

    # testing: use first key
    # key = next(iter(input_spec_all.keys()))
    # print(key+ ' ' +input_spec_all[key]['type']+ ' ' + input_spec_all[key]['description'][0:50])

    # From ACK CRD YAML, parse top level spec (input_spec_all), then
    # in component.py, add all the parser.add_argument
    # in component.yaml, populate inputs section
    # in component.yaml, populate implementation.args section
    py_add_argument_buffer = get_py_add_argument(input_spec_all, input_spec_required)
    yaml_inputs_buffer = get_yaml_inputs(input_spec_all)
    yaml_args_buffer = get_yaml_args(input_spec_all)
    yaml_outputs_buffer = get_yaml_outputs(input_spec_all)

    # .PY: replace placeholders in templates, then write to file
    with open("code_gen/templates/component.py.tpl") as t:
        template = string.Template(t.read())
        d = {
            'PY_ADD_ARGUMENT': py_add_argument_buffer,
        }
        file_draft = template.safe_substitute(d)

    with open('code_gen/templates/component.py', 'w') as f:
        f.write(file_draft)

    # .YAML: replace placeholders in templates, then write to file
    with open("code_gen/templates/component.yaml.tpl") as t:
        template = string.Template(t.read())
        d = {
            'CRD_NAME': crd_name,
            'YAML_INPUTS': yaml_inputs_buffer,
            'YAML_OUTPUTS': yaml_outputs_buffer,
            'YAML_ARGS': yaml_args_buffer
        }
        file_draft = template.safe_substitute(d)

    with open('code_gen/templates/component.yaml', 'w') as f:
        f.write(file_draft)

