# Hướng dẫn chi tiết Server

Đoạn mã đã cung cấp tạo ra một lớp `Server` với các phương thức để xử lý các kết nối và truyền dữ liệu.

1. **Khởi tạo**
- Khi khởi tạo một đối tượng `Server`, bạn cần cung cấp địa chỉ IP (`host`) và cổng (`port`) của máy chủ bạn muốn thiết lập.

```python
    Server('192.168.1.12', 19100)
```
2. **Xử lý dữ liệu từ mỗi client**
- Phương thức `HandleClient` xử lý dữ liệu từ mỗi client. Nếu không nhận được dữ liệu hoặc xảy ra lỗi, kết nối sẽ được đóng.

```python
    HandleClient(client, address)
```
3. **Xử lý các kết nối**
- Phương thức `HandleConnections` xử lý các kết nối đến máy chủ.

```python
    HandleConnections()
```
4. **Lắng nghe**
- Phương thức `Listening` bắt đầu lắng nghe các kết nối đến máy chủ.

```python
    Listening()
```
**Lưu ý:** *Mã này chỉ nên được sử dụng cho mục đích học tập. Sử dụng nó để thực hiện các hoạt động phi pháp (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Luôn tuân thủ pháp luật khi sử dụng và phát triển mã nguồn mở.*