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
- Trước khi mã hóa, dữ liệu được chuyển đổi thành dạng bytes nếu nó là một chuỗi.
- Một salt mới được tạo ra và được kết hợp với dữ liệu trước khi mã hóa.
- Một HMAC được tính toán dựa trên dữ liệu đã mã hóa và salt.
- Cuối cùng, HMAC, salt và dữ liệu đã mã hóa được nối lại để tạo thành chuỗi mã hóa kết quả.
---
### Giải Mã (`decrypt`):

- Phương thức `decrypt` được sử dụng để giải mã một chuỗi mã hóa thành dữ liệu gốc.
- Trước tiên, chuỗi mã hóa được phân tách thành HMAC, salt và dữ liệu đã mã hóa.
- HMAC mới được tính toán dựa trên dữ liệu đã mã hóa và salt.
- Nếu HMAC tính toán khớp với HMAC trong chuỗi mã hóa, dữ liệu đã mã hóa được giải mã và trả về.
- Nếu HMAC không khớp, một AssertionError được ném, chỉ ra rằng dữ liệu đã bị sửa đổi hoặc làm giả.
