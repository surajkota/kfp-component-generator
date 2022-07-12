import os 

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

REQUIRED_ARGS = {
	"--hyper_parameter_tuning_job_config":
	""" '{"S3Uri":"s3://fake-bucket/data","S3DataType":"S3Prefix","S3DataDistributionType":"FullyReplicated"}' """,
	"--hyper_parameter_tuning_job_name":
	""" "job name example" """,
	"--tags":
	""" "[]" """,
	"--training_job_definition":
	""" "{}" """,
	"--training_job_definitions":
	""" '[{"ChannelName": "train", "DataSource": {"S3DataSource":{"S3Uri": "s3://fake-bucket/data","S3DataType":"S3Prefix","S3DataDistributionType": "FullyReplicated"}},"ContentType":"","CompressionType": "None","RecordWrapperType":"None","InputMode": "File"}]' """,
	"--warm_start_config":
	"'" + str(channelObj) + "'",
}

arguments = ""

for key in REQUIRED_ARGS:
	arguments = arguments + " " + key + " " + REQUIRED_ARGS[key]

file_loc = "code_gen/components/HyperParameterTuningJob1/src/HyperParameterTuningJob.py"

os.system("pwd")
os.system("python " + file_loc + arguments)