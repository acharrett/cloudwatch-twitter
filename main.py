import base64
import json
from os import environ
import boto3
import twitter

def handler(event={}, context={}):
    ssm_param_name = 'twitter'
    alert_people = environ['TWITTER_USERS'].split(',')
    alerts = []

    for record in event['Records']:
        alert_message = record['Sns']['Subject']
        alerts.append(alert_message)

    twitter_api = twitter_connect(ssm_param_name)

    for alert_message in alerts:
        send_alert(alert_message, twitter_api, alert_people)

def twitter_connect(ssm_param_name):
    client = boto3.client('ssm')

    response = client.get_parameter(
        Name=ssm_param_name,
        WithDecryption=True
    )

    twitter_creds = json.loads(base64.b64decode(response['Parameter']['Value']))

    twitter_api = twitter.Api(consumer_key=twitter_creds['consumer_key'],
                              consumer_secret=twitter_creds['consumer_secret'],
                              access_token_key=twitter_creds['access_token'],
                              access_token_secret=twitter_creds['access_token_secret'])

    return twitter_api

def send_alert(alert, twitter_api, alert_people):
    for twitter_user in alert_people:
        print(str(twitter_user) + " " + alert)
        twitter_api.PostDirectMessage(alert, screen_name=twitter_user)
