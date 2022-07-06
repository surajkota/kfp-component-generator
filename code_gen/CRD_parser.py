import json, yaml, re, os
from string import Template
import string
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast
from spec_input_parsers import SpecInputParsers

# Run this script in /kfp-component-generator

##############User inputs##############
ACK_CRD_YAML_LOCATION = "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
COMPONENT_CONTAINER_IMAGE = "rdpen/kfp-component-sagemaker:latest"
##############User inputs##############

# type conversion table (reference: KFP_TYPE_FROM_ARGS)
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

def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def parse_crd(_file_name):
    """
    Read in ACK CRD YAML file from file location
    Parse file and get fields
    """

    # crd_file = open("code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml", 'r')
    crd_file = open(_file_name, 'r')
    crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

    input_spec_required = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['required']
    input_spec_all = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
    output_statuses = crd_dict['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['status']['properties']
    crd_name = crd_dict['spec']['names']['kind']

    return input_spec_required, input_spec_all, output_statuses, crd_name

def get_py_add_argument(_input_spec_all, _input_spec_required):
    """
    Populate parser.add_argument with name, type, description, ..
    Return a code snippet waiting to be written to component.py.tpl template
    """

    py_add_argument_buffer = ""

    for key in _input_spec_all:
        py_add_argument_buffer += """
    parser.add_argument(
        "--%s",
        type = %s,
        help = "%s",
        required = %r
    )""" % (camel_to_snake(key), 
                CRD_TYPE_TO_ARGS_TYPE.get(_input_spec_all[key]['type']),
                _input_spec_all[key]['description'][0:50], 
                key in _input_spec_required)

    return py_add_argument_buffer

def get_yaml_inputs(_input_spec_all):
    """
    Populate input section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """
    CRD_TYPE_TO_DEFAULT_VALUE: Dict[str, str] = {
        "string":  """''""",
        "integer": 0,
        "boolean": """False""",
        # SpecInputParsers.nullable_string_argument: "String", # todo
        "object": """'{}'""",
        "array":  """'[]'""",
        # SpecInputParsers.str_to_bool: "Bool",
    }

    yaml_inputs_buffer = ""

    for key in _input_spec_all:
        yaml_inputs_buffer += """
  - {
      name: %s,
      type: %s,
      default: %s,
      description: "%s",
    }""" % (camel_to_snake(key), 
        CRD_TYPE_TO_KFP_TYPE.get(_input_spec_all[key]['type']), 
        CRD_TYPE_TO_DEFAULT_VALUE.get(_input_spec_all[key]['type']), 
        _input_spec_all[key]['description'][0:50])

    return yaml_inputs_buffer

def get_yaml_args(_input_spec_all):
    """
    Populate args section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """

    yaml_args_buffer = ""

    for key in _input_spec_all:
        key = camel_to_snake(key)
        yaml_args_buffer += ("""- --%s\n      - { inputValue: %s }
      """ % (key, key))

    return yaml_args_buffer

def get_yaml_outputs(_output_statuses):
    """
    Populate output section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """

    yaml_outputs_buffer = ""

    for key in _output_statuses:
        yaml_outputs_buffer += """
  - {
      name: %s,
      type: %s,
      description: "%s",
    }""" % (camel_to_snake(key), 
            CRD_TYPE_TO_KFP_TYPE.get(output_statuses[key]['type']), 
            output_statuses[key]['description'][0:50])
    
    return yaml_outputs_buffer

def get_pipeline_user_inputs(_input_spec_all):
    pipeline_user_inputs_buffer = ""

    for key in _input_spec_all:
        pipeline_user_inputs_buffer += """\t%s = ,\n""" % camel_to_snake(key)
        
    return pipeline_user_inputs_buffer

def get_pipeline_args_assign(_input_spec_all):
    pipeline_args_assign_buffer = ""

    for key in _input_spec_all:
        pipeline_args_assign_buffer += """\t\t%s = %s,\n""" % (camel_to_snake(key), camel_to_snake(key))
    
    return pipeline_args_assign_buffer

def write_buffer_to_file(_replace_dict, _template_loc, _out_file_loc, _out_file_dir):

    # replace placeholders in templates
    with open(_template_loc) as t:
        template = string.Template(t.read())
        file_draft = template.safe_substitute(_replace_dict)

    # if output dir not exist, create one and write to file
    if not os.path.exists(_out_file_dir):
        os.makedirs(_out_file_dir)
    with open(_out_file_loc, 'w+') as f:
        f.write(file_draft)

    print("CREATED: " + _out_file_loc)

##############################

if __name__ == "__main__":

    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(ACK_CRD_YAML_LOCATION)

    # testing: use only first key
    # key = next(iter(input_spec_all.keys()))
    # print(key+ ' ' +input_spec_all[key]['type']+ ' ' + input_spec_all[key]['description'][0:50])

    # From ACK CRD YAML, parse top level spec (input_spec_all), then
    # in component.py, add all the parser.add_argument
    # in component.yaml, populate inputs section
    # in component.yaml, populate implementation.args section
    py_add_argument_buffer = get_py_add_argument(input_spec_all, input_spec_required)
    yaml_inputs_buffer = get_yaml_inputs(input_spec_all)
    yaml_args_buffer = get_yaml_args(input_spec_all)
    yaml_outputs_buffer = get_yaml_outputs(output_statuses)
    pipeline_user_inputs_buffer = get_pipeline_user_inputs(input_spec_all)
    pipeline_args_assign_buffer = get_pipeline_args_assign(input_spec_all)

    output_component_dir = 'code_gen/components/' + crd_name + '/'
    output_yaml_location = output_component_dir + 'component.yaml'
    output_py_dir =  output_component_dir + 'src/'
    output_py_location = output_py_dir + crd_name + '.py'
    output_pipeline_dir = output_component_dir + 'pipeline/'
    output_pipeline_location = output_pipeline_dir + crd_name + '-pipeline'+ '.py'
    
    # # pipeline.py: replace placeholders in templates
    # with open("code_gen/templates/pipeline.py.tpl") as t:
    #     template = string.Template(t.read())
    #     d = {
    #         'PIPELINE_USER_INPUTS' : pipeline_user_inputs_buffer,
    #         'PIPELINE_ARGS_ASSIGN': pipeline_args_assign_buffer,
    #         'CRD_NAME': crd_name
    #     }
    #     file_draft = template.safe_substitute(d)

    # # if output dir not exist, create one and write to file
    # if not os.path.exists(output_pipeline_dir):
    #     os.makedirs(output_pipeline_dir)
    # with open(output_pipeline_location, 'w+') as f:
    #     f.write(file_draft)

    pipeline_replace = {
            'PIPELINE_USER_INPUTS' : pipeline_user_inputs_buffer,
            'PIPELINE_ARGS_ASSIGN': pipeline_args_assign_buffer,
            'CRD_NAME': crd_name
        }

    write_buffer_to_file(pipeline_replace, "code_gen/templates/pipeline.py.tpl", output_pipeline_location, output_pipeline_dir)

    # # component.py: replace placeholders in templates
    # with open("code_gen/templates/component.py.tpl") as t:
    #     template = string.Template(t.read())
    #     d = {
    #         'PY_ADD_ARGUMENT': py_add_argument_buffer,
    #     }
    #     file_draft = template.safe_substitute(d)

    # # if output dir not exist, create one and write to file
    # if not os.path.exists(output_py_dir):
    #     os.makedirs(output_py_dir)
    # with open(output_py_location, 'w+') as f:
    #     f.write(file_draft)
    
    py_replace = {
            'PY_ADD_ARGUMENT': py_add_argument_buffer,
        }

    write_buffer_to_file(py_replace, "code_gen/templates/component.py.tpl", output_py_location, output_py_dir)

    # # component.yaml: replace placeholders in templates, then write to file
    # with open("code_gen/templates/component.yaml.tpl") as t:
    #     template = string.Template(t.read())
    #     d = {
    #         'CRD_NAME': crd_name,
    #         'YAML_INPUTS': yaml_inputs_buffer,
    #         'YAML_OUTPUTS': yaml_outputs_buffer,
    #         'YAML_ARGS': yaml_args_buffer,
    #         'COMPONENT_CONTAINER_IMAGE': COMPONENT_CONTAINER_IMAGE
    #     }
    #     file_draft = template.safe_substitute(d)

    # # write to yaml location, no need to create dir again, done in os.makedirs(output_py_dir)
    # with open(output_yaml_location, 'w+') as f:
    #     f.write(file_draft)

    yaml_replace = {
            'CRD_NAME': crd_name,
            'YAML_INPUTS': yaml_inputs_buffer,
            'YAML_OUTPUTS': yaml_outputs_buffer,
            'YAML_ARGS': yaml_args_buffer,
            'COMPONENT_CONTAINER_IMAGE': COMPONENT_CONTAINER_IMAGE
        }
    
    write_buffer_to_file(yaml_replace, "code_gen/templates/component.yaml.tpl", output_yaml_location, output_component_dir)

