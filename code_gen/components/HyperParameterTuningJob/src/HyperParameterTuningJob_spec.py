"""Specification for the SageMaker - HyperParameterTuningJob"""

from dataclasses import dataclass

from typing import List
from code_gen.common.sagemaker_component_spec import (
    SageMakerComponentSpec,
    SageMakerComponentBaseOutputs,
)
from code_gen.common.spec_input_parsers import SpecInputParsers
from code_gen.common.common_inputs import (
    SageMakerComponentInput as Input,
    SageMakerComponentOutput as Output,
    SageMakerComponentInputValidator as InputValidator,
    SageMakerComponentOutputValidator as OutputValidator,
)


@dataclass(frozen=True)
class SageMakerHyperParameterTuningJobInputs:
    """Defines the set of inputs for the HyperParameterTuningJob component."""
    
    hyper_parameter_tuning_job_config: Input
    hyper_parameter_tuning_job_name: Input
    tags: Input
    training_job_definition: Input
    training_job_definitions: Input
    warm_start_config: Input


@dataclass
class SageMakerHyperParameterTuningJobOutputs(SageMakerComponentBaseOutputs):
    """Defines the set of outputs for the HyperParameterTuningJob component."""
    
    ack_resource_metadata: Output
    best_training_job: Output
    conditions: Output
    failure_reason: Output
    hyper_parameter_tuning_job_status: Output
    overall_best_training_job: Output


class SageMakerHyperParameterTuningJobSpec(
    SageMakerComponentSpec[SageMakerHyperParameterTuningJobInputs, SageMakerHyperParameterTuningJobOutputs]
):
    INPUTS: SageMakerHyperParameterTuningJobInputs = SageMakerHyperParameterTuningJobInputs(
        
        hyper_parameter_tuning_job_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="The HyperParameterTuningJobCon",
            required=True
        ), 
        hyper_parameter_tuning_job_name=InputValidator(
            input_type=str,
            description="The name of the tuning job. Th",
            required=True
        ), 
        tags=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="An array of key-value pairs. Y",
            required=False
        ), 
        training_job_definition=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="The HyperParameterTrainingJobD",
            required=False
        ), 
        training_job_definitions=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="A list of the HyperParameterTr",
            required=False
        ), 
        warm_start_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Specifies the configuration fo",
            required=False
        ), 
    )
    
    OUTPUTS = SageMakerHyperParameterTuningJobOutputs(
        
        ack_resource_metadata=OutputValidator(
            description="All CRs managed by ACK have a ",
        ), 
        best_training_job=OutputValidator(
            description="A TrainingJobSummary object th",
        ), 
        conditions=OutputValidator(
            description="All CRS managed by ACK have a ",
        ), 
        failure_reason=OutputValidator(
            description="If the tuning job failed, the ",
        ), 
        hyper_parameter_tuning_job_status=OutputValidator(
            description="The status of the tuning job: ",
        ), 
        overall_best_training_job=OutputValidator(
            description="If the hyperparameter tuning j",
        ), 
    )

    def __init__(self, arguments: List[str]):
        super().__init__(arguments, SageMakerHyperParameterTuningJobInputs, SageMakerHyperParameterTuningJobOutputs)

    @property
    def inputs(self) -> SageMakerHyperParameterTuningJobInputs:
        return self._inputs

    @property
    def outputs(self) -> SageMakerHyperParameterTuningJobOutputs:
        return self._outputs

    @property
    def output_paths(self) -> SageMakerHyperParameterTuningJobOutputs:
        return self._output_paths

