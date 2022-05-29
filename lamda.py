import json
import boto3

def mail_to_user(data, mail_id):
    """Connects to ses service.

    Args:
      data[0]:Subject of mail.
      data[1]:Body of mail

    Returns:
      Sends the mail.

    Raises:
      MessageRejected: If not in prod then cannot send to un-veririfed mail ids.
    """
    ses = boto3.client('ses')
    try:
        # TODO USER MAIL ID
        ses.send_email(
        Source='test@gmail.com',
        Destination={
            'ToAddresses': [
                mail_id,
            ],
        },
        Message={
            'Subject': {
                'Data': data[0],
            },
            'Body': {
                'Text': {
                    'Data': data[1],
                },
                'Html':{
                    'Data': data[1],
                }
            }
        },)
    except ses.exceptions.MessageRejected:
        print("Not in production mode cannot send to unverified email-id")
    except Exception as e:
        print(e)


def state_save_without_tags(name):
    """Connects to ssm service.
    Check if mail is send 6 times.
    else add the counter in ssm

    Args:
      name:Id of the instance.

    Returns:
      True: Needs to delete the instance
      False: No Need to uninstall the instance and counter is added

    """
    ssm = boto3.client('ssm')
    try:
        details = ssm.get_parameter(Name=name, WithDecryption= False)
        count = int(details['Parameter']['Version'])
    except ssm.exceptions.ParameterNotFound:
        count = 0
    count+=1
    if(count > 6):
        ssm.delete_parameter(Name = name)
        return True
    else:
        ssm.put_parameter(
            Name=name,
            Description=str(count),
            Value='string',
            Type='String',
            Overwrite=True,
            AllowedPattern='string',
            Tier='Standard'
        )
        return False

def lambda_handler(event, context):
    AWS_REGION = 'us-east-1'
    EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)

    instances = EC2_RESOURCE.instances.all()
    log_details = ""
    # loops through each instance
    for instance in instances:
        tags = instance.tags
        is_created_by = False
        is_environment = False
        is_name = False
        if instance.state['Name'] != 'terminated':
            if tags:
                for tag in tags: 
                    if 'Key' in tag:
                        if tag['Key'] == 'created by' :
                            is_created_by = True
                            mail_id = tag['Value']
                        if tag['Key'] == 'Environment'  :
                            is_environment = True
                        if tag['Key'] == 'Name' :
                            is_name = True
            
            # assuming if created by tag == none we need to delete the instance
            else:
                instance.terminate()
                log_details+=f"Instance deleted as is None : {instance.id}\n"

            if  is_created_by and (not is_name or not is_environment):
                    if state_save_without_tags(instance.id) :
                        data = f'''<br><br> InstanceId = {instance.id} is being terminated since the 
                                required tags has not been added!!!!<br><br>'''
                        subject=f"Instance Termination{instance.id}"
                        
                        mail_to_user([subject,data] , mail_id)
                        instance.terminate()
                        log_details+= f"Terminated Instace:{instance.id}\n"
                    else:
                        data = f"<br><br> InstanceId = {instance.id}<br><br>"
                        if not is_name:
                            data+= "Add 'Name' tag to the instance<br>"
                        if not is_environment:
                            data+= "Add 'Environment' tag to the instance<br>"
                        subject="Add the required tags for the instance"
                        mail_to_user([subject,data] , mail_id)
                        log_details+= f"send mail to owner of:{instance.id}\n"
                         
    return {
        'statusCode': 200,
        'body': json.dumps(log_details)
    }
