===============================
Server Class Usage Guide
===============================

The provided code creates a `Server` class with methods for handling connections and data transmission.

1. **Initialization**: When initializing a `Server` object, you need to provide the IP address (`host`) and port (`port`) of the server you want to set up.

.. code-block:: python

    Server('192.168.1.12', 19100)

2. **Handling Client Data**: The `HandleClient` method processes data from each client. If no data is received or an error occurs, the connection is closed.

.. code-block:: python

    HandleClient(client, address)

3. **Handling Connections**: The `HandleConnections` method handles incoming connections to the server.

.. code-block:: python

    HandleConnections()

4. **Listening**: The `Listening` method starts listening for incoming connections to the server.

.. code-block:: python

    Listening()

Please note: This code should only be used for learning purposes. Using it to perform illegal activities (such as cyber attacks) can lead to serious legal consequences. Always comply with legal regulations when using and developing open source code.
