import yaml

with open("code_gen/components/train/pipeline/ack_training_job_request.yaml") as f:
    crd_dict = yaml.load(f, Loader=yaml.FullLoader)

print(crd_dict['spec'])

for key in crd_dict['spec']:
    print(key)
    

# with open("test.yaml", 'w+') as f:
#     yaml.dump(crd_dict, f, default_flow_style=False)