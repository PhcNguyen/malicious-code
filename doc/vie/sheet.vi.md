# GoogleSheet Class

Lớp `GoogleSheet` cung cấp các phương thức để tương tác với Google Sheets thông qua Google Sheets API.

## Cách Thức Hoạt Động

1. **Khởi tạo**: Khi khởi tạo một đối tượng `GoogleSheet`, nó sẽ tải thông tin tài khoản dịch vụ từ tệp `credentials.json` và tạo một dịch vụ Google Sheets.

2. **Lấy tất cả các giá trị**: Phương thức `get_all_values()` trả về tất cả các giá trị từ một bảng tính cụ thể.

3. **Cập nhật giá trị trong một phạm vi**: Phương thức `UpdateValuesInRange()` cập nhật một loạt các ô trong bảng tính với một danh sách giá trị.

4. **Cập nhật giá trị**: Phương thức `UpdateValues()` thêm một hàng mới vào bảng tính với một danh sách giá trị.

5. **Cập nhật cột**: Phương thức `UpdateColumn()` cập nhật một cột trong bảng tính với một danh sách giá trị.

## Cách Sử Dụng

Đầu tiên, hãy khởi tạo một đối tượng `GoogleSheet`:

```python
sheet = GoogleSheet()
```
- Sau đó, bạn có thể sử dụng các phương thức của đối tượng sheet để tương tác với Google Sheets. Ví dụ, để lấy tất cả các giá trị từ bảng tính mặc định, bạn có thể gọi:
```python
values = sheet.get_all_values()
```
- Để cập nhật một hàng mới trong bảng tính với một danh sách giá trị, bạn có thể gọi:
```python
values = ['value1', 'value2', 'value3']
sheet.UpdateValues(values)
```
- Để cập nhật một cột trong bảng tính với một danh sách giá trị, bạn có thể gọi:
```python
values = ['value1', 'value2', 'value3']
row_id = 1
sheet.UpdateColumn(values, row_id)
```

Hy vọng rằng tệp markdown này sẽ giúp bạn hiểu rõ hơn về cách thức hoạt động và cách sử dụng lớp `GoogleSheet`. Nếu bạn có bất kỳ câu hỏi hoặc vấn đề gì khác, đừng ngần ngại liên hệ với tôi.
