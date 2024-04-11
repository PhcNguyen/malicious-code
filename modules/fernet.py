from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
from hmac import HMAC
import os

class Fernet:
    def __init__(self, key) -> None:
        self.key = key
    
    def generate_key() -> bytes:
        return os.urandom(16)
    
print(Fernet.generate_key())