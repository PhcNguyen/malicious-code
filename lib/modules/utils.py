import os.path
from .terminal import Terminal
from .yml import safe_load
from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM
)

def setting(bibliography: str, name: str) -> list:
    Terminal.Init()
    filename = f'{bibliography}/{name}.yml'

    if not os.path.exists(bibliography):
        os.mkdir(bibliography)

    if not os.path.exists(filename):
        with socket(AF_INET, SOCK_DGRAM) as server:
            server.connect(("8.8.8.8", 80))
            localhost = server.getsockname()[0]

        while True:
            port = Terminal.Input(
                'Port', 'Yellow'
            )
            if port.isdigit() and 1 <= int(port) <= 65535:
                break
            else:
                Terminal.Console(
                    "Error",
                    "Invalid PORT.",
                    "Red"
                )

        with open(filename, 'w') as file:
            file.write(
                f"server:\n  - {localhost}\n  - {port}\n"
            )

    else:
        with open(filename, 'r') as file:
            data: dict = safe_load(file)['server']

        localhost = data[0]
        port = data[1]

    return [localhost, port]