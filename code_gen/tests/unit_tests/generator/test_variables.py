input_spec_required = [
    "outputDataConfig",
    "roleARN",
]

input_spec_all = {
    "checkpointConfig": {
        "description": "Contains information about the output location for managed spot training checkpoint data.",
        "properties": {"localPath": {"type": "string"}, "s3URI": {"type": "string"}},
        "type": "object",
    },
    "outputDataConfig": {
        "description": "Specifies the path to the S3 location where you want to store model artifacts. Amazon SageMaker creates subfolders for the artifacts.",
        "properties": {
            "kmsKeyID": {"type": "string"},
            "s3OutputPath": {"type": "string"},
        },
        "type": "object",
    },
    "roleARN": {
        "description": "The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf. \n During model training, Amazon SageMaker needs your permission to read input data from an S3 bucket, download a Docker image that contains training code, write model artifacts to an S3 bucket, write logs to Amazon CloudWatch Logs, and publish metrics to Amazon CloudWatch. You grant permissions for all of these tasks to an IAM role. For more information, see Amazon SageMaker Roles (https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html). \n To be able to pass this role to Amazon SageMaker, the caller of this API must have the iam:PassRole permission.",
        "type": "string",
    },
    "debugRuleEvaluationStatuses": {
        "description": "Evaluation status of Debugger rules for debugging on a training job.",
        "items": {
            "description": "Information about the status of the rule evaluation.",
            "properties": {
                "lastModifiedTime": {"format": "date-time", "type": "string"},
                "ruleConfigurationName": {"type": "string"},
                "ruleEvaluationJobARN": {"type": "string"},
                "ruleEvaluationStatus": {"type": "string"},
                "statusDetails": {"type": "string"},
            },
            "type": "object",
        },
        "type": "array",
    },
}

crd_name = "TrainingJob"


output_statuses = {
    "ackResourceMetadata": {
        "description": "All CRs managed by ACK have a common `Status.ACKResourceMetadata` member that is used to contain resource sync state, account ownership, constructed ARN for the resource",
        "properties": {
            "arn": {
                "description": 'ARN is the Amazon Resource Name for the resource. This is a globally-unique identifier and is set only by the ACK service controller once the controller has orchestrated the creation of the resource OR when it has verified that an "adopted" resource (a resource where the ARN annotation was set by the Kubernetes user on the CR) exists and matches the supplied CR\'s Spec field values. TODO(vijat@): Find a better strategy for resources that do not have ARN in CreateOutputResponse https://github.com/aws/aws-controllers-k8s/issues/270',
                "type": "string",
            },
            "ownerAccountID": {
                "description": "OwnerAccountID is the AWS Account ID of the account that owns the backend AWS service API resource.",
                "type": "string",
            },
            "region": {
                "description": "Region is the AWS region in which the resource exists or will exist.",
                "type": "string",
            },
        },
        "required": ["ownerAccountID", "region"],
        "type": "object",
    },
    "debugRuleEvaluationStatuses": {
        "description": "Evaluation status of Debugger rules for debugging on a training job.",
        "items": {
            "description": "Information about the status of the rule evaluation.",
            "properties": {
                "lastModifiedTime": {"format": "date-time", "type": "string"},
                "ruleConfigurationName": {"type": "string"},
                "ruleEvaluationJobARN": {"type": "string"},
                "ruleEvaluationStatus": {"type": "string"},
                "statusDetails": {"type": "string"},
            },
            "type": "object",
        },
        "type": "array",
    },
    "failureReason": {
        "description": "If the training job failed, the reason it failed.",
        "type": "string",
    },
}

