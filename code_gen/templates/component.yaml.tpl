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
    image: ${COMPONENT_CONTAINER_IMAGE}
    command: [python3]
    args:
      - code_gen/components/${CRD_NAME}/src/${CRD_NAME}.py
      ###########################GENERATED SECTION BELOW############################
      ${YAML_ARGS}
      ###########################GENERATED SECTION ABOVE############################

