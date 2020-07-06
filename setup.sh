#!/bin/sh
aws_region=`grep region: serverless.yml |awk -F': ' '{ print $2 }'`
ssm_param_name=`grep SsmParamName: serverless.yml |awk -F': ' '{ print $2 }'`
pip3 install python-twitter --target=.
secret_value=`cat twitter.json |base64 -w0`
aws ssm put-parameter --type SecureString --name $ssm_param_name --value $secret_value --region $aws_region
