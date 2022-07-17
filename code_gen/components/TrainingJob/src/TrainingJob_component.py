import logging
from typing import Dict
from enum import Enum, auto
from sagemaker.image_uris import retrieve
import yaml

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


@ComponentMetadata(
    name="SageMaker - Training Job",
    description="Train Machine Learning and Deep Learning Models using SageMaker",
    spec=SageMakerTrainingJobSpec,
)
class SageMakerTrainingJobComponent(SageMakerComponent):
    """SageMaker component for training."""

    def Do(self, spec: SageMakerTrainingJobSpec):
        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ) -> Dict:

        print("test")
        # with open(
        #     "code_gen/components/TrainingJob/src/TrainingJob-request.yaml.tpl", "r"
        # ) as job_request_outline:
        #     job_request_dict = yaml.load(job_request_outline, Loader=yaml.FullLoader)
        #     job_request_spec = job_request_dict["spec"]
        #     for para in vars(_args):
        #         camel_para = snake_to_camel(para)
        #         if camel_para in job_request_spec:
        #             job_request_spec[camel_para] = getattr(_args, para)

        #     # print(job_request_spec)

        #     job_request_dict["spec"] = job_request_spec

        #     # print(job_request_dict)

        #     out_loc = "code_gen/components/TrainingJob/src/TrainingJob-request.yaml"
        #     with open(out_loc, "w+") as f:
        #         yaml.dump(job_request_dict, f, default_flow_style=False)
        #     print("CREATED: " + out_loc)


if __name__ == "__main__":
    import sys

    spec = SageMakerTrainingJobSpec(sys.argv[1:])

    component = SageMakerTrainingJobComponent()
    component.Do(spec)
