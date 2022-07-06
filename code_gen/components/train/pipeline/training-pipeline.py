#!/usr/bin/env python3

# Uncomment the apply(use_aws_secret()) below if you are not using OIDC
# more info : https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples/README.md

# RUN in code_gen/components/train/pipeline/
# dsl-compile --py training-pipeline.py --output training-pipeline.tar.gz

import kfp
import json
import copy
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
import yaml

sagemaker_train_op = components.load_component_from_file(
    "../component.yaml"
)

# input args
with open('ack.yaml', 'r') as f:
    yaml_file = yaml.safe_load(f)

@dsl.pipeline(name="Training pipeline", description="SageMaker training job test")
def training(
    ack_yaml = yaml_file,
):
    training = sagemaker_train_op(
        ack_yaml = ack_yaml
    )  # .apply(use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'))


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(training, __file__ + ".zip")
