#!/usr/bin/env python3

# Uncomment the apply(use_aws_secret()) below if you are not using OIDC
# more info : https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples/README.md

# RUN in dir: code_gen/components/HyperParameterTuningJob/pipeline/
# dsl-compile --py HyperParameterTuningJob-pipeline.py --output HyperParameterTuningJob-pipeline.tar.gz

import kfp
import json
import copy
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
import yaml

# users can prepare complex input args (object, array) here:



###########################GENERATED SECTION BELOW############################

sagemaker_HyperParameterTuningJob_op = components.load_component_from_file(
    "../component.yaml"
    # "code_gen/components/HyperParameterTuningJob/component.yaml"
)

@dsl.pipeline(name="HyperParameterTuningJob", description="SageMaker HyperParameterTuningJob component")
def HyperParameterTuningJob(
	hyper_parameter_tuning_job_config = ,
	hyper_parameter_tuning_job_name = ,
	tags = ,
	training_job_definition = ,
	training_job_definitions = ,
	warm_start_config = ,

):
    HyperParameterTuningJob = sagemaker_HyperParameterTuningJob_op(
		hyper_parameter_tuning_job_config = hyper_parameter_tuning_job_config,
		hyper_parameter_tuning_job_name = hyper_parameter_tuning_job_name,
		tags = tags,
		training_job_definition = training_job_definition,
		training_job_definitions = training_job_definitions,
		warm_start_config = warm_start_config,

    )  # .apply(use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'))

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(HyperParameterTuningJob, __file__ + ".zip")
