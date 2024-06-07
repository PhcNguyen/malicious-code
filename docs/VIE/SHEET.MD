## SheetApis

### `SheetApis` Class:
- `__init__(self, id: str)`: Phương thức khởi tạo nhận một định danh Google Sheets ID và khởi tạo dịch vụ API Google Sheets.
   
- `__create_service(self)`: Phương thức tạo dịch vụ API Google Sheets bằng cách sử dụng thông tin xác thực từ một tệp JSON và khởi tạo một dịch vụ.

- `get_all_values(self, sheet: str = 'Sheet1') -> List[List[str]]`: Phương thức này lấy tất cả các giá trị từ một sheet cụ thể trong Google Sheet.
   
- `update_values_in_range(self, values: List[List[str]], range_str: str) -> Dict[str, Any]`: Phương thức này cập nhật các giá trị trong một phạm vi được chỉ định trên Google Sheet với các giá trị mới được cung cấp.
   
- `update_values(self, values: List[List[str]], sheet: str = 'Sheet1') -> Dict[str, Any]`: Phương thức này cập nhật các giá trị trên Google Sheet, tăng số hàng và sử dụng một phạm vi mới cho các giá trị cập nhật.
---
```python
# Khởi tạo một đối tượng SheetApis với ID của Google Sheets
sheet = SheetApis("your_sheet_id")

# Lấy tất cả các giá trị từ một sheet cụ thể
all_values = sheet.get_all_values()

# Cập nhật các giá trị trên Google Sheet
new_values = [['A1', 'B1', 'C1'], ['A2', 'B2', 'C2']]
sheet.update_values(new_values)
```

