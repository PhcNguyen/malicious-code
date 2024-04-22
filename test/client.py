import requests

# Đường dẫn của máy chủ HTTP mà bạn đã tạo
server_url = "http://localhost:8000"

# Gửi yêu cầu GET đến máy chủ HTTP
response = requests.post(server_url)

# Kiểm tra mã trạng thái của phản hồi
if response.status_code == 200:
    print("Yêu cầu thành công!")
    print("Nội dung phản hồi:")
    print(response.text)
else:
    print(f"Lỗi: Mã trạng thái {response.status_code}")
