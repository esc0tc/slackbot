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

VERIFIED_EMAIL="smbadmin@mcgarrybowen.com"
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

    ashton_data = data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", "U7N0U0G49"),
                ("text", u7)
            )
        )
    ashton_data = ashton_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def ashtonImPost(data):
        ashton_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
           "Content-Type",
           "application/json"
        )

        to_ashton = urllib.request.urlopen(ashton_request)
        to_ashton.read()

    ashtonImPost(ashton_data)

    eric_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", "U114C6QC9"),
                ("text", u7)
            )
        )

    eric_data = eric_data.encode("ascii")

    # Construct the HTTP request that will be sent to the Slack API.
    def ericImPost(data):
        eric_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_eric = urllib.request.urlopen(eric_request)
        to_eric.read()

    ericImPost(eric_data)

    harry_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", "U1GDDG3C6"),
                ("text", u7)
            )
        )

    harry_data = harry_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def harryImPost(data):
        harry_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_harry = urllib.request.urlopen(harry_request)
        to_harry.read()

    harryImPost(harry_data)

    james_data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", "U0Z9BP1FH"),
                ("text", u7)
            )
        )

    james_data = james_data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
    def jamesImPost(data):
        james_request = urllib.request.Request(
            INFOTECH_URL,
            data=data,
            method="POST"
        )
        request.add_header(
            "Content-Type",
            "application/json"
        )
        to_james = urllib.request.urlopen(james_request)
        to_james.read()

    jamesImPost(james_data)

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
                       'Data': 'Ashton and Harry have been notified of your emergency. If you don\'t see either Ashton or Harry soon, then please message them directly in Slack. @harry_marcus @ashton_holland\n\nEmergency Confirmation\n - Name: ' + u6 + '\n - Email: ' + u5 + '\n - Issue: ' + alert_type + '\n - Location: ' + alert_location
                        }
                    }
                }
            )

    if alert_type in ['av-help-client-meeting', 'computer-will-not-turn-on', 'no-internet', 'no-email-access']:
        alert_response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Thanks, " + u9 + "!\nEither Ashton or Harry will be messaging you any minute.\n>Ashton and Harry have both been notified of your emergency via text, email, _and_ Slack. If you do not hear from either of them in the next 5 minutes then please message them directly. *@harry_marcus* *@ashton_holland*.\n*`If you have another emergency, please begin again.`* *Otherwise, please take a moment to submit the details of your emergency while you wait: https://dan.service-now.com*"
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
                        "Sounds like this isn't an emergency. Please visit 'https://dan.service-now.com'. Goodbye."
                    ).format(alert_type)
                }
            }
        }
    send_sms_alerts(["+12088903874", "+18182649284", "+19253059357"])
    send_alerts(alert_type)
    send_alert_to_user(userAddress)
    return alert_response
