# Hướng dẫn chi tiết Encdec

Mã Python này bao gồm một số hàm để xử lý tệp.

 1. **Khởi tạo Fernet**

    ```python
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    ```

- Trước khi gọi các hàm `Encrypt` hoặc `Decrypt`, bạn cần khởi tạo một đối tượng `Fernet` với một khóa bí mật. `Fernet` là một hệ thống mã hóa đối xứng an toàn được cung cấp bởi thư viện `cryptography`.

 2. **Mã hóa Tệp**

    ```python
    Encrypt(cipher_suite)
    ```

- Hàm `Encrypt` sẽ mã hóa tất cả các tệp được liệt kê bởi hàm `List_Files`. Mỗi tệp sẽ được đọc và mã hóa thành `chunks`, sau đó được ghi vào một tệp tạm thời. Cuối cùng, tệp tạm thời sẽ thay thế tệp gốc.

 3. **Giải mã Tệp**

    ```python
    Decrypt(cipher_suite)
    ```

- Hàm `Decrypt` sẽ giải mã tất cả các tệp đã được mã hóa bởi hàm `Encrypt`, tương tự như quá trình mã hóa nhưng ngược lại.

 4. **Liệt kê Tệp**

    ```python
    files = List_Files()
    ```

- Hàm `List_Files` sẽ trả về một danh sách các tệp dựa trên các phần mở rộng tệp được xác định trong tệp `scripts/extensions.yaml`. Hàm này sử dụng `Path.home().rglob('*')` để liệt kê tất cả các tệp trong thư mục chính của người dùng.

**Lưu ý:** *Mã này chỉ nên được sử dụng cho mục đích học tập. Sử dụng nó để thực hiện các hoạt động phi pháp (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Luôn tuân thủ pháp luật khi sử dụng và phát triển mã nguồn mở.*
