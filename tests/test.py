from lib.cryptography.fernet import Fernet


key = Fernet.generate_key()
print(key)

bot = Fernet(key)

enc = bot.encrypt('bay gio test xem ma hoa thanh cong khong')
print(enc)

dec = bot.decrypt(enc)
print(dec)