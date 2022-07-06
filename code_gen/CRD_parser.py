import json
import yaml
from string import Template
import string
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast
from spec_input_parsers import SpecInputParsers

# Read in files
crd_file = open("code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml", 'r')
crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

input_spec_required = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['required']
input_spec_all = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
output_statuses = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['status']['properties']

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

# use first key as test
# key = next(iter(input_spec_all.keys()))
# print(key+ ' ' +input_spec_all[key]['type']+ ' ' + input_spec_all[key]['description'][0:50])

# From ACK CRD YAML, parse top level spec (input_spec_all), then
# in component.py, add all the parser.add_argument
# in component.yaml, populate inputs section
# in component.yaml, populate implementation.args section
add_input_args_buffer = ""
yaml_inputs_buffer = ""
yaml_args_buffer = ""

for key in input_spec_all:
    add_input_args_buffer += """
    parser.add_argument(
        "--%s",
        type = %s,
        help = "%s",
        required = %r
    )""" % (key, 
            CRD_TYPE_TO_ARGS_TYPE.get(input_spec_all[key]['type']),
            input_spec_all[key]['description'][0:50], 
            key in input_spec_required)
    

    yaml_inputs_buffer += """
  - {
    name: %s,
    type: %s,
    description: "%s"
  }""" % (key, 
        CRD_TYPE_TO_KFP_TYPE.get(input_spec_all[key]['type']), 
        input_spec_all[key]['description'][0:50])

    yaml_args_buffer += ("""
      - --%s
      - { inputValue: %s }""" % (key, key))

# replace placeholders in templates, then write to file
with open("code_gen/templates/component.py.tpl") as t:
    template = string.Template(t.read())
    d = {
        'ADD_INPUT_ARGS': add_input_args_buffer,
    }
    file_draft = template.safe_substitute(d)

with open('code_gen/templates/component.py', 'w') as f:
    f.write(file_draft)

########## Generate component.yaml

crd_name = crd_dict['spec']['names']['kind']

# Populate yaml outputs
yaml_outputs_buffer = ""
for key in output_statuses:
    yaml_outputs_buffer += """
  - {
    name: %s,
    type: %s,
    description: "%s"
  }""" % (key, 
        CRD_TYPE_TO_KFP_TYPE.get(output_statuses[key]['type']), 
        output_statuses[key]['description'][0:50])

# replace placeholders in templates, then write to file
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