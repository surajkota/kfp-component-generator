import unittest
import os

from code_gen.generator.utils import (
    camel_to_snake,
    get_class_names,
    get_crd_info,
    parse_crd,
    snake_to_camel,
    write_snippet_to_file,
)


class utilsTestCase(unittest.TestCase):
    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake("Test"), "test")
        self.assertEqual(camel_to_snake("TestCase"), "test_case")
        self.assertEqual(camel_to_snake("testCaseTest"), "test_case_test")
        self.assertEqual(camel_to_snake("roleARN"), "role_arn")
        self.assertEqual(camel_to_snake("roleARNTest"), "role_arn_test")

    def test_snake_to_camel(self):
        self.assertEqual(snake_to_camel("test"), "test")
        self.assertEqual(snake_to_camel("test_case"), "testCase")
        self.assertEqual(snake_to_camel("test_case_test"), "testCaseTest")
        self.assertEqual(snake_to_camel("role_arn"), "roleARN")
        # self.assertEqual(snake_to_camel('role_arn_test'), 'roleARNTest')

    def test_parse_crd(self):
        input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
            "code_gen/tests/unit_tests/generator/files/test_crd.yaml"
        )
        input_spec_all_sample = {
            "appName": {"description": "The name of the app.", "type": "string"},
            "appType": {
                "description": "The type of app. Supported apps are JupyterServer and KernelGateway. TensorBoard is not supported.",
                "type": "string",
            },
            "domainID": {"description": "The domain ID.", "type": "string"},
            "resourceSpec": {
                "description": "The instance type and the Amazon Resource Name (ARN) of the SageMaker image created on the instance.",
                "properties": {
                    "instanceType": {"type": "string"},
                    "lifecycleConfigARN": {"type": "string"},
                    "sageMakerImageARN": {"type": "string"},
                    "sageMakerImageVersionARN": {"type": "string"},
                },
                "type": "object",
            },
            "tags": {
                "description": "Each tag consists of a key and an optional value. Tag keys must be unique per resource.",
                "items": {
                    "description": "A tag object that consists of a key and an optional value, used to manage metadata for SageMaker Amazon Web Services resources.",
                    "properties": {
                        "key": {"type": "string"},
                        "value": {"type": "string"},
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "userProfileName": {
                "description": "The user profile name.",
                "type": "string",
            },
        }
        output_statuses_sample = {
            "ackResourceMetadata": {
                "description": "All CRs managed by ACK have a common `Status.ACKResourceMetadata` member that is used to contain resource sync state, account ownership, constructed ARN for the resource",
                "properties": {
                    "arn": {
                        "description": "ARN is the Amazon Resource Name for the resource.",
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
            "conditions": {
                "description": "describe the various terminal states of the CR and its backend AWS service API resource",
                "items": {
                    "description": "Condition is the common struct used by all CRDs managed by ACK service controllers to indicate terminal states of the CR and its backend AWS service API resource",
                    "properties": {
                        "lastTransitionTime": {
                            "description": "Last time the condition transitioned from one status to another.",
                            "format": "date-time",
                            "type": "string",
                        },
                        "message": {
                            "description": "A human readable message indicating details about the transition.",
                            "type": "string",
                        },
                        "reason": {
                            "description": "The reason for the condition's last transition.",
                            "type": "string",
                        },
                        "status": {
                            "description": "Status of the condition, one of True, False, Unknown.",
                            "type": "string",
                        },
                        "type": {
                            "description": "Type is the type of the Condition",
                            "type": "string",
                        },
                    },
                    "required": ["status", "type"],
                    "type": "object",
                },
                "type": "array",
            },
            "status": {"description": "The status.", "type": "string"},
        }

        self.assertListEqual(
            input_spec_required, ["appName", "appType", "domainID", "userProfileName"]
        )
        self.assertDictEqual(input_spec_all, input_spec_all_sample)
        self.assertDictEqual(output_statuses, output_statuses_sample)
        self.assertEqual(crd_name, "App")

    def test_get_crd_info(self):
        group, version, plural, namespace = get_crd_info(
            "code_gen/tests/unit_tests/generator/files/test_crd.yaml"
        )

        self.assertEqual(group, "sagemaker.services.k8s.aws")
        self.assertEqual(version, "v1alpha1")
        self.assertEqual(plural, "apps")
        self.assertEqual(namespace, "default")

    def test_get_class_names(self):
        self.assertEqual(
            get_class_names(""),
            (
                "SageMakerInputs",
                "SageMakerOutputs",
                "SageMakerSpec",
                "SageMakerComponent",
            ),
        )
        self.assertEqual(
            get_class_names("Train"),
            (
                "SageMakerTrainInputs",
                "SageMakerTrainOutputs",
                "SageMakerTrainSpec",
                "SageMakerTrainComponent",
            ),
        )

    def test_write_snippet_to_file(self):
        replace_dict = {
            "CRD_NAME": "App",
            "INPUT_CLASS_NAME": "SageMakerXxxxInputs",
        }

        write_snippet_to_file(
            replace_dict,
            "code_gen/tests/unit_tests/generator/files/test_template.tpl",
            "code_gen/tests/unit_tests/generator/files/",
            "test_template_replaced.txt",
        )

        self.assertTrue(
            os.path.exists(
                "code_gen/tests/unit_tests/generator/files/test_template_replaced.txt"
            )
        )

        with open(
            "code_gen/tests/unit_tests/generator/files/test_template_replaced.txt"
        ) as f:
            content = f.read()
            self.assertEqual(
                content,
                """App-controller
    SageMakerXxxxInputs""",
            )

        os.remove(
            "code_gen/tests/unit_tests/generator/files/test_template_replaced.txt"
        )


if __name__ == "__main__":
    group, version, plural, namespace = get_crd_info(
        "code_gen/tests/unit_tests/generator/files/test_crd.yaml"
    )
    print(group, version, plural, namespace)
