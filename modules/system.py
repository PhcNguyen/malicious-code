# Class System
from os import execv, system as _system, name as _os_name
from psutil import  net_if_addrs, AF_LINK
from sys import executable, argv
# Class Colors, Color
from collections import deque
# Class EmailSender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# Class Sqlite
import os.path
import sqlite3
from datetime import datetime


class System:
    def __init__(self) -> None:
        self.Windows = _os_name == 'nt'
 
    def Init(self) -> None:
        _system('')

    def Clear(self) -> None:
        return _system("cls" if self.Windows else "clear")

    def Title(self, title: str):
        if self.Windows:
            return _system(f"title {title}")

    def Size(self, x: int, y: int) -> None:
        if self.Windows:
            return _system(f"mode {x}, {y}")
    
    def Reset(self) -> None:
        execv(executable, [executable] + argv) 
    
    def Mac(self) -> str:
        try:
            address_mac = [
                address.address 
                for addresses in net_if_addrs().values() 
                for address in addresses 
                if address.family == AF_LINK
            ]
            return '|'.join(address_mac) if address_mac else 'nm'  
        except:
            return 'nm'
    
    def Command(command: str):
        return _system(command)


class Colors:
    @staticmethod
    def make_ansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"
    
    @staticmethod
    def remove_ansi(col: str) -> str:
        return col.replace('\033[38;2;', '').replace('m','').replace('50m', '').replace('\x1b[38', '')
    
    @staticmethod
    def start(color: str) -> str:
        return f"\033[38;2;{color}m"
    
    @staticmethod
    def get_spaces(text: str) -> int:
        return len(text) - len(text.lstrip())
    
    @staticmethod
    def mix_colors(col1: str, col2: str) -> list:
        col1, col2 = Colors.remove_ansi(col=col1), Colors.remove_ansi(col=col2)
        return deque([col1, col2]) if col1 == col2 else deque([col1, Colors.static_mix([col1, col2], _start=False), col2])


class Color:
    @staticmethod
    def static_mix(colors: list, _start: bool = True) -> str:
        rgb = [list(map(int, Colors.remove_ansi(col).split(';'))) for col in colors]
        average_rgb = [round(sum(color[i] for color in rgb) / len(rgb)) for i in range(3)]
        rgb_string = ';'.join(map(str, average_rgb))
        return Colors.start(rgb_string) if _start else rgb_string 


class Col:
    Red = Colors.start('255;0;0')
    
    Blue = Colors.start('28;121;255')
    Cyan = Colors.start('0;255;255')
    Pink = Colors.start('255,192,203')

    Black = Colors.start('0;0;0')
    White = Colors.start('255;255;255')
    Green = Colors.start('0;255;0')

    Purple = Colors.start('255;0;255')
    Yellow = Colors.start('255;255;0')
    Orange = Colors.start('255;165;0')


class EmailSender:
    def __init__(self, email: str, password: str) -> None:
        self.sender_email = email
        self.password = password

    def SendEmail(self, message, receiver_email) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = 'KEY'
            msg.attach(MIMEText(message, 'plain'))
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
            return True
        except:
            return False


class SqliteLog:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    def _connect(self) -> None:
        if not os.path.exists('data'):
            os.makedirs('data')
        self.conn = sqlite3.connect('data/server.db')
        self.cursor = self.conn.cursor()

    def _create_table(self, table_name: str) -> None:
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                activity TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def _close(self) -> None:
        if self.conn:
            self.conn.close()

    def activity(self, ip: str, activity: str) -> str:
        try:
            self._connect()
            ip = ip.replace('.', '_')
            self._create_table(f'IP_{ip}')
            timestamp = datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute(f'''
                INSERT INTO IP_{ip} (activity, timestamp) VALUES (?, ?)
            ''', (activity, timestamp))
            self.conn.commit()
        except Exception as error:
            Console(ip, error, 'Red')
        finally:
            self._close()


def Console(ip: str, msg: str, color: str) -> None:

    color_code = getattr(Col, color)

    message = f" [{Col.Green}{ip}{Col.White}] --> {color_code}{msg}{Col.White}."

    print(message)