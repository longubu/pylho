'''
Functions to send alerts via online/mobile messaging
'''

def send_text(msg, sid, token, to_number, twilio_number):
    '''Sends text message to any number using valid twilio credentials. Note,
    sending to ANY `to_number` requires a premium twilio account.

    # Arguments
    msg: [str] Message to send

    sid: [str] twilio sid

    token: [str] twilio token

    to_number: [str] number to send msg to

    twilio_number [str] associated phone number of account
    '''
    from twilio.rest import Client
    client = Client(sid, token)
    client.messages.create(to=to_number, from_=twilio_number, body=msg)


def send_text_to_long(msg):
    '''Sends text message to me. Dont use this'''
    from personal_keys import Long
    # get personal key
    twilio_info = Long.twilio
    send_text(msg, **twilio_info)


def send_slack(msg, token=None, channel='#vpicu-gpu'):
    '''Sends message to vpicu.vpicu-gpu channel as ButterBot

    # Arguments
    msg: [str] Message to send

    token: [str] Token of vpicu slackbot to use. If None, will default to
        ButterBot

    channel: [str] channel to post in vpicu slack.
    '''
    from slackclient import SlackClient
    if token is None:
        from personal_keys import Long
        butterbot_info = Long.butterbot

    sc = SlackClient(**butterbot_info)
    sc.api_call("chat.postMessage", channel=channel, text=msg)
