"""
Functions dealing with
"""

def send_text(msg):
    from twilio.rest import TwilioRestClient
    sid = 'ACfdfe250a7a88d95ee510cafd516831c3'
    token = 'a377f2daa60689f611366230492807c0'
    twilio_number = '+19162908690'
    to_number = "+19163978488"
    client = TwilioRestClient(sid, token)
    client.messages.create(to=to_number, from_=twilio_number,
                           body=msg)
