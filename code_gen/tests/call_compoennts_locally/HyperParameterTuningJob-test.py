import os 

"""
Call component.py locally
"""

# json object
channelObj = {
    "ChannelName": "",
    "DataSource": {
        "S3DataSource": {
            "S3Uri": "",
            "S3DataType": "S3Prefix",
            "S3DataDistributionType": "FullyReplicated",
        }
    },
    "CompressionType": "None",
    "RecordWrapperType": "None",
}

training_job_definition = {
    "AlgorithmSpecification": {
      "TrainingImage": "training_image",
      "TrainingInputMode": "File"
    },
    "InputDataConfig": [
      {
        "ChannelName": "train",
        "CompressionType": "None",
        "ContentType": "csv",
        "DataSource": {
          "S3DataSource": {
            "S3DataDistributionType": "FullyReplicated",
            "S3DataType": "S3Prefix",
            "S3Uri": 's3://xxx/xxx/output'
          }
        }
      },
      {
        "ChannelName": "validation",
        "CompressionType": "None",
        "ContentType": "csv",
        "DataSource": {
          "S3DataSource": {
            "S3DataDistributionType": "FullyReplicated",
            "S3DataType": "S3Prefix",
            "S3Uri": 's3://xxx/xxx/output'
          }
        }
      }
    ],
    "OutputDataConfig": {
      "S3OutputPath": "s3://xxx/xxx/output"
    },
    "ResourceConfig": {
      "InstanceCount": 2,
      "InstanceType": "ml.c4.2xlarge",
      "VolumeSizeInGB": 10
    },
    "RoleArn": "role",
    "StaticHyperParameters": {
      "eval_metric": "auc",
      "num_round": "100",
      "objective": "binary:logistic",
      "rate_drop": "0.3",
      "tweedie_variance_power": "1.4"
    },
    "StoppingCondition": {
      "MaxRuntimeInSeconds": 43200
    }
}

warm_start_config = {
	"ParentHyperParameterTuningJobs" : [
	{"HyperParameterTuningJobName" : 'MyParentTuningJob'}
	],
	"WarmStartType" : "IdenticalDataAndAlgorithm"
}

REQUIRED_ARGS = {
	"--hyper_parameter_tuning_job_config":
	""" '{"S3Uri":"s3://fake-bucket/data","S3DataType":"S3Prefix","S3DataDistributionType":"FullyReplicated"}' """,
	"--hyper_parameter_tuning_job_name":
	""" 'job name example' """,
	"--tags":
	""" '[]' """,
	"--training_job_definition":
	"'" + str(training_job_definition) + "'",
	"--training_job_definitions":
	""" '[]' """,
	"--warm_start_config":
	"'" + str(warm_start_config) + "'",
}

arguments = ""

for key in REQUIRED_ARGS:
	arguments = arguments + " " + key + " " + REQUIRED_ARGS[key]

file_loc = "code_gen/components/HyperParameterTuningJob/src/HyperParameterTuningJob.py"

# os.system("pwd")
os.system("python " + file_loc + arguments)