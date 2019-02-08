#!/usr/bin/python3
#Author: Prashant Pokhriyal
#A BOTO3 wrapper script for managing the iam groups.

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

#Clear the screen
os.system('clear')

#Terminal Color Variables
red='\033[31m'
green='\033[32m'
blue='\033[34m'
orange='\033[33m'
end='\033[0m'


#Function to list the IAM Groups
def list_iam_groups():

    try:

        client = boto3.client('iam')
        response = client.list_groups()
        print(response)

    except NoCredentialsError:
        print("""{}Error{}: Please Configure your AWS Authentication Credentials.
       Use '--aws-auth aws_access_key_id aws_secrect_access_key region'""".format(red,end))

    except ClientError as error:

        if error.response['Error']['Code'] == 'InvalidClientTokenId':
            print("""{}Error{}: Invalid AWS Authentication Credentials.
       Use '--aws-auth aws_access_key_id aws_secrect_access_key region' """.format(red,end))


#Function to create the AWS Authentication Credentials
        

list_iam_groups()
    
