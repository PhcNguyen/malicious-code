# Cấu trúc thư mục Ransomware

Dự án `Ransomware` bao gồm các thư mục và tệp sau:
```
[ Ransomware ]
  ├──[ doc ]
  │    ├── DOCUMENT.md
  │    ├──────────────────────[ eng ]
  │    └──[ vie ]               ├── client.en.md
  │         ├── client.vi.md    ├── encdec.en.md
  │         ├── encdec.vi.md    ├── server.en.md
  │         ├── server.vi.md    └── system.en.md
  │         └── system.vi.md
  │
  ├──[ modules ]        
  │    ├── __init__.py    
  │    ├── encdec.py
  │    └── system.py
  ├─────────────────────[ scripts ]
  ├──[ test ]             ├── extensions.yaml
  │    ├── __init__.py    └── info.txt
  │    ├── server.py 
  │    └── client.py
  │
  ├── .gitignore 
  ├── LICENSE
  ├── README.md
  └── requirements.txt
```
- `doc`: Thư mục này chứa tài liệu hướng dẫn sử dụng mã nguồn.
    - `eng`: Chứa các tệp `.rst` hướng dẫn bằng tiếng Anh.
    - `vie`: Chứa các tệp `.rst` hướng dẫn bằng tiếng Việt.
- `modules`: Thư mục này chứa các module Python.
    - `__init__.py`
    - `encdec.py`
    - `system.py`
- `scripts`: Thư mục này chứa các tệp script.
    - `extensions.yaml`
    - `info.txt`
- `test`: Thư mục này chứa các tệp kiểm thử.
    - `__init__.py`
    - `server.py`
    - `client.py`
- `.gitignore`: Tệp này dùng để chỉ định những tệp hoặc thư mục không được Git theo dõi.
- `LICENSE`: Tệp này chứa thông tin về giấy phép của dự án.
- `README.md`: Tệp này chứa thông tin giới thiệu và hướng dẫn sử dụng dự án.
- `requirements.txt`: Tệp này chứa danh sách các thư viện Python cần thiết cho dự án.
