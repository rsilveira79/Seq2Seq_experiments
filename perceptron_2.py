import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

SLACK_BOT_TOKEN='xoxb-131416520182-mI83M0XZPh4LNsER5SBLG1fo'
BOT_NAME = 'perceptronbot'
EXAMPLE_COMMAND = "do"
EXAMPLE_COMMAND2 = "please"
EXAMPLE_COMMAND3 = "what"


slack_client = SlackClient('xoxb-131416520182-mI83M0XZPh4LNsER5SBLG1fo')

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "EXPERIENCES !!! EXPERIENCES !!! EXPERIENCES !!! EXPERIENCES!!!"
    if command.startswith(EXAMPLE_COMMAND):
        response = "Do not forget to check dataset licenses !!!"
    if command.startswith(EXAMPLE_COMMAND2):
        response = "Laser in 1960 was fancy stuff..."
    if command.startswith(EXAMPLE_COMMAND3):
        response = "Send me DSKD papers pls..."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print(BOT_NAME + " connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
