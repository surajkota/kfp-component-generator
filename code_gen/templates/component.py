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
    
    parser.add_argument(
        "--algorithmSpecification",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "The registry path of the Docker image that contain",
        required = True
    )
    parser.add_argument(
        "--checkpointConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Contains information about the output location for",
        required = False
    )
    parser.add_argument(
        "--debugHookConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Configuration information for the Debugger hook pa",
        required = False
    )
    parser.add_argument(
        "--debugRuleConfigurations",
        type = SpecInputParsers.yaml_or_json_list,
        help = "Configuration information for Debugger rules for d",
        required = False
    )
    parser.add_argument(
        "--enableInterContainerTrafficEncryption",
        type = SpecInputParsers.str_to_bool,
        help = "To encrypt all communications between ML compute i",
        required = False
    )
    parser.add_argument(
        "--enableManagedSpotTraining",
        type = SpecInputParsers.str_to_bool,
        help = "To train models using managed spot training, choos",
        required = False
    )
    parser.add_argument(
        "--enableNetworkIsolation",
        type = SpecInputParsers.str_to_bool,
        help = "Isolates the training container. No inbound or out",
        required = False
    )
    parser.add_argument(
        "--environment",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "The environment variables to set in the Docker con",
        required = False
    )
    parser.add_argument(
        "--experimentConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Associates a SageMaker job as a trial component wi",
        required = False
    )
    parser.add_argument(
        "--hyperParameters",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Algorithm-specific parameters that influence the q",
        required = False
    )
    parser.add_argument(
        "--inputDataConfig",
        type = SpecInputParsers.yaml_or_json_list,
        help = "An array of Channel objects. Each channel is a nam",
        required = False
    )
    parser.add_argument(
        "--outputDataConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Specifies the path to the S3 location where you wa",
        required = True
    )
    parser.add_argument(
        "--profilerConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Configuration information for Debugger system moni",
        required = False
    )
    parser.add_argument(
        "--profilerRuleConfigurations",
        type = SpecInputParsers.yaml_or_json_list,
        help = "Configuration information for Debugger rules for p",
        required = False
    )
    parser.add_argument(
        "--resourceConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "The resources, including the ML compute instances ",
        required = True
    )
    parser.add_argument(
        "--roleARN",
        type = str,
        help = "The Amazon Resource Name (ARN) of an IAM role that",
        required = True
    )
    parser.add_argument(
        "--stoppingCondition",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Specifies a limit to how long a model training job",
        required = True
    )
    parser.add_argument(
        "--tags",
        type = SpecInputParsers.yaml_or_json_list,
        help = "An array of key-value pairs. You can use tags to c",
        required = False
    )
    parser.add_argument(
        "--tensorBoardOutputConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Configuration of storage locations for the Debugge",
        required = False
    )
    parser.add_argument(
        "--trainingJobName",
        type = str,
        help = "The name of the training job. The name must be uni",
        required = True
    )
    parser.add_argument(
        "--vpcConfig",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "A VpcConfig object that specifies the VPC that you",
        required = False
    )
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

if __name__ == "__main__":
    main()
