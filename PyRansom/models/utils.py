import re
import os
import sys
import typing
import socket
import requests
import platform
import subprocess



class System:
    """
    4 functions: 
    - clear()   |   Clears the terminal screen
    - command() |   Executes a system command
    - reset()   |   Resets the Python script by re-executing it
    - exit()    |   Exits the Python script
    """

    Windows = os.name == 'nt'

    @staticmethod
    def clear() -> int:
        return os.system(
            "cls" if System.Windows else "clear"
        )
        
    @staticmethod
    def command(command: str) -> int:
        return os.system(command)

    @staticmethod
    def reset() -> typing.NoReturn:
        return os.execv(
            sys.executable, ['python'] + sys.argv
        )

    @staticmethod
    def exit() -> typing.NoReturn:
        sys.exit()



class InternetProtocol:
    IPIFY_URL = "https://api.ipify.org?format=json"  # Hằng số cho URL API
    
    @staticmethod
    def local() -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Kết nối đến máy chủ DNS công cộng
                ip_address = s.getsockname()[0]  # Lấy địa chỉ IP của máy tính
            return ip_address
        except socket.error:
            return 'N/A'

    @staticmethod
    def public() -> str:
        try:
            response = requests.get(InternetProtocol.IPIFY_URL)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            ip_data = response.json()
            return ip_data.get("ip")
        except (requests.RequestException, ValueError):
            return 'N/A'

    @staticmethod
    def ping() -> str:
        # Xác định lệnh ping dựa trên hệ điều hành
        host = "google.com"
        system_name = platform.system().lower()
        
        # Tùy chỉnh tham số lệnh ping theo hệ điều hành
        if system_name == "windows":
            param = "-n"
        elif system_name.startswith("linux") or system_name == "darwin":  # Unix-based (Linux và macOS)
            param = "-c"
        else:
            return 'Unsupported OS'
        
        try:
            # Thực hiện lệnh ping, gửi 1 gói tin
            output = subprocess.check_output(["ping", param, "1", host], universal_newlines=True)
            
            # Phân tích đầu ra để tìm thời gian ping
            if system_name == "windows":
                # Tìm thời gian từ "Reply from"
                match = re.search(r'time=(\d+)ms', output)
                if match:
                    return f'{match.group(1)}ms'
            else:
                # Tìm thời gian trong chuỗi kết quả cho Linux/macOS
                match = re.search(r'time[=<](\d+\.?\d*) ms', output)
                if match:
                    return f'{match.group(1)}ms'
            return 'N/A'
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 'N/A'