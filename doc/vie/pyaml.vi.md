Hàm `safe_load` của bạn đang phân tích cú pháp một luồng dữ liệu YAML và trả về một từ điển Python. Dưới đây là cách nó hoạt động:

1. **Khởi tạo các biến**: Hàm bắt đầu bằng cách khởi tạo một từ điển rỗng `yaml_data`, một danh sách rỗng `current_list`, và một khóa `current_key` được đặt thành `None`. Nó cũng khởi tạo một biểu thức chính quy `pattern` để khớp với các dòng có dạng `- value` hoặc `key: value`.

2. **Đọc từng dòng**: Hàm sau đó lặp qua từng dòng trong luồng đầu vào. Nếu dòng là một chuỗi trống, nó kiểm tra xem có danh sách hiện tại không. Nếu có, nó thêm danh sách vào từ điển với khóa hiện tại và sau đó xóa danh sách.

3. **Phân tích cú pháp dòng**: Nếu dòng không phải là một chuỗi trống, hàm sẽ cố gắng khớp dòng với biểu thức chính quy. Nếu dòng khớp với biểu thức chính quy, nó sẽ kiểm tra xem dòng có phải là một giá trị danh sách (được đánh dấu bằng `-`) hay không. Nếu có, nó thêm giá trị vào danh sách hiện tại. Nếu không, nó coi dòng là một cặp `key: value`.

4. **Xử lý cặp `key: value`**: Khi hàm gặp một cặp `key: value`, nó kiểm tra xem có danh sách hiện tại không. Nếu có, nó thêm danh sách vào từ điển với khóa hiện tại và sau đó xóa danh sách. Nó sau đó cập nhật khóa hiện tại và giá trị hiện tại dựa trên dòng hiện tại. Nếu giá trị không phải là `None`, nó thêm cặp `key: value` vào từ điển.

5. **Kết thúc danh sách**: Cuối cùng, sau khi đã xử lý tất cả các dòng, nếu vẫn còn một danh sách chưa được thêm vào từ điển, hàm sẽ thêm nó vào từ điển.

Sau khi đã xử lý tất cả các dòng, hàm trả về từ điển `yaml_data`, chứa tất cả các cặp `key: value` và `key: list` đã được phân tích cú pháp từ luồng đầu vào.
