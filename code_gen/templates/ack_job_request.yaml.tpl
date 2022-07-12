apiVersion: sagemaker.services.k8s.aws/v1alpha1
kind: ${CRD_NAME}
metadata:
  name: ${ACK_JOB_NAME}
spec:
${JOB_REQUEST_SPEC}