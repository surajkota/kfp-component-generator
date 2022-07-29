#!/usr/bin/env python3

# Uncomment the apply(use_aws_secret()) below if you are not using OIDC
# more info : https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples/README.md

# RUN in source directory: python code_gen/tests/pipelines/TrainingJob-pipeline.py
# or
# Manually compile in dir: code_gen/tests/pipelines/
# dsl-compile --py TrainingJob-pipeline.py --output TrainingJob-pipeline.tar.gz

import random, os
import kfp
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
import tarfile
from datetime import datetime


#############################################################################
# users can prepare complex input args (object, array) here:
# set up input values
trainingJobName = "kfp-ack-training-job-" + str(random.randint(0, 999999))

hyperParameters = {
    "max_depth": "2",
    "gamma": "10",
    "eta": "0.3",
    "min_child_weight": "6",
    "objective": "multi:softmax",
    "num_class": "10",
    "num_round": "10",
}

algorithmSpecification = {
    # The URL and tag of your ECR container
    # If you are not on us-west-2 you can find an imageURI here https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html
    "trainingImage": "746614075791.dkr.ecr.us-west-1.amazonaws.com/sagemaker-xgboost:1.2-1",
    "trainingInputMode": "File",
}

# change it to your role with SageMaker and S3 access
# example arn:aws:iam::1234567890:role/service-role/AmazonSageMaker-ExecutionRole
roleARN = "arn:aws:iam::740468203605:role/ack-sagemaker-execution-role"

# change it to your bucket: s3://<YOUR BUCKET/OUTPUT> 
outputDataConfig = {"s3OutputPath": "s3://ack-sagemaker-bucket-740468203605"}
resourceConfig = {
    "instanceCount": 1,
    "instanceType": "ml.m4.xlarge",
    "volumeSizeInGB": 5,
}

stoppingCondition = {"maxRuntimeInSeconds": 86400}

inputDataConfig = [
    {
        "channelName": "train",
        "dataSource": {
            "s3DataSource": {
                "s3DataType": "S3Prefix",
                # change it to your input path of the train data: s3://<YOUR BUCKET>/sagemaker/xgboost/train
                "s3URI": "s3://ack-sagemaker-bucket-740468203605/sagemaker/xgboost/train",
                "s3DataDistributionType": "FullyReplicated",
            },
        },
        "contentType": "text/libsvm",
        "compressionType": "None",
    },
    {
        "channelName": "validation",
        "dataSource": {
            "s3DataSource": {
                "s3DataType": "S3Prefix",
                # change it to your input path of the validation data: s3://<YOUR BUCKET>/sagemaker/xgboost/validation
                "s3URI": "s3://ack-sagemaker-bucket-740468203605/sagemaker/xgboost/validation",
                "s3DataDistributionType": "FullyReplicated",
            },
        },
        "contentType": "text/libsvm",
        "compressionType": "None",
    },
]

###########################GENERATED SECTION BELOW############################

sagemaker_TrainingJob_op = components.load_component_from_file(
    # "../../components/TrainingJob/component.yaml" # run in /pipeline
    "code_gen/components/TrainingJob/component.yaml" # run in source dir
)


@dsl.pipeline(name="TrainingJob", description="SageMaker TrainingJob component")
def TrainingJob(
    algorithm_specification=algorithmSpecification,
    checkpoint_config=None,
    debug_hook_config=None,
    debug_rule_configurations=None,
    enable_inter_container_traffic_encryption=False,
    enable_managed_spot_training=False,
    enable_network_isolation=False,
    environment=None,
    experiment_config=None,
    hyper_parameters=hyperParameters,
    input_data_config=inputDataConfig,
    output_data_config=outputDataConfig,
    profiler_config=None,
    profiler_rule_configurations=None,
    resource_config=resourceConfig,
    role_arn=roleARN,
    stopping_condition=stoppingCondition,
    tags=None,
    tensor_board_output_config=None,
    training_job_name=trainingJobName,
    vpc_config=None,
):
    TrainingJob = sagemaker_TrainingJob_op(
        algorithm_specification=algorithm_specification,
        checkpoint_config=checkpoint_config,
        debug_hook_config=debug_hook_config,
        debug_rule_configurations=debug_rule_configurations,
        enable_inter_container_traffic_encryption=enable_inter_container_traffic_encryption,
        enable_managed_spot_training=enable_managed_spot_training,
        enable_network_isolation=enable_network_isolation,
        environment=environment,
        experiment_config=experiment_config,
        hyper_parameters=hyper_parameters,
        input_data_config=input_data_config,
        output_data_config=output_data_config,
        profiler_config=profiler_config,
        profiler_rule_configurations=profiler_rule_configurations,
        resource_config=resource_config,
        role_arn=role_arn,
        stopping_condition=stopping_condition,
        tags=tags,
        tensor_board_output_config=tensor_board_output_config,
        training_job_name=training_job_name,
        vpc_config=vpc_config,
    ).apply(use_aws_secret("aws-secret", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"))


if __name__ == "__main__":
    #### SET PARAMETERS HERE #####################################################
    AUTHSERVICE_SESSION_COOKIE=""
    PIPELINE_NAME = "TrainingJob-pipeline"
    EXPERIMENT_NAME = "TrainingJob"
    NOW_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    RUN_JOB_NAME = "TrainingJob-" + NOW_TIME
    ###############################################################################
    
    # compile the pipeline, unzip it and get pipeline.yaml
    kfp.compiler.Compiler().compile(TrainingJob, __file__ + ".tar.gz")
    
    print("#####################Pipeline compiled########################")
    
    with tarfile.open(__file__ + ".tar.gz") as tar:
        # tar.extractall()
        tar.extract("pipeline.yaml", "code_gen/tests/pipelines")
        tar.close()

    # configure kfp client
    kubeflow_gateway_endpoint="localhost:8080" # "Domain" in your cookies. Eg: "localhost:8080" or "<ingress_alb_address>.elb.amazonaws.com"
    authservice_session_cookie=AUTHSERVICE_SESSION_COOKIE
    
    namespace="kubeflow-user-example-com"

    client = kfp.Client(host=f"http://{kubeflow_gateway_endpoint}/pipeline", cookies=f"authservice_session={authservice_session_cookie}")
    
    # print(client.list_experiments(namespace=namespace))
    
    print("KFP Python client connected to Kubeflow")

    # Upload the pipeline to Kubeflow
    pipeline_file_path = "code_gen/tests/pipelines/pipeline.yaml"    
    pipeline_name = PIPELINE_NAME
    
    if not client.get_pipeline_id(name = pipeline_name): 
        # if pipeline does not exist, upload pipeline
        pipeline_file = os.path.join(pipeline_file_path)
        pipeline = client.pipeline_uploads.upload_pipeline(pipeline_file, name=pipeline_name)
        
    else:
        # if pipeline exist, upload new pipeline version
        pipeline_id = client.get_pipeline_id(name = pipeline_name)
        
        pipeline_version_file_path = "code_gen/tests/pipelines/pipeline.yaml"    
        pipeline_version_name = NOW_TIME
        pipeline_version_file = os.path.join(pipeline_version_file_path)
        pipeline_version = client.pipeline_uploads.upload_pipeline_version(pipeline_version_file,
                                                                        name=pipeline_version_name,
                                                                        pipelineid=pipeline_id)
        
    print("Uploaded pipeline")
    
    # Run the pipeline in experiment
    experiment_id = client.get_experiment(namespace=namespace, experiment_name=EXPERIMENT_NAME).id
    my_run = client.run_pipeline(experiment_id, RUN_JOB_NAME, __file__ + ".tar.gz")
    
    print("Created pipeline run: " + my_run.id)