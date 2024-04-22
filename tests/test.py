import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.cryptography.fernet import Fernet


key = Fernet.generate_key()
print(key)

bot = Fernet(key)

enc = bot.encrypt('bay gio test xem ma hoa thanh cong khong')
print(enc)

dec = bot.decrypt(enc)
print(dec)