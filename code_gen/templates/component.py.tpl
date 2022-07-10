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
    ${PY_ADD_ARGUMENT}
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

if __name__ == "__main__":
    main()
