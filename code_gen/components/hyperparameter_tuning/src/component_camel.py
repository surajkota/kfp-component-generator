import argparse
import yaml
import logging
import boto3
import os
from kubernetes import client, config, utils
from spec_input_parsers import SpecInputParsers

def main():
    parser = argparse.ArgumentParser()

    ###########################GENERATED SECTION BELOW############################
    
    # parser.add_argument(
    #     "--hyperParameterTuningJobConfig",
    #     type = SpecInputParsers.yaml_or_json_dict,
    #     help = "The HyperParameterTuningJobConfig object that desc",
    #     required = True
    # )
    parser.add_argument(
        "--ack_yaml",
        type=yaml.safe_load,
        help="Raw YAML for deployment",
        default="{}"
    )
    parser.add_argument(
        "--hyperParameterTuningJobName",
        type = str,
        help = "The name of the tuning job. This name is the prefi",
        required = True
    )
    # parser.add_argument(
    #     "--tags",
    #     type = SpecInputParsers.yaml_or_json_list,
    #     help = "An array of key-value pairs. You can use tags to c",
    #     required = False
    # )
    # parser.add_argument(
    #     "--trainingJobDefinition",
    #     type = SpecInputParsers.yaml_or_json_dict,
    #     help = "The HyperParameterTrainingJobDefinition object tha",
    #     required = False
    # )
    # parser.add_argument(
    #     "--trainingJobDefinitions",
    #     type = SpecInputParsers.yaml_or_json_list,
    #     help = "A list of the HyperParameterTrainingJobDefinition ",
    #     required = False
    # )
    # parser.add_argument(
    #     "--warmStartConfig",
    #     type = SpecInputParsers.yaml_or_json_dict,
    #     help = "Specifies the configuration for starting the hyper",
    #     required = False
    # )
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

if __name__ == "__main__":
    main()
