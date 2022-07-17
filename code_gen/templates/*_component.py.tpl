import logging
from typing import Dict
from enum import Enum, auto
from sagemaker.image_uris import retrieve
import yaml

from code_gen.components.TrainingJob.src.TrainingJob_spec import (
    ${INPUT_CLASS_NAME},
    ${OUTPUT_CLASS_NAME},
    ${SPEC_CLASS_NAME},
)
from code_gen.common.sagemaker_component import (
    SageMakerComponent,
    ComponentMetadata,
    SageMakerJobStatus,
    DebugRulesStatus,
)
from code_gen.generator.utils import snake_to_camel


@ComponentMetadata(
    name="SageMaker - ${CRD_NAME}",
    description="",
    spec=${SPEC_CLASS_NAME},
)
class ${COMPONENT_CLASS_NAME}(SageMakerComponent):
    """SageMaker component for training."""

    def Do(self, spec: ${SPEC_CLASS_NAME}):
        self.ACK_JOB_NAME = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ACK-${CRD_NAME}"
        )
        # print(self.ACK_JOB_NAME)
        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: ${INPUT_CLASS_NAME},
        outputs: ${OUTPUT_CLASS_NAME},
    ) -> Dict:

        with open(
            "code_gen/components/TrainingJob/src/TrainingJob-request.yaml.tpl", "r"
        ) as job_request_outline:
            job_request_dict = yaml.load(job_request_outline, Loader=yaml.FullLoader)
            job_request_spec = job_request_dict["spec"]

            for para in vars(inputs):
                camel_para = snake_to_camel(para)
                if camel_para in job_request_spec:
                    job_request_spec[camel_para] = getattr(inputs, para)

            # job_request_dict["spec"] = job_request_spec
            job_request_dict["metadata"]["name"] = self.ACK_JOB_NAME

            print(job_request_dict)

            out_loc = "code_gen/components/TrainingJob/src/TrainingJob-request.yaml"
            with open(out_loc, "w+") as f:
                yaml.dump(job_request_dict, f, default_flow_style=False)
            print("CREATED: " + out_loc)


if __name__ == "__main__":
    import sys

    spec = ${SPEC_CLASS_NAME}(sys.argv[1:])

    component = ${COMPONENT_CLASS_NAME}()
    component.Do(spec)
