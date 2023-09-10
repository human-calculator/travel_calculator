import requests

from calculator.settings import SLACK_WEBHOOK


def send_slack(message: str):
    headers = {"Content-type": "application/json"}
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    requests.post(SLACK_WEBHOOK, headers=headers, json=payload)