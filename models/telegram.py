from requests.exceptions import RequestException
from typing import Union

import requests


SENDMESSAGE = "https://api.telegram.org/bot{}/sendMessage"
SENDDOCUMENT = "https://api.telegram.org/bot{}/sendDocument"


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
                url=url, 
                data=payload
            )
            response.raise_for_status()
        except RequestException as e:
            print(f"Error sending message: {e}")
            return None
        return response.json()
    
    def sendDocument(
        self, 
        chat_id: str,
        dir_file: str
    ) -> None:
        try:
            url = SENDDOCUMENT.format(self.token)

            with open(file, 'rb') as file:
                files = {
                    'document': file
                }
                payload = {
                    'chat_id': chat_id
                }
                response = requests.post(
                    url=url,
                    files=files,
                    data=payload
                )
                response.raise_for_status()
        except: pass

