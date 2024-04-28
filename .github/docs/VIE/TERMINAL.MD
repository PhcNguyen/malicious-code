## Terminal - Col

Đoạn mã Python này bao gồm một số lớp và hàm cho các hoạt động hệ thống, xử lý màu sắc, in thông báo lên console.

1. **Class Terminal**
- Lớp này chứa các phương thức để tương tác với hệ thống. Nó bao gồm các phương thức để xóa console, đặt kích thước console, khởi động lại chương trình, và thực thi các lệnh hệ thống.

2. **Class Col**
- Phương thức để tạo mã màu ANSI
- Chứa các mã màu ANSI đã được định nghĩa trước để sử dụng dễ dàng.

```python
    # Khởi tạo hệ thống
    from lib.modules import Terminal, Col

    Terminal.Init()

    # Xóa console
    Terminal.Clear()

    # Đặt kích thước console
    Terminal().Size(80, 24)

    # In một thông báo lên console
    Terminal.Console("127.0.0.1", "Hello, World!", "Green")

    # Color black (RGB)
    Black = Col.start('0;0;0')
    
    # Class Col
    print(f"{Col.Red} I AM IS RED {Col.White}")
```