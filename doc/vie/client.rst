================================
Hướng Dẫn Sử Dụng Lớp Ransomware
================================

Đoạn mã đã cung cấp tạo ra một lớp `Ransomware` với các phương thức để mã hóa và giải mã dữ liệu.

1. **Khởi tạo**: Khi khởi tạo một đối tượng `Ransomware`, bạn cần cung cấp địa chỉ IP (`host`) và cổng (`port`) của máy chủ mà bạn muốn kết nối.

.. code-block:: python

    bot = Ransomware('192.168.1.12', 19100)

2. **Kết nối với máy chủ**: Phương thức `ConnectServer` sẽ thử kết nối với máy chủ thông qua địa chỉ IP và cổng đã cung cấp. Nếu không thể kết nối sau 3 lần thử, hệ thống sẽ được đặt lại.

.. code-block:: python

    bot.ConnectServer()

3. **Mã hóa**: Phương thức `Encrypted` sẽ mã hóa dữ liệu sử dụng khóa riêng tư đã được tạo.

.. code-block:: python

    bot.Encrypted()

4. **Giải mã**: Phương thức `Decrypted` sẽ giải mã dữ liệu đã được mã hóa sử dụng cùng một khóa.

.. code-block:: python

    bot.Decrypted()

Lưu ý: Đoạn mã này chỉ nên được sử dụng cho mục đích học hỏi. Việc sử dụng nó để thực hiện các hành vi vi phạm pháp luật (như tấn công mạng) có thể dẫn đến hậu quả pháp lý nghiêm trọng. Hãy luôn tuân thủ quy định pháp luật khi sử dụng và phát triển mã nguồn mở.