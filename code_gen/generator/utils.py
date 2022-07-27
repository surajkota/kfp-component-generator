import random
import inquirer
import requests
import urllib.request
import yaml, re, os
from string import Template
import string
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast
from code_gen.common.spec_input_parsers import SpecInputParsers


def camel_to_snake(name):
    """Convert camel case to snake case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name):
    """Convert snake case to camel case."""
    if name == "role_arn":
        return "roleARN"
    temp = name.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def parse_crd(_file_path):
    """Read in ACK CRD YAML file from file location Parse file and get
    fields."""

    with open(_file_path, "r") as crd_file:
        crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

        _input_spec_required = crd_dict["spec"]["versions"][0]["schema"][
            "openAPIV3Schema"
        ]["properties"]["spec"]["required"]
        _input_spec_all = crd_dict["spec"]["versions"][0]["schema"]["openAPIV3Schema"][
            "properties"
        ]["spec"]["properties"]
        _output_statuses = crd_dict["spec"]["versions"][0]["schema"]["openAPIV3Schema"][
            "properties"
        ]["status"]["properties"]
        _crd_name = crd_dict["spec"]["names"]["kind"]

    return _input_spec_required, _input_spec_all, _output_statuses, _crd_name


def get_crd_info(_file_path):
    """Read in ACK CRD YAML file from file location Parse file and get crd
    information: name, plural, version, namespace."""
    with open(_file_path, "r") as crd_file:
        crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

    _group = crd_dict["spec"]["group"]
    _plural = crd_dict["spec"]["names"]["plural"]
    _version = crd_dict["spec"]["versions"][0]["name"]
    _namespace = "default" if crd_dict["spec"]["scope"] == "Namespaced" else ""

    return _group, _version, _plural, _namespace


def get_class_names(_crd_name):
    """Get component class names from CRD name."""
    _input_class_name = "SageMaker" + _crd_name + "Inputs"
    _output_class_name = "SageMaker" + _crd_name + "Outputs"
    _spec_class_name = "SageMaker" + _crd_name + "Spec"
    _component_class_name = "SageMaker" + _crd_name + "Component"

    return (
        _input_class_name,
        _output_class_name,
        _spec_class_name,
        _component_class_name,
    )


def write_snippet_to_file(_replace_dict, _template_path, _out_file_dir, _out_file_name):
    """Open template file at _template_path Substite placeholders in templates
    following mapping _replace_dict Create a dir _out_file_dir, if does not
    exist Write output file stream to file _out_file_path."""

    _out_file_path = _out_file_dir + _out_file_name
    
    # open and replace placeholders in templates
    with open(_template_path) as t:
        template = string.Template(t.read())
        file_draft = template.safe_substitute(_replace_dict)

    # if output dir does not exist, create one and write to file
    if not os.path.exists(_out_file_dir):
        os.makedirs(_out_file_dir)
    with open(_out_file_path, "w+") as f:
        f.write(file_draft)

    print("CREATED: " + _out_file_path)


def fetch_all_crds():
    """Fetch all ACK CRD from latest release."""

    try:
        releases = requests.get(
            "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/releases/latest"
        ).json()
        latest_release_ver_name = releases["name"]
    except:
        print("Error fetching latest release, see response below")
        print(releases)
        return None
    
    print("RETRIEVED: latest release name " + latest_release_ver_name)
    
    latest_tag = requests.get(
        "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/git/ref/tags/"
        + latest_release_ver_name
    ).json()
    latest_tag_sha = latest_tag["object"]["sha"]
    latest_tag_type = latest_tag["object"]["type"]
    
    print("RETRIEVED: latest tag type " + latest_tag_type)

    if latest_tag_type == "tag":
        latest_tag_commit = requests.get(latest_tag["object"]["url"]).json()
        latest_tag_commit_sha = latest_tag_commit["object"]["sha"]
    elif latest_tag_type == "commit":
        latest_tag_commit_sha = latest_tag_sha

    crds = requests.get(
        "https://api.github.com/repos/aws-controllers-k8s/sagemaker-controller/contents/config/crd/bases?ref="
        + latest_tag_commit_sha
    ).json()
    
    print("RETRIEVED: all crds")

    return crds


def download_selected_crd(crds, crd_selected):
    """Download selected ACK CRD from latest release."""

    list_of_crd_names = []

    for crd in crds:
        list_of_crd_names.append(crd["name"])

    # if crd_selected is not configured, prompt user to select a crd_name
    if crd_selected is None:
        questions = [
            inquirer.List(
                "crd_name_chosen",
                message="Select the CRD you want to use:",
                choices=list_of_crd_names,
            ),
        ]
        crd_name_chosen = inquirer.prompt(questions).get("crd_name_chosen")
    else:
        crd_name_chosen = crd_selected

    # download the CRD file to local
    crd_download_url = ""
    for item in crds:
        if item["name"] == crd_name_chosen:
            crd_download_url = item["download_url"]
            break

    if crd_download_url == "":
        print("Error: CRD not found")
        return
    else:
        download_path = "code_gen/ack_crd/{}".format(crd_name_chosen)
        urllib.request.urlretrieve(crd_download_url, download_path)
        print("DOWNLOADED: CRD path: {}".format(download_path))
        return download_path
