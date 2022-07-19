import logging
from typing import Dict
from enum import Enum, auto
from sagemaker.image_uris import retrieve
import yaml
from kubernetes import client, config, utils


from code_gen.components.TrainingJob.src.TrainingJob_spec import (
    SageMakerTrainingJobInputs,
    SageMakerTrainingJobOutputs,
    SageMakerTrainingJobSpec,
)
from code_gen.common.sagemaker_component import (
    SageMakerComponent,
    ComponentMetadata,
    SageMakerJobStatus,
    DebugRulesStatus,
)
from code_gen.generator.utils import snake_to_camel


@ComponentMetadata(
    name="SageMaker - TrainingJob",
    description="",
    spec=SageMakerTrainingJobSpec,
)
class SageMakerTrainingJobComponent(SageMakerComponent):
    """SageMaker component for training."""

    def Do(self, spec: SageMakerTrainingJobSpec):
        # set parameters
        self.ack_job_name = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ack-trainingjob"
        )
        self.group_name = "sagemaker.services.k8s.aws"
        self.version_name = "v1alpha1"
        self.plural_name = "trainingjobs"
        self.component_dir = "code_gen/components/TrainingJob/"
        self.job_request_outline_location = (
            self.component_dir + "src/TrainingJob-request.yaml.tpl"
        )
        self.job_request_location = self.component_dir + "src/TrainingJob-request.yaml"

        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ) -> Dict:

        return super()._create_job_request(inputs, outputs)

    def _submit_job_request(self, request: Dict) -> object:
        # list pods test
        # ret = self._k8s_api_client.list_pod_for_all_namespaces(watch=False)
        # for i in ret.items:
        #     print(
        #         "%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
        #     )
        # jobs = list()
        # jobs.append(request)

        print("ack job name: " + request["metadata"]["name"])
        print("Sagemaker name: " + request["spec"]["trainingJobName"])

        # utils.create_from_yaml(
        #     k8s_client=self._k8s_api_client, yaml_objects=jobs, verbose=True
        # )

    def _get_job_status(self):
        job_statuses = super()._get_job_status()
        print(job_statuses["trainingJobStatus"])


if __name__ == "__main__":
    import sys

    spec = SageMakerTrainingJobSpec(sys.argv[1:])

    component = SageMakerTrainingJobComponent()
    component.Do(spec)
