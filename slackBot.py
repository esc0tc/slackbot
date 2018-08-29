import boto3
import logging
import os
import urllib
import json
import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]

INFOTECH_URL = "https://slack.com/api/chat.postMessage"
INFO_URL = "https://slack.com/api/users.info"

ses = boto3.client('ses')
sns = boto3.client('sns')
lex = boto3.client('lex-runtime')

VERIFIED_EMAIL=""
verifiedEmail=[""]
phoneNumbers=[""]
ALERT_EMAILS = [verifiedEmail, ]

def handler(event, context):
    print('fulfillment event:')
    print(event)
    alert_type = event['currentIntent']['slots']['Type']
    alert_location = event['currentIntent']['slots']['Location']
    lex_user, channel_id, user_id = event['userId'].split(":")
    print(alert_type)

    current_time = datetime.datetime.now()
    timer_start = current_time + datetime.timedelta(0,300)
    print(timer_start)


    data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("user", user_id)
            )
        )
    data = data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(
        INFO_URL,
        data=data,
        method="POST"
    )
        # Add a header mentioning that the text is URL-encoded.
    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

        # Fire off the request!
    u1 = urllib.request.urlopen(request)
    u3 = json.loads(u1.read())
    u5 = u3['user']['profile']['email']
    u6 = u3['user']['profile']['real_name']
    u7 = '*Employee Emergency*\n - Name: ' + u6 + '\n - Email: ' + u5 + '\n - *Issue: ' + alert_type + '*\n - *Location: ' + alert_location + '*\n - *`You have 5 minutes to make contact.`*'
    u8 = '*Emergency Confirmation*\n - Name: ' + u6 + '\n - Email: ' + u5 + '\n - *Issue: ' + alert_type + '*\n - *Location: ' + alert_location + '*\n - *`If you don\'t see either Ashton or Harry soon, then please message them directly.` @harry_marcus @ashton_holland*'
    u9 = u3['user']['profile']['first_name']

    slope_data = data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", ""),
                ("text", u7)
            )
        )
    slope_data = slope_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def slopeImPost(data):
        slope_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
           "Content-Type",
           "application/json"
        )

        to_slope = urllib.request.urlopen(slope_request)
        to_slope.read()

    slopeImPost(slope_data)

    ridge_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", ""),
                ("text", u7)
            )
        )

    ridge_data = ridge_data.encode("ascii")

    # Construct the HTTP request that will be sent to the Slack API.
    def ridgeImPost(data):
        ridge_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_ridge = urllib.request.urlopen(ridge_request)
        to_ridge.read()

    ridgeImPost(ridge_data)

    peak_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", ""),
                ("text", u7)
            )
        )

    peak_data = peak_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def peakImPost(data):
        peak_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_peak = urllib.request.urlopen(peak_request)
        to_peak.read()

    peakImPost(peak_data)

    summit_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", ""),
                ("text", u7)
            )
        )

    summit_data = summit_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def summitImPost(data):
        summit_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_summmit = urllib.request.urlopen(summit_request)
        to_summit.read()

    summitImPost(summit_data)

    slackuser_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", user_id),
                ("text", u8)
            )
        )

    slackuser_data = slackuser_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def slackuserImPost(data):
        slackuser_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_slackuser = urllib.request.urlopen(slackuser_request)
        to_slackuser.read()

    slackuserImPost(slackuser_data)

    def send_email_alerts(to_addresses):
        for to_address in to_addresses:
            ses.send_email(
                Source=VERIFIED_EMAIL,
                Destination={
                    'ToAddresses': to_address
                },
                Message={
                    'Subject': {
                        'Data': 'EMERGENCY SLACK'
                    },
                    'Body': {
                        'Text': {
                       'Data': 'Employee Emergency\n - Name: ' + u6 + '\n - Email: ' + u5 + '\n - Issue: ' + alert_type + '*\n - Location: ' + alert_location + '\n ***You have 5 minutes to make contact***'
                        }
                    }
                }
            )
    def send_sms_alerts(numbers):
        for number in numbers:
            sns.publish(
                PhoneNumber=number,
                Message='EMERGENCY : \n ' + u6 + ' | ' + u5 + '\n -> ' + alert_type + '\n -> ' + alert_location
            )
    def send_alerts(level):
        if level.lower() in ['av-help-client-meeting', 'computer-will-not-turn-on', 'no-internet', 'no-email-access']:
            print('Running the ' + level + ' Alert runbook')
            if level.lower() == 'av-help-client-meeting':
                send_email_alerts(ALERT_EMAILS)
            elif level.lower() == 'computer-will-not-turn-on':
                send_email_alerts(ALERT_EMAILS)
            elif level.lower() == 'no-internet':
                send_email_alerts(ALERT_EMAILS)
            elif level.lower() == 'no-email-access':
                send_email_alerts(ALERT_EMAILS)

        else:
            print('I can\'t tell if you have an emergency or not.')

    userAddress = [u5]

    def send_alert_to_user(address):
            ses.send_email(
                Source=VERIFIED_EMAIL,
                Destination={
                    'ToAddresses': address
                },
                Message={
                    'Subject': {
                        'Data': 'IT-Emergency - Confirmation'
                    },
                    'Body': {
                        'Text': {
                       'Data': ''
                        }
                    }
                }
            )

    if alert_type in ['av-help-client-meeting', 'computer-will-not-turn-on', 'no-internet', 'no-email-access'];
        alert_response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Thanks"
                    ).format(alert_type)
                }
            }
        }
    else:
        alert_response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Sounds like this isn't an emergency. Goodbye."
                    ).format(alert_type)
                }
            }
        }
    send_sms_alerts([""])
    send_alerts(alert_type)
    send_alert_to_user(userAddress)
    return alert_response
