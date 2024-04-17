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
# Class GoogleSheet
from google.oauth2 import service_account as SACC # type: ignore
from googleapiclient.discovery import build

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


class GoogleAuthService:
    def __init__(self):
        self._create_service()

    def _create_service(self):
        try:
            credentials = SACC.Credentials.from_service_account_file(
                'scripts/credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            Console('127.0.0.1', e, 'Red')


class GoogleSheet:
    def __init__(self, service):
        self.id_sheet = '10rs_CfL4W5uKJI-ueX1n1MVZF4DT8uzqyb7wgtp0zfo'
        self.service = service
        self._values = None

    def AllValues(self, sheet='Sheet1'):
        if not self._values:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.id_sheet,
                range=sheet
            ).execute()
            self._values = result.get('values', [])
        return self._values

    def UpdateValues(self, values, sheet='Sheet1'):
        row = len(self.all_values(sheet)) + 1
        range_str = f'{sheet}!A{row}:F{row}'
        return self.update_values_in_range(values, range_str)
    

def Console(ip: str, msg: str, color: str) -> None:
    color_code = getattr(Col, color)
    message = f" [{Col.Green}{ip}{Col.White}] --> {color_code}{msg}{Col.White}."
    print(message)