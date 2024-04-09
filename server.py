#!user/bin/env python3
# Import modules
import os
from time import sleep, time
from threading import Thread
from modules import System, Col
from socket import socket, AF_INET, SOCK_STREAM

# Lớp Server để xử lý các kết nối và truyền dữ liệu
class Server:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.server = socket(AF_INET, SOCK_STREAM)
        self.client_connect_time = {}  # Lưu thời gian kết nối của mỗi client

    # Xử lý dữ liệu từ mỗi client
    def HandleClient(self, client, address):
        connect_time = time()  # Thời điểm bắt đầu kết nối
        self.client_connect_time[address[0]] = connect_time
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break
                if not isinstance(data, bytes): 
                    data = data.encode('utf-8')
                Console(address[0], data, 1)
            except Exception as error:
                Console(address[0], error, 3)
                break
        client.close()
        disconnect_time = time()  # Thời điểm ngắt kết nối
        self.calculate_connection_time(address[0], connect_time, disconnect_time)

    # Xử lý các kết nối đến server
    def HandleConnections(self):
        while True:
            client, address = self.server.accept()
            Console(address[0], None, 0)
            thread = Thread(target=self.HandleClient, args=(client, address))
            thread.start()

    # Tính toán thời gian kết nối của mỗi client
    def calculate_connection_time(self, ip, connect_time, disconnect_time):
        if ip in self.client_connect_time:
            connection_time = disconnect_time - connect_time
            Console(ip, f'Disconnect.  {connection_time:.2f} seconds', 2)
            del self.client_connect_time[ip]

    # Bắt đầu lắng nghe các kết nối đến server
    def Listening(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            Console('SYSTEM', 'The server starts listening', 2)
            thread = Thread(target=self.HandleConnections)
            thread.start()
        except OSError as error:
            Console(None, 'Address already in use', 3)

# Lớp SqliteLog để lưu trữ các hoạt động và lỗi vào cơ sở dữ liệu SQLite
class SqliteLog:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    # Kết nối đến cơ sở dữ liệu
    def connect(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.conn = sqlite3.connect(f'data/server.db')
        self.cursor = self.conn.cursor()

    # Đóng kết nối đến cơ sở dữ liệu
    def close(self):
        if self.conn:
            self.conn.close()

    # Tạo bảng trong cơ sở dữ liệu
    def create_table(self, table_name):
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
            self.create_table(f'IP_{IP}')
            timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute(f'''
                INSERT INTO IP_{IP} (activity, timestamp) VALUES (?, ?)
            ''', (activity, timestamp))
            self.conn.commit()
        except Exception as e:
           Console('error', str(e), 3)
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
        except Exception as e:
            Console('error', str(e), 3)
        finally:
            self.close()

    # Đóng kết nối đến cơ sở dữ liệu
    def close(self) -> None:
        if self.conn:
            self.conn.close()

# Hàm Console để in thông điệp ra console và ghi hoạt động và lỗi vào cơ sở dữ liệu
def Console(ip: str, msg, select: int=0,) -> None:
    log = SqliteLog()
    if select == 1 and msg is not None:
        log.activity(ip, msg)
        msg = round(len(msg)/1024, 3)
    elif select == 3 :
        log.error(msg)
    messages = {
        0: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Green}Connect to the Server{Col.White}.",
        1: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Yellow}Packet data: {msg} KB{Col.White}.",
        2: f" [{Col.Pink}{ip}{Col.White}] --> {Col.Purple}{msg}{Col.White}.",
        3: f" [{Col.Pink}ERROR{Col.White}] --> {Col.Red}{msg}{Col.White}."
    }
    print(messages.get(select, f" [{Col.Pink}{ip}{Col.White}] --> Unknown message: {msg}"))

# Hàm main để khởi tạo server và bắt đầu lắng nghe các kết nối
if __name__ == '__main__':
    try:
        System().clear()
        Server().Listening()
    except Exception as error:
        Console(None, error, 3)
        sleep(10)
        os.execv(sys.executable, [sys.executable] + sys.argv)

