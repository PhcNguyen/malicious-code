# AesCipher Documentation

## Describe
`AesCipher` cung cấp các phương thức để mã hóa và giải mã dữ liệu bằng thuật toán AES trong chế độ CTR. Lớp này cho phép sử dụng kích thước khóa khác nhau và sử dụng các IV (Vector khởi tạo) để tăng cường tính bảo mật.

## Phương thức
### 1. AesCipher(int keySize = 256)

- **Describe**: Khởi tạo một thể hiện mới của lớp `AesCipher` với kích thước khóa chỉ định.
- **Parameter**:
  - `keySize`: Kích thước khóa (128, 192, hoặc 256 bits).

### 2. Encrypt(byte[] plaintext, byte[] iv)

- **Describe**: Mã hóa dữ liệu bằng AES CTR.
- **Parameter**:
  - `plaintext`: Dữ liệu gốc cần mã hóa.
  - `iv`: Vector khởi tạo cho mã hóa.
- **Returns**: Dữ liệu đã mã hóa.

### 3. Decrypt(byte[] cipherText, byte[] iv)

- **Describe**: Giải mã dữ liệu đã mã hóa bằng AES CTR.
- **Parameter**:
  - `cipherText`: Dữ liệu đã mã hóa cần giải mã.
  - `iv`: Vector khởi tạo được sử dụng trong mã hóa.
- **Returns**: Dữ liệu gốc.

### 4. EncryptFile(string filePath, long fileSize)

- **Describe**: Mã hóa một tệp và tạo một tệp mã hóa mới với phần mở rộng `.enc`.

- **Parameter**:
    - `filePath`: Đường dẫn của tệp cần mã hóa.
    - `fileSize`: Kích thước của tệp cần mã hóa.

- **How it works**:
    1. **Đọc tệp gốc**: Phương thức mở tệp gốc để đọc dữ liệu theo từng khối dựa trên `fileSize`, giúp xử lý tệp lớn mà không cần tải toàn bộ nội dung vào bộ nhớ.
    2. **Mã hóa**: Dữ liệu được mã hóa từng khối sử dụng thuật toán `AES` với chế độ `CTR (Counter)`. Khóa mã hóa và `IV (Vector khởi tạo)` sẽ được sử dụng để đảm bảo tính bảo mật.
    3. **Ghi ra tệp mã hóa**: Dữ liệu mã hóa được ghi vào một tệp mới có cùng tên với tệp gốc, nhưng có phần mở rộng `.enc` để dễ dàng nhận biết là tệp mã hóa.

- **Returns**:     
    - `true` nếu tệp được mã hóa thành công.
    - `false` nếu xảy ra lỗi trong quá trình mã hóa hoặc ghi tệp.

### 5.
- **Describe**: Giải mã một tệp đã mã hóa và khôi phục tệp về nội dung ban đầu, đồng thời loại bỏ phần mở rộng `.enc` để khôi phục tên tệp gốc.

- **Parameter**:
    - `filePath`: Đường dẫn của tệp cần mã hóa.
    - `fileSize`: Kích thước của tệp cần mã hóa.

- **How it works**:
    1. **Mở tệp mã hóa**: Phương thức mở tệp đã mã hóa `(tệp có phần mở rộng .enc)` và đọc dữ liệu từng khối theo kích thước `fileSize`.
    2. **Giải mã**: Sử dụng thuật toán `AES` với chế độ `CTR` và `IV` tương tự như khi mã hóa, nội dung của từng khối sẽ được giải mã.
    3. **Ghi ra tệp gốc**: Dữ liệu giải mã sẽ được ghi vào một tệp mới có tên giống tệp gốc ban đầu `(không bao gồm phần mở rộng .enc)`.

- **Returns**:
    - `true` nếu tệp được giải mã thành công và khôi phục về trạng thái ban đầu.
    - `false` nếu có lỗi trong quá trình giải mã hoặc ghi tệp gốc.

## Example Use

```csharp
var aesCipher = new AesCipher();

byte[] key = aesCipher.key;
byte[] iv = new byte[16]; // IV ngẫu nhiên
byte[] encrypted = aesCipher.Encrypt(plaintext, iv);
byte[] decrypted = aesCipher.Decrypt(encrypted, iv);
```

## Contacts

If you have any questions, please reach out to the developers at **PhcNguyen Developers**.

You can also contact me via Telegram: [phcnguyenz](https://t.me/phcnguyenz).