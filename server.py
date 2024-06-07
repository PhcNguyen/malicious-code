import time
import socket
from threading import Thread
from modules.core import Terminal, SheetApis, System

# ID of the Google Sheet
idsheet: str = '10rs_CfL4W5uKJI-ueX1n1MVZF4DT8uzqyb7wgtp0zfo'

class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = int(port)
        self.server = socket.socket()
        self.data_queue = []
        self.apis = SheetApis(idsheet)

    def handle_sheet(self) -> None:
        """Process the data queue and update the Google Sheet."""
        while True:
            try:
                if self.data_queue:
                    address, data = self.data_queue.pop(0)
                    if isinstance(data, bytes): 
                        data = data.decode()
                    self.apis.update_values([data.split('|')])  
                    Terminal.Console(self.host, 'Yellow', f"Processed data from {address}")
                else:
                    time.sleep(5)
            except Exception as error:
                Terminal.Console('SHEETS', 'Red', error)

    def handle_client(self, client: socket.socket, address) -> None:
        """Handle incoming data from a client."""
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
                    'Yellow', 
                    f'Packet data: {round(len(data)/1024, 3)} KB'
                )
            except Exception as error:
                Terminal.Console(address[0], 'Red', error)
                break
        client.close()
        Terminal.Console(address[0], 'Blue', 'Disconnected')

    def handle_connections(self) -> None:
        """Accept and handle incoming client connections."""
        while True:
            client, address = self.server.accept()
            Terminal.Console(address[0], 'Orange', 'Connected to Server')
            thread = Thread(target=self.handle_client, args=(client, address))
            thread.start()

    def listening(self) -> None:
        """Start the server and listen for incoming connections."""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            Terminal.Console(f'{self.host}:{self.port}', 'Green', 'Server starts listening')
            connection_thread = Thread(target=self.handle_connections)
            connection_thread.start()
            sheet_thread = Thread(target=self.handle_sheet)
            sheet_thread.start()
        except socket.error:
            Terminal.Console(self.host, 'Red', 'Address already in use')
        except Exception as error:
            Terminal.Console(self.host, 'Red', error)

if __name__ == '__main__':
    server = Server(System.local_ip(), 12345)
    server.listening()
