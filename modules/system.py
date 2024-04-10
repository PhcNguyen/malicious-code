from os import execv, system as _system, name as _os_name
from sys import executable, argv

class System:
    def __init__(self):
        self.Windows = _os_name == 'nt'

    def init(self):
        _system('')

    def clear(self):
        return _system("cls" if self.Windows else "clear")

    def title(self, title: str):
        if self.Windows:
            return _system(f"title {title}")

    def size(self, x: int, y: int):
        if self.Windows:
            return _system(f"mode {x}, {y}")
    
    def reset(self):
        execv(executable, [executable] + argv)   