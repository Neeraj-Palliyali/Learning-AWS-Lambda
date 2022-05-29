#Lamda Function To check for tags

##Description
Develop a simple python serverless lambda function which would terminate all EC2 instances which don’t follow a tagging criteria. (A free tier AWS account would work).

##Deployment steps
***

Step1:Goto iam console
Step2:Create a lamda function role from iam console
Step3:required policies
    >AmazonEC2ReadOnlyAccess
    >AmazonSSMFullAccess
    >AmazonSESFullAccess
Step4:Name the role(assuming "lamda_ec2_tag_checker") and save

Step5:Goto AWS Lamda functions page
Step6:Create an function 
    >name (any name)(assuming ec2_tag_checker)
    >runtime(Python 3.7)
    >execution role : lamda_ec2_tag_checker
    >create function


Step7:Add test even without any parameters to just check(optional)
    >test 
    >you can see "hello from Lamda!"
Step8:Copy the code from lamda.py(this repo) and replace the code on the lamda function page
    >save
    >deploy



Step9:Goto EventBridge
Step10:Create a rule
    >name (any name)
    >rule type: Schedule
    >cron(0,*,?,*,*,*)
    >select target as the lamda function you created(ec2_tag_checker)
    >create the rule

Step11:Goto SES
Step12:Goto "Verified identities" and create an identity
    >select email address
    >type in email address
    >click on create identity

Step13:Goto the mail id inbox you will have a mail from aws click on the
       verification url 
Step14:Check on the SES -> "Verified identities" and check if the mail id
       added is in "Verified" status if so copy the mail-id

Step15:Goto your lamda function code
    >goto the #TODO
    >change Source='test@gmail.com' to Source=mail-id (mail-id copied from last step)
    >remove the todo line
    >deploy


Step16:check mail to confirm it work at the specified time when the rule is created 
        if an instance follows the parameters int he question 

***

##NOTE:
Here I assumed the ec2 instances are already created and the mail id of the 
"created by" person is either verified or the SES is in production mode.


