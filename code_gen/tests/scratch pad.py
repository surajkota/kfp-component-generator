import os
from unicodedata import name
from venv import create
import yaml
from kubernetes import client, config, utils
from kubernetes.client.api_client import ApiClient
import distutils.util as util

#############################################################################################################
# # # organize the input spec, sort alphabetically by key
# # with open("code_gen/components/TrainingJob1/pipeline/ack_training_job_request.yaml") as f:
# with open("code_gen/components/HyperParameterTuningJob1/pipeline/my-hyperparameter-job.yaml") as f:
#     crd_dict = yaml.load(f, Loader=yaml.FullLoader)

# print(crd_dict['spec'])

# # for key in crd_dict['spec']:
# #     print(key)

# # with open("test.yaml", 'w+') as f:
# #     yaml.dump(crd_dict, f, default_flow_style=False)

#############################################################################################################
# test submit yaml to kubectl
## configure kubectl client
# config.load_kube_config()
# k8s_api_client = client.CoreV1Api()


# def _get_k8s_api_client() -> ApiClient:
#     # Create new client everytime to avoid token refresh issues
#     # https://github.com/kubernetes-client/python/issues/741
#     # https://github.com/kubernetes-client/python-base/issues/125
#     if bool(util.strtobool(os.environ.get("LOAD_IN_CLUSTER_KUBECONFIG", "false"))):
#         config.load_incluster_config()
#         return ApiClient()
#     return config.new_client_from_config()


# def create_custom_resource(namespace, version, plural, group, custom_resource: dict):
#     _api_client = _get_k8s_api_client()
#     _api = client.CustomObjectsApi(_api_client)

#     if namespace is None:
#         return _api.create_cluster_custom_object(
#             group.lower(),
#             version.lower(),
#             plural.lower(),
#             custom_resource,
#         )
#     return _api.create_namespaced_custom_object(
#         group.lower(),
#         version.lower(),
#         namespace.lower(),
#         plural.lower(),
#         custom_resource,
#     )


# cr = {
#     "apiVersion": "sagemaker.services.k8s.aws/v1alpha1",
#     "kind": "TrainingJob",
#     "metadata": {"name": "ack-trainingjob-20220719154251"},
#     "spec": {
#         "algorithmSpecification": {
#             "trainingImage": "746614075791.dkr.ecr.us-west-1.amazonaws.com/sagemaker-xgboost:1.2-1",
#             "trainingInputMode": "File",
#         },
#         "checkpointConfig": None,
#         "debugHookConfig": None,
#         "debugRuleConfigurations": None,
#         "enableInterContainerTrafficEncryption": None,
#         "enableManagedSpotTraining": None,
#         "enableNetworkIsolation": None,
#         "environment": None,
#         "experimentConfig": None,
#         "hyperParameters": {
#             "max_depth": "5",
#             "gamma": "4",
#             "eta": "0.2",
#             "min_child_weight": "6",
#             "objective": "multi:softmax",
#             "num_class": "10",
#             "num_round": "10",
#         },
#         "inputDataConfig": [
#             {
#                 "channelName": "train",
#                 "dataSource": {
#                     "s3DataSource": {
#                         "s3DataType": "S3Prefix",
#                         "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/train",
#                         "s3DataDistributionType": "FullyReplicated",
#                     }
#                 },
#                 "contentType": "text/libsvm",
#                 "compressionType": "None",
#             },
#             {
#                 "channelName": "validation",
#                 "dataSource": {
#                     "s3DataSource": {
#                         "s3DataType": "S3Prefix",
#                         "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/validation",
#                         "s3DataDistributionType": "FullyReplicated",
#                     }
#                 },
#                 "contentType": "text/libsvm",
#                 "compressionType": "None",
#             },
#         ],
#         "outputDataConfig": {"s3OutputPath": "s3://ack-sagemaker-bucket-402026529871"},
#         "profilerConfig": None,
#         "profilerRuleConfigurations": None,
#         "resourceConfig": {
#             "instanceCount": 1,
#             "instanceType": "ml.m4.xlarge",
#             "volumeSizeInGB": 5,
#         },
#         "roleARN": "arn:aws:iam::402026529871:role/ack-sagemaker-execution-role-402026529871",
#         "stoppingCondition": {"maxRuntimeInSeconds": 86400},
#         "tags": None,
#         "tensorBoardOutputConfig": None,
#         "trainingJobName": "training-job-from-ack-kfp-22",
#         "vpcConfig": None,
#     },
# }

# group = "sagemaker.services.k8s.aws"
# version = "v1alpha1"
# plural = "trainingjobs"

# _k8s_custom_client = client.CustomObjectsApi(_get_k8s_api_client())

# # # get all training jobs

# # api_response = _k8s_custom_client.list_cluster_custom_object(
# #     group=group,
# #     version=version,
# #     plural=plural,
# # )
# # for job in api_response["items"]:
# #     print("ACK name: " + job["metadata"]["name"])
# #     # print("Sagemaker name: " + job["spec"]["trainingJobName"])
# #     # print(job["status"]["trainingJobStatus"])


# # submit ack job
# # utils.create_from_yaml(k8s_client=k8s_api_client, yaml_file="code_gen/components/TrainingJob/src/TrainingJob_request.yaml", verbose=True)

# create_custom_resource(
#     namespace="default", version=version, plural=plural, group=group, custom_resource=cr
# )

#############################################################################################################
# retrive CRD YAML from github
# # https://stackoverflow.com/questions/67040794/how-can-i-get-the-commit-hash-of-the-latest-release-from-github-api

# retrive CRD YAML from github
import requests
import inquirer
import urllib.request


# releases = requests.get(
#     "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/releases/latest"
# ).json()
# latest_version_name = releases["name"]

# # print(latest_version_name)

# # tags = requests.get(
# #     "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/tags"
# # ).json()
# # latest_tag_sha = tags[0]["commit"]["sha"]
# #
# # print(latest_tag_sha)

# latest_tag = requests.get(
#     "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/git/ref/tags/" + latest_version_name
# ).json()
# latest_tag_sha = latest_tag["object"]["sha"]
# latest_tag_type = latest_tag["object"]["type"]

# # print(latest_tag_type, latest_tag_sha)

# if latest_tag_type == "tag":
#     latest_tag_commit = requests.get(latest_tag["object"]["url"]).json()
#     latest_tag_commit_sha = latest_tag_commit["object"]["sha"]
# elif latest_tag_type == "commit":
#     latest_tag_commit_sha = latest_tag_sha

# # print(latest_tag_commit_sha)

# crds = requests.get("https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/contents/config/crd/bases?ref=" + latest_tag_commit_sha).json()

# list_of_crd_names = []

# for crd in crds:
#     list_of_crd_names.append(crd["name"])

# questions = [
#     inquirer.List(
#         "crd_chosen",
#         message="Select the CRD you want to use:",
#         choices=list_of_crd_names,
#     ),
# ]
# crd_chosen = inquirer.prompt(questions).get("crd_chosen")

# for item in crds:
#     if item["name"] == crd_chosen:
#         crd_download_url = item["download_url"]
#         break

# # print(crd_download_url)

# urllib.request.urlretrieve(crd_download_url, "code_gen/ack_crd_v0.3.3/{}".format(crd_chosen))

