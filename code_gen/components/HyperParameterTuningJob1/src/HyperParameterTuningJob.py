import argparse
import yaml
import logging
import boto3
import os
from kubernetes import client, config, utils
from common.spec_input_parsers import SpecInputParsers

def main():
    parser = argparse.ArgumentParser()

    ###########################GENERATED SECTION BELOW############################
    
    parser.add_argument(
        "--hyper_parameter_tuning_job_config",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "The HyperParameterTuningJobConfig object that desc",
        required = True
    )
    parser.add_argument(
        "--hyper_parameter_tuning_job_name",
        type = str,
        help = "The name of the tuning job. This name is the prefi",
        required = True
    )
    parser.add_argument(
        "--tags",
        type = SpecInputParsers.yaml_or_json_list,
        help = "An array of key-value pairs. You can use tags to c",
        required = False
    )
    parser.add_argument(
        "--training_job_definition",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "The HyperParameterTrainingJobDefinition object tha",
        required = False
    )
    parser.add_argument(
        "--training_job_definitions",
        type = SpecInputParsers.yaml_or_json_list,
        help = "A list of the HyperParameterTrainingJobDefinition ",
        required = False
    )
    parser.add_argument(
        "--warm_start_config",
        type = SpecInputParsers.yaml_or_json_dict,
        help = "Specifies the configuration for starting the hyper",
        required = False
    )
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

    logging.info("Testing----------------")
    logging.info("\n")
    logging.info(args.hyper_parameter_tuning_job_config)
    logging.info("\n")
    logging.info(args.hyper_parameter_tuning_job_name)
    logging.info("\n")
    logging.info(args.tags)
    logging.info("\n")
    logging.info(args.training_job_definition)
    logging.info("\n")
    logging.info(args.training_job_definitions)
    logging.info("\n")
    logging.info(args.warm_start_config)
    logging.info("\n")
    
if __name__ == "__main__":
    main()
