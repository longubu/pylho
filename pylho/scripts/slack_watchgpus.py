'''

'''
from slackclient import SlackClient
from pylho import personal_keys
import time
from subprocess import Popen, PIPE


butterbot_info = personal_keys.Long.butterbot
sc = SlackClient(**butterbot_info)

print('Starting')
try:
    if sc.rtm_connect():
        while True:
            events = sc.rtm_read()
            for event in events:
                if (('channel' in event) and ('text' in event) and (event.get('type') == 'message')):
                    channel = event['channel']
                    text = event['text']
                    thread_ts = event['ts']
                    if 'watchgpus' in text.lower():
                        proc = Popen(['nvidia-smi'], stdout=PIPE, stderr=PIPE)

                        while True:
                            retcode = proc.poll()
                            if retcode is not None:
                                stdout = proc.stdout.readlines()
                                stderr = proc.stderr.readlines()

                                # break while loop
                                break

                        msg = '```' + ''.join(stdout) + '```'
                        sc.api_call('chat.postMessage', channel=channel,
                                    text=msg, as_user='true:',
                                    thread_ts=thread_ts, reply_broadcast=False)
            time.sleep(5)
    else:
        print('Connection failed, invalid token?')
except Exception, e:
    butterbot_info = personal_keys.Long.butterbot
    sc = SlackClient(**butterbot_info)
    sc.api_call('chat.postMessage', channel='#vpicu-gpu', text='slack_watchgpus stopped running: %s' % e)

print('Done')
