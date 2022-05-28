import boto3
AWS_REGION = 'us-east-1'
ssm = boto3.client('ssm')
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)

instances = EC2_RESOURCE.instances.all()
print(ssm.describe_parameters())

# response = ssm.put_parameter(
#     Name='i-06fc58bfe57c37e42',
#     Description='2',
#     Value='string',
#     Type='String',
#     Overwrite=True,
#     AllowedPattern='string',
#     Tier='Standard'
# )
# print(response)

for instance in instances:
    print(f'EC2 instance {instance.id}" information:')
    print(f'Instance state: {instance.state["Name"]}')
    print(f'Instance AMI: {instance.image.id}')
    print(f'Instance platform: {instance.platform}')
    print(f'Instance type: "{instance.instance_type}')
    print(f'Piblic IPv4 address: {instance.public_ip_address}')
    print(f'Tags :{instance.tags}')
    tags = instance.tags
    is_created_by = False
    is_environment = False
    is_name = False
    for tag in tags: 
        if 'Key' in tag:
            if tag['Key'] == 'created by' :
                is_created_by = True
            if tag['Key'] == 'Environment' and is_created_by:
                is_environment = True
            if tag['Key'] == 'Name' and is_created_by:
                is_name = True
    print(is_created_by, is_name, is_environment)

    print('-'*60)

# response = ec2.describe_instances()
# instances = response['Reservations']
# for intance in instances:
#     print(intance['Instances'][0]['InstanceId']) 

# for instance in instances:
    # print(instance)
# print(ec2.list_identities())
# print('Regions:', response['Regions'])