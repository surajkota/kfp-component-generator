name: "Sagemaker - ${CRD_NAME}"
description: Train Machine Learning and Deep Learning Models using SageMaker
inputs:

  ###########################GENERATED SECTION BELOW############################
  ${YAML_INPUTS}
  ###########################GENERATED SECTION ABOVE############################

outputs:

  ###########################GENERATED SECTION BELOW############################
  ${YAML_OUTPUTS}
  ###########################GENERATED SECTION ABOVE############################

implementation:
  container:
    image: rdpen/kfp-component-sagemaker:latest
    command: [python3]
    args:
      - code_gen/train/src/train.py

      ###########################GENERATED SECTION BELOW############################
      ${YAML_ARGS}
      ###########################GENERATED SECTION ABOVE############################

