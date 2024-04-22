#!/usr/bin/env python3
import os
import base64
import binascii
from typing import Union
from hmac import new as new_hmac, compare_digest
from lib.cryptography.cipher import (
    SALT_SIZE, HMAC_SIZE, 
    get_key_iv, AESCipher)


class Fernet:
    def __init__(self, key: Union[bytes, str]) -> None:
        self.key = key
        try:
            key = base64.urlsafe_b64decode(key)
        except binascii.Error as exc:
            raise ValueError(
                "Fernet key must be 32 url-safe base64-encoded bytes."
            ) from exc
        if len(key) != 32:
            raise ValueError(
                "Fernet key must be 32 url-safe base64-encoded bytes."
            )
    
    @classmethod
    def generate_key(cls) -> bytes:
        return base64.urlsafe_b64encode(os.urandom(32))
    
    def encrypt(self, plaintext: Union[bytes, str]) -> str:
        if isinstance(self.key, str):
            self.key = self.key.encode('utf-8')
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        salt = os.urandom(SALT_SIZE)
        key, hmac_key, iv = get_key_iv(self.key, salt)
        ciphertext = AESCipher(key).encrypt_cbc(plaintext, iv)
        hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
        assert len(hmac) == HMAC_SIZE
        
        return hmac + salt + ciphertext
    
    def decrypt(self, ciphertext: Union[bytes, str]) -> str:
        if isinstance(self.key, str):
            self.key = self.key.encode('utf-8')

        hmac, ciphertext = ciphertext[:HMAC_SIZE], ciphertext[HMAC_SIZE:]
        salt, ciphertext = ciphertext[:SALT_SIZE], ciphertext[SALT_SIZE:]
        key, hmac_key, iv = get_key_iv(self.key, salt)

        expected_hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
        assert compare_digest(hmac, expected_hmac), 'Ciphertext corrupted or tampered.'

        return AESCipher(key).decrypt_cbc(ciphertext, iv).decode()