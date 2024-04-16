===============================
Encdec Detailed Guide
===============================

Đoạn mã Python này bao gồm một số hàm để xử lý các tệp.

1. **Khởi tạo Fernet**: Trước khi gọi các hàm `Encrypt` hoặc `Decrypt`, bạn cần khởi tạo một đối tượng `Fernet` với khóa bí mật. `Fernet` là một hệ thống mã hóa đối xứng an toàn được cung cấp bởi thư viện `cryptography`.

.. code-block:: python

    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

2. **Mã hóa các tệp**: Hàm `Encrypt` sẽ mã hóa tất cả các tệp được liệt kê bởi hàm `List_Files`. Mỗi tệp sẽ được đọc và mã hóa từng phần, sau đó ghi vào một tệp tạm thời. Cuối cùng, tệp tạm thời sẽ thay thế tệp gốc.

.. code-block:: python

    Encrypt(cipher_suite)

3. **Giải mã các tệp**: Hàm `Decrypt` sẽ giải mã tất cả các tệp đã được mã hóa bởi hàm `Encrypt`, tương tự như quá trình mã hóa nhưng ngược lại.

.. code-block:: python

    Decrypt(cipher_suite)

4. **Liệt kê các tệp**: Hàm `List_Files` sẽ trả về một danh sách các tệp dựa trên các phần mở rộng tệp được định nghĩa trong tệp `scripts/extensions.yaml`. Hàm này sử dụng `Path.home().rglob('*')` để liệt kê tất cả các tệp trong thư mục home của người dùng.

.. code-block:: python

    files = List_Files()

Lưu ý: Đoạn mã này chỉ nên được sử dụng cho mục đích học hỏi. Việc sử dụng nó để thực hiện các hành vi vi phạm pháp luật (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Hãy luôn tuân thủ quy định pháp luật khi sử dụng và phát triển mã nguồn mở.