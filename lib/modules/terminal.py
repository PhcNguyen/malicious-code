from os import execv, system as _system, name as _os_name
from sys import executable, argv, exit
from typing import Optional
from collections import deque


class Terminal:
    def __init__(self) -> None:
        self.Windows: bool = _os_name == 'nt'

    def Clear(self) -> None:
        return _system("cls" if self.Windows else "clear")

    def Title(self, title: str) -> None:
        if self.Windows:
            return _system(f"title {title}")

    def Size(self, x: int, y: int) -> None:
        if self.Windows:
            return _system(f"mode {x}, {y}")
    
    @staticmethod
    def Init() -> None:
        _system('')
        
    @staticmethod
    def Reset() -> None:
        execv(executable, [executable] + argv) 
    
    @staticmethod
    def Exit() -> None:
        exit()
    
    @staticmethod
    def Command(command: str) -> Optional[int]:
        return _system(command)
    
    @staticmethod
    def Console(ip: str, msg: str, color: str) -> None:
        print(f" [{Col.Green}{ip}{Col.White}] --> {getattr(Col, color)}{msg}{Col.White}")


class Col:
    @staticmethod
    def start(color: str) -> str:
        return f"\033[38;2;{color}m"
    
    Red: str = start('255;0;0')
    
    Blue: str = start('28;121;255')
    Cyan: str = start('0;255;255')
    Pink: str = start('255,192,203')

    Black: str = start('0;0;0')
    White: str = start('255;255;255')
    Green: str = start('0;255;0')

    Purple: str = start('255;0;255')
    Yellow: str = start('255;255;0')
    Orange: str = start('255;165;0')
