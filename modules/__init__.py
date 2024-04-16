#  Ransomware
#   ├── doc
#   │   ├── eng
#   │   │   ├── client.rst
#   │   │   ├── encdec.rst
#   │   │   ├── server.rst
#   │   │   └── system.rst
#   │   │
#   │   └── vie
#   │       ├── client.rst
#   │       ├── encdec.rst
#   │       ├── server.rst
#   │       └── system.rst
#   ├───────────────────── scripts
#   ├── modules             ├── extensions.yaml 
#   │   ├── __init__.py     └── info.txt
#   │   ├── encdec.py
#   │   └── system.py
#   │ 
#   ├── test
#   │   ├── __init__.py
#   │   ├── server.py
#   │   └── client.py
#   │
#   ├── .gitidnore
#   ├── LICENSE
#   ├── README.md
#   └── requirements.txt

# doc: Thư mục này chứa tài liệu hướng dẫn sử dụng mã nguồn. Nó được chia thành hai thư mục con:
# ├── eng: Chứa các tệp .rst hướng dẫn bằng tiếng Anh.
# └── vie: Chứa các tệp .rst hướng dẫn bằng tiếng Việt.

# modules: Thư mục này chứa các module Python
# scripts: Thư mục này chứa các tệp script.
# test: Thư mục này chứa các tệp kiểm thử.

# .gitignore: Tệp này dùng để chỉ định những tệp hoặc thư mục không được Git theo dõi.
# LICENSE: Tệp này chứa thông tin về giấy phép của dự án.
# README.md: Tệp này chứa thông tin giới thiệu và hướng dẫn sử dụng dự án.
# requirements.txt: Tệp này chứa danh sách các thư viện Python cần thiết cho dự án.


__all__ = ['encdec', 'system']
__version__ = '1.0.5'