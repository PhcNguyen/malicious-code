from requests.exceptions import RequestException
from typing import Union

import requests
import time


SENDMESSAGE = "https://api.telegram.org/bot{}/sendMessage"
GETUPDATE = "https://api.telegram.org/bot{}/getUpdate"


def handle():
    pass


class Telegram:
    def __init__(self, token: str) -> None:
        self.token = token
        self.offset = None
        self.handlers = []

    def sendMessage(
        self, 
        chat_id: str, 
        text: str
    ) -> Union[dict, None]:
        
        url = SENDMESSAGE.format(self.token)
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        try:
            response = requests.post(
                url=SENDMESSAGE.format(self.token), 
                data=payload
            )
            response.raise_for_status()
        except RequestException as e:
            print(f"Error sending message: {e}")
            return None
        return response.json()

    def getUpdates(self) -> Union[dict, None]:
        payload = {
            'timeout': 10,
            'offset': self.offset
        }
        try:
            response = requests.get(
                url=GETUPDATE.format(self.token), 
                params=payload
            )
            response.raise_for_status()
        except RequestException as e:
            print(f"Error getting updates: {e}")
            return None
        return response.json()

    def Updates(self, updates: dict):
        for update in updates.get("result", []):
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                for handler in self.handlers:
                    response_text = handler(chat_id, text)
                    if response_text:
                        self.sendMessage(chat_id, response_text)

    def Poll(self):
        while True:
            updates = self.getUpdates()
            if updates and updates.get("ok"):
                if updates["result"]:
                    self.Updates(updates)
                    self.offset = updates["result"][-1]["update_id"] + 1
            time.sleep(1)
