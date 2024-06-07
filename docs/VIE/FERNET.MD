## Fernet

### Khởi tạo (`__init__`):

- Phương thức `__init__` được sử dụng để khởi tạo một đối tượng Fernet với một khóa đã cho.
- Đầu vào `key` có thể là một chuỗi base64 hoặc một byte string.
- Nếu đầu vào là chuỗi base64, nó sẽ được giải mã và chuyển đổi thành byte string.
- Nếu chiều dài của `key` không phải là 32 bytes, nó sẽ ném một ValueError.
---
### Tạo Khóa (`generate_key`):

- Phương thức `generate_key` được sử dụng để tạo ra một khóa mới ngẫu nhiên với độ dài 32 bytes.
- Khóa được tạo ra sẽ được mã hóa dưới dạng base64 và trả về dưới dạng byte string.
---
### Mã Hóa (`encrypt`):

- Phương thức `encrypt` được sử dụng để mã hóa dữ liệu đầu vào thành một chuỗi mã hóa.
---
### Giải Mã (`decrypt`):

- Phương thức `decrypt` được sử dụng để giải mã một chuỗi mã hóa thành dữ liệu gốc.

