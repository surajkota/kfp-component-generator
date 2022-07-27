# Amazon SageMaker Component Generator

## Summary
With Amazon SageMaker Components for Kubeflow Pipelines (KFP), you can create and monitor training, tuning, endpoint deployment, and batch transform jobs in Amazon SageMaker. By running Kubeflow Pipeline jobs on Amazon SageMaker, you move data processing and training jobs from the Kubernetes cluster to Amazon SageMaker’s machine learning-optimized managed service. The job parameters, status, logs, and outputs from Amazon SageMaker are still accessible from the Kubeflow Pipelines UI.

## Components
Amazon SageMaker Components for Kubeflow Pipelines offer an alternative to launching compute-intensive jobs in Kubernetes and integrate the orchestration benefits of Kubeflow Pipelines. The following Amazon SageMaker components have been created to integrate 6 key Amazon SageMaker features into your ML workflows. You can create a Kubeflow Pipeline built entirely using these components, or integrate individual components into your workflow as needed. 

For an end-to-end tutorial using these components, see [Using Amazon SageMaker Components](https://sagemaker.readthedocs.io/en/stable/workflows/kubernetes/using_amazon_sagemaker_components.html).

For more example pipelines, see [Sample AWS SageMaker Kubeflow Pipelines](https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples).

There is no additional charge for using Amazon SageMaker Components for Kubeflow Pipelines. You incur charges for any Amazon SageMaker resources you use through these components.

## Repo Structure

The code generator is in [`code_gen`](https://github.com/rd-pong/kfp-component-generator/tree/main/code_gen)

```dotnetcli
code_gen
├── __init__.py
├── __pycache__
├── ack_crd         # Downloaded ACK CRD YAML files
├── assets          
├── common          # Classes and methods commonly used by components
├── components      # Components generated by the generator
├── generator       # Generator scripts
├── templates       # Templates used by the generator
└── tests           

```

## How to use the generator

Install the required packages `pip install -r requirements.txt`

Run `gen_main.py` in the project source directory. There are two options:

1. Specify crd as input arguments: `python code_gen/generator/gen_main.py --crd_name <crd_name> --container_image <container_image>`
2. Use arrow key to select CRD later from prompt: `python code_gen/generator/gen_main.py --container_image <container_image>`

Examples:
1. `python code_gen/generator/gen_main.py --crd_name "sagemaker.services.k8s.aws_trainingjobs.yaml" --container_image "rdpen/kfp-component-sagemaker:latest"`
2. `python code_gen/generator/gen_main.py --container_image "rdpen/kfp-component-sagemaker:latest"`

Sample output:
```dotnetcli
user@xxxxx kfp-component-generator % python code_gen/generator/gen_main.py --container_image "rdpen/kfp-component-sagemaker:latest"
RETRIEVED: latest release name v0.3.3
RETRIEVED: latest tag type tag
RETRIEVED: all crds
[?] Select the CRD you want to use:: sagemaker.services.k8s.aws_trainingjobs.yaml
   sagemaker.services.k8s.aws_modelbiasjobdefinitions.yaml
   sagemaker.services.k8s.aws_modelexplainabilityjobdefinitions.yaml
   sagemaker.services.k8s.aws_modelpackagegroups.yaml
   sagemaker.services.k8s.aws_modelpackages.yaml
   sagemaker.services.k8s.aws_modelqualityjobdefinitions.yaml
   sagemaker.services.k8s.aws_models.yaml
   sagemaker.services.k8s.aws_monitoringschedules.yaml
   sagemaker.services.k8s.aws_notebookinstancelifecycleconfigs.yaml
   sagemaker.services.k8s.aws_notebookinstances.yaml
   sagemaker.services.k8s.aws_processingjobs.yaml
 > sagemaker.services.k8s.aws_trainingjobs.yaml
   sagemaker.services.k8s.aws_transformjobs.yaml
   sagemaker.services.k8s.aws_userprofiles.yaml

DOWNLOADED: CRD path: code_gen/ack_crd/sagemaker.services.k8s.aws_trainingjobs.yaml
CREATED: code_gen/components/TrainingJob/src/TrainingJob_spec.py
CREATED: code_gen/components/TrainingJob/src/TrainingJob_component.py
CREATED: code_gen/components/TrainingJob/src/TrainingJob_request.yaml.tpl
CREATED: code_gen/components/TrainingJob/component.yaml
```

## How to run the generated components

There are two ways to run the components:
1. Run the component directly using `code_gen/tests/call_compoennts_locally/TrainingJob-test.py`
2. Run the component in the Kubeflow web dashboard using pipelines
    
### Prerequisite:

We need to create a IAM user and a IAM role for the component to run.

#### Configure EKS access for an IAM user (who is not the cluster creator)

1. Create an IAM user that has EKS permission policy. 
2. Enable the IAM user access to the cluster ([ref](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html))
    
    Decide which role to bind ([ref](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings))
    
    ```
    eksctl create iamidentitymapping \
        --cluster <cluster-name> \
        --region=<region-code> \
        --arn arn:aws:iam::<account-number>:user/<user-name> \
        --group system:masters \
        --no-duplicate-arns
    ```

#### Configure Sagemaker permissions for an IAM role

https://github.com/aws-controllers-k8s/sagemaker-controller/blob/main/samples/README.md#sagemaker-execution-iam-role

This roleARN will be used as user input in `code_gen/tests/call_compoennts_locally/TrainingJob-test.py` and `code_gen/tests/pipelines/TrainingJob-pipeline.py`

#### Create a S3 bucket

https://github.com/aws-controllers-k8s/sagemaker-controller/blob/main/samples/README.md#s3-bucket
    
### Run the component directly

Make sure you can connect to EKS:

- Configure current user to the one we created previously: `aws configure`
- Check the current identity: `aws sts get-caller-identity`
- Create or update the kubeconfig file for your cluster: `aws eks --region region update-kubeconfig --name cluster_name`
- Test your configuration: `kubectl get svc`

Follow [this guide](https://github.com/aws-controllers-k8s/sagemaker-controller/blob/main/samples/training/README.md#prerequisites) to upload S3 data and get proper image link. Stop at [Get an Image](https://github.com/aws-controllers-k8s/sagemaker-controller/blob/main/samples/training/README.md#get-an-image).

In `code_gen/tests/call_compoennts_locally/TrainingJob-test.py`, modify values with those associated with your account and training job.

In the project source directory, run `python3 code_gen/tests/call_compoennts_locally/TrainingJob-test.py`

### Run the component in the Kubeflow web dashboard

#### Store IAM user credential in K8s cluster

Store the IAM credentials as a aws-secret in kubernetes cluster. Then use those in the components.

Find the credentials of the IAM user created previously. Apply them to k8s cluster.

- Replace `AWS_ACCESS_KEY_IN_BASE64` and `AWS_SECRET_ACCESS_IN_BASE64`.
    > Note: To get base64 string you can do `echo -n $AWS_ACCESS_KEY_ID | base64`
- Change the namespace, make sure the secret is placed in the same namespace as the components got created 
    ```
    cat <<EOF | kubectl apply -f -
    apiVersion: v1
    kind: Secret
    metadata:
        name: aws-secret
        namespace: kubeflow-user-example-com
    type: Opaque
    data:
        AWS_ACCESS_KEY_ID: <AWS_ACCESS_KEY_IN_BASE64>
        AWS_SECRET_ACCESS_KEY: <AWS_SECRET_ACCESS_IN_BASE64>
    EOF
    ```

#### Build docker

1. Check image name (implementation.container.image) is correct in the generated component.yaml
2. In the project source directory, create and push docker image:
    ```
    image_name=rdpen/kfp-component-sagemaker
    image_tag=44
    full_image_name=${image_name}:${image_tag}
    
    docker build --platform=linux/amd64 -t "${full_image_name}" .
    docker push "$full_image_name"
    ```

#### Upload pipeline and run
1. In `code_gen/components/TrainingJob/pipeline`, compile the pipeline:
    `dsl-compile --py TrainingJob-pipeline.py --output TrainingJob-pipeline.tar.gz`  
2. In the Kubeflow UI, upload this compiled pipeline specification (the .tar.gz file) and click on create run.






