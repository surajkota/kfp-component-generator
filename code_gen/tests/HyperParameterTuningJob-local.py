from code_gen.components.HyperParameterTuningJob1.src.HyperParameterTuningJob import main

REQUIRED_ARGS = [
        "--hyper_parameter_tuning_job_config",
        """{"S3Uri": "s3://fake-bucket/data","S3DataType":"S3Prefix","S3DataDistributionType": "FullyReplicated"}""",
        "--hyper_parameter_tuning_job_name",
        "job name example",
        "--tags",
        "[]",
        "--training_job_definition",
        "{}",
        "--training_job_definitions",
        '[{"ChannelName": "train", "DataSource": {"S3DataSource":{"S3Uri": "s3://fake-bucket/data","S3DataType":"S3Prefix","S3DataDistributionType": "FullyReplicated"}},"ContentType":"","CompressionType": "None","RecordWrapperType":"None","InputMode": "File"}]',
        "--warm_start_config",
        "{}",
]

main(REQUIRED_ARGS)