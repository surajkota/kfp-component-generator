apiVersion: sagemaker.services.k8s.aws/v1alpha1
kind: ${CRD_NAME}
metadata:
  name: ack-${CRD_NAME_LOWER}-${RAND_NUM}
spec:
${JOB_REQUEST_OUTLINE_SPEC}