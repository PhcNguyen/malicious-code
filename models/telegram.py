import requests



class Telegram:
    SENDMESSAGE = "https://api.telegram.org/bot{}/sendMessage"
    SENDDOCUMENT = "https://api.telegram.org/bot{}/sendDocument"

    def __init__(self, token: str) -> None:
        self.token = token

    def sendMessage(
        self, 
        chat_id: str, 
        text: str
    ) -> bool:
        
        url = Telegram.SENDMESSAGE.format(self.token)
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
            return True
        except :return False
    
    def sendDocument(
        self, 
        chat_id: str,
        dir_file: str
    ) -> bool:
        try:
            url = Telegram.SENDDOCUMENT.format(self.token)

            with open(dir_file, 'rb') as file:
                files = {'document': file}
                payload = {'chat_id': chat_id}
                response = requests.post(
                    url=url,
                    files=files,
                    data=payload
                )
                response.raise_for_status()
                return True
        except: return False