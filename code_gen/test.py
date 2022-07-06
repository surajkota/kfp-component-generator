# in kfp-component-generator, run ->-> python -m code_gen.test
# or change vscode debug config
# https://jsonformatter.org/yaml-parser

# import common
# from common import generate_components
import json
import yaml

## ACK YAML parser
# stream = open("code_gen/ack_crd/sagemaker.services.k8s.aws_trainingjobs.yaml", 'r')
# dictionary = yaml.load(stream, Loader=yaml.FullLoader)
# para_input_all = dictionary['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
# para_input_required = dictionary['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['required']
# para_output = dictionary['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['status']['properties']

# print(para_output)

###############################################################
## templating
from string import Template
import string

## input and outputs
component_name = "SageMakerTraining" # ${COMPONENT_NAME}
input_class_name = component_name + "Inputs" # ${INPUT_CLASS_NAME}
output_class_name = component_name + "Outputs" # ${OUTPUT_CLASS_NAME}

# ${INPUT_PARA_TYPE_VALIDATOR}
# ${INPUT_PARA}

# write to file
with open("code_gen/templates/test_spec.py.tpl") as t:
    template = string.Template(t.read())
    d = {
        'COMPONENT_NAME': component_name,
        'INPUT_CLASS_NAME': input_class_name,
        'OUTPUT_CLASS_NAME': output_class_name
    }

    # spec_file_draft = template.safe_substitute(d)
    spec_file_draft = template.substitute(id1 = "44")

with open('code_gen/templates/test_spec.py', 'w') as f:
    f.write(spec_file_draft)

class SpecGenerator():
    pass
    """Defines attributes and methods to generate a spec file """
    # attributes
        # spec_file_draft
        # 

    # replace input class name
    # replace output class name
    # ACK YAML parser -> 
    
    # generate input parameters and type
    # generate output parameters and types

    # write spec file to path


