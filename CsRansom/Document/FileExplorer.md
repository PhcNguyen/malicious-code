# FileExplorer Documentation

## Introduce
`FileExplorer` là một lớp được thiết kế để quét, mã hóa và giải mã các tệp trên hệ thống. Lớp này hỗ trợ mã hóa tệp bằng thuật toán AES và có khả năng xử lý nhiều tệp cùng lúc.

`FileDetail` đại diện cho thông tin của một file bao gồm kích thước, tên, và đường dẫn đầy đủ.

## Tính năng
**Quét tệp**: Tìm kiếm và lưu trữ thông tin về các tệp có kích thước lớn hơn một ngưỡng nhất định.
**Mã hóa tệp**: Mã hóa tệp bằng AES với kích thước khóa 256 bit.
**Giải mã tệp**: Giải mã tệp đã được mã hóa trở về định dạng gốc.
**Ghi nhật ký**: Ghi lại các thông tin quan trọng trong quá trình quét và mã hóa.

## Layer Structure
### Attributes
- `logging`: Đối tượng ghi nhật ký để theo dõi hoạt động.
- `aesCipher`: Đối tượng mã hóa để thực hiện các hoạt động mã hóa và giải mã.
- `SpecificFiles`: Bộ sưu tập các tệp cụ thể đã được tìm thấy.
- `excludedDirectories`: Danh sách các thư mục không được quét (C:\\Program File, ...).
- `allowedFileExtensions`: Danh sách các phần mở rộng tệp được phép (.txt, .xml, ...).

### Methods
#### 1. `void EncryptFilesMultiple()`
Mã hóa tất cả các tệp trong `SpecificFiles` đồng thời.

#### 2. `void DecryptFilesMultiple()`
Giải mã tất cả các tệp trong `SpecificFiles` đồng thời.

#### 3. `void Scan(long minimumSize = 1024 * 1024, SortOrder sortOrder = SortOrder.Ascending)`
Quét hệ thống để tìm các tệp có kích thước lớn hơn `minimumSize`. Kết quả có thể được sắp xếp theo thứ tự tăng dần hoặc giảm dần.

#### 4. `void FindFiles(string path)`
Phương thức riêng để quét các tệp và thư mục trong đường dẫn đã cho.

## Example Use

```csharp
// Sử dụng lớp FileExplorer
FileExplorer fileExplorer = new FileExplorer();

// Bước 2: Quét các tệp cần mã hóa
List<FileDetail> filesToEncrypt = fileExplorer.Scan(minimumSize: 1024 * 1024); // Quét các tệp lớn hơn 1MB

// Bước 3: Mã hóa tất cả các tệp đã tìm thấy
fileExplorer.EncryptFilesMultiple();

// Bước 4: Giải mã tệp khi cần (ví dụ: giải mã tất cả các tệp đã mã hóa)
fileExplorer.DecryptFilesMultiple();
```

> [!Note]
> - Các tệp gốc sẽ bị xóa sau khi mã hóa thành công.
> - Đảm bảo bạn có quyền truy cập để quét và mã hóa các tệp.

---

## Contacts

If you have any questions, please reach out to the developers at **PhcNguyen Developers**.

You can also contact me via Telegram: [phcnguyenz](https://t.me/phcnguyenz).

