# Hướng dẫn chi tiết System

Đoạn mã Python này bao gồm một số lớp và hàm cho các hoạt động hệ thống, xử lý màu sắc, gửi email, ghi log SQLite, và in thông báo lên console.

1. **Lớp System**
- Lớp này chứa các phương thức để tương tác với hệ thống. Nó bao gồm các phương thức để xóa console, đặt kích thước console, khởi động lại chương trình, và thực thi các lệnh hệ thống.

2. **Lớp Colors**
- Lớp này chứa các phương thức tĩnh để xử lý mã màu ANSI. Nó bao gồm các phương thức để tạo mã màu ANSI, loại bỏ mã màu ANSI, bắt đầu một chuỗi màu, lấy số khoảng trắng đầu tiên trong một chuỗi, và pha trộn màu.

3. **Lớp Color**
- Lớp này chứa một phương thức tĩnh để pha trộn màu.

4. **Lớp Col**
- Lớp này chứa các mã màu ANSI đã được định nghĩa trước để sử dụng dễ dàng.

5. **Lớp EmailSender**
- Lớp này được sử dụng để gửi email sử dụng một tài khoản Gmail. Nó bao gồm một phương thức để gửi email.

6. **Hàm Console**
- Hàm này được sử dụng để in các thông báo màu lên console.

Dưới đây là một ví dụ về cách sử dụng các lớp và hàm này:

```python

    # Khởi tạo hệ thống
    system = System()
    system.Init()

    # Xóa console
    system.Clear()

    # Đặt kích thước console
    system.Size(80, 24)

    # In một thông báo lên console
    Console("127.0.0.1", "Hello, World!", "Green")

    # Gửi một email
    email_sender = EmailSender("your_email@gmail.com", "your_password")
    email_sender.SendEmail("Hello, World!", "receiver_email@gmail.com")
```

**Lưu ý:** *Mã này chỉ nên được sử dụng cho mục đích học tập. Sử dụng nó để thực hiện các hoạt động phi pháp (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Luôn tuân thủ pháp luật khi sử dụng và phát triển mã nguồn mở.*