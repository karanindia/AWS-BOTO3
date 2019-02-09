#!/usr/bin/python3
#Author: Prashant Pokhriyal
#A BOTO3 wrapper script for managing the iam groups.

import os
import pathlib
import getpass
import sys
import csv
from sys import argv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError

#Clear the screen
#os.system('clear')

#Terminal Color Variables
red='\033[31m'
green='\033[32m'
blue='\033[34m'
orange='\033[33m'
end='\033[0m'


#Function to list out all the arguments
def HELP():

    print("Description: A BOTO3 wrapper script for managing the IAM Groups.")
    print("")
    print("--help\t\t\tList all the available arguments")
    print("--list-iam-groups\tList all the available IAM Groups")
    print("--aws-auth\t\tCreate AWS Authentication Credentials")


#Function to list the IAM Groups
def list_iam_groups():

    try:

        client = boto3.client('iam')
        response = client.list_groups()
        
        #Check the Lenght of the List
        if len(response['Groups']) == 0:

            print("[ {}Error{} ] IAM Group List is Empty. Use '--create-groups' option.".format(red,end))
        else:

            #Creating the csv file for GroupName,GroupID,ARN
            with open('/tmp/iam-group-list.csv',mode='w') as csvfile:

                filewriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
                filewriter.writerow(['Group Name','Group ID','ARN'])
            
                #Loop through the list of groups
                for i in response['Groups']:
                    filewriter.writerow([i.get('GroupName'),i.get('GroupId'),i.get('Arn')])

            csvfile.close()
            print("[{}OK{} ] Group List created Successfully : /tmp/iam-group-list.csv".format(green,end))

    except NoCredentialsError:
        print("""[ {}Error{} ] Please Configure your AWS Authentication Credentials.
       Use '--aws-auth' option""".format(red,end))

    except PartialCredentialsError:
        print("""[ {}Error{} ]: Invalid AWS Authentication Credentials.
       Use '--aws-auth' option """.format(red,end))

    except EndpointConnectionError:
        print("[ {}Error{} ] Please Check your Network Connectivity.".format(red,end))
    except ClientError as error:

        if error.response['Error']['Code'] == 'InvalidClientTokenId':
            print("""[ {}Error{} ] Invalid AWS Authentication Credentials.
       Use '--aws-auth' option """.format(red,end))


#Function to create the AWS Authentication Credentials
def aws_auth_credentials(accesskeyid,secrectkey,region):


            #Create the aws user environment directory
            aws_user = getpass.getuser()

            if aws_user != "root":
                pathlib.Path('/home/'+aws_user+'/.aws').mkdir(parents=True,exist_ok=True)

                #Create the AWS Credential and Config file
                f = open('/home/'+aws_user+'/.aws/credentials',"w+")
                f.write("[default]\naws_access_key_id = "+accesskeyid+"\naws_secret_access_key = "+secrectkey)
                f.close()            
                
                f = open('/home/'+aws_user+'/.aws/config',"w+")
                f.write("[default]\nregion="+region)
                f.close()
                
                print("\n[ {}OK{} ] AWS Authentication Credentials created successfully.".format(green,end))
                
            else:
                pathlib.Path('/'+aws_user+'/.aws').mkdir(parents=True,exist_ok=True)

                #Create the AWS Credential and Config file
                f = open('/'+aws_user+'/.aws/credentials',"w+")
                f.write("[default]\naws_access_key_id = "+accesskeyid+"\naws_secret_access_key = "+secrectkey)
                f.close()            
                
                f = open('/'+aws_user+'/.aws/config',"w+")
                f.write("[default]\nregion="+region)
                f.close()

                print("\n[ {}OK{} ] AWS Authentication Credentials created successfully.".format(green,end))

if __name__ == '__main__':

    #Check if argument is passed or not
    if len(sys.argv) < 2:

        print("[ {}Error{} ] Two few arguments.Please use --help option.".format(red,end))
    else:

        if sys.argv[1] == "--help":

            HELP()

        elif sys.argv[1] == "--aws-auth":

            print(" ")
            print("[ {}AWS Authentication Credentials{} ]".format(orange,end))
            print("==================================")

            user_input1 = input("Enter the AWS AccessKeyID : ")
            user_input2 = input("Enter the AWS SecrectKey  : ")
            user_input3 = input("AWS Region                : ")
            aws_auth_credentials(user_input1,user_input2,user_input3)

        elif sys.argv[1] == "--list-iam-groups":

            list_iam_groups()

        else:

            print("[ {}Error{} ] Invalid Argument '{}'.Please use --help option.".format(red,end,sys.argv[1]))
