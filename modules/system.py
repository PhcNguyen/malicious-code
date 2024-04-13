from os import execv, system as _system, name as _os_name
from sys import executable, argv
from psutil import  net_if_addrs, AF_LINK

class System:
    def __init__(self) -> None:
        self.Windows = _os_name == 'nt'
 
    def init(self) -> None:
        _system('')

    def clear(self) -> None:
        return _system("cls" if self.Windows else "clear")

    def title(self, title: str):
        if self.Windows:
            return _system(f"title {title}")

    def size(self, x: int, y: int) -> None:
        if self.Windows:
            return _system(f"mode {x}, {y}")
    
    def reset(self) -> None:
        execv(executable, [executable] + argv) 
    
    def mac(self) -> str:
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
