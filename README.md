# Ransomware Directory Structure

The `Ransomware` project consists of the following directories and files:
```
[ Ransomware ]
  ├──[ doc ]
  │    ├── DOCUMENT.md
  │    ├─────────────────────[ eng ]
  │    └─[ vie ]               ├── client.en.md
  │        ├── encdec.vi.md    ├── server.en.md
  │        ├── system.vi.md    └── ...
  │        └── ...
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
  ├── ENG.md
  ├── VIE.md
  └── requirements.txt
```
- `doc`: This directory contains documentation files.
    - `eng`: Contains English language `.md` files.
    - `vie`: Contains Vietnamese language `.md` files.
- `modules`: This directory contains Python modules.
    - `__init__.py`
    - `encdec.py`
    - `system.py`
- `scripts`: This directory contains script files.
    - `extensions.yaml`
    - `info.txt`
- `test`: This directory contains test files.
    - `__init__.py`
    - `server.py`
    - `client.py`
- `.gitignore`: This file specifies intentionally untracked files to ignore by Git.
- `LICENSE`: This file contains information about the project's license.
- `README.md`: This file contains introduction and usage instructions for the project.
- `requirements.txt`: This file contains a list of Python libraries required for the project.

# Cấu trúc thư mục Ransomware

Dự án `Ransomware` bao gồm các thư mục và tệp sau:

- `doc`: Thư mục này chứa tài liệu hướng dẫn sử dụng mã nguồn.
    - `eng`: Chứa các tệp `.md` hướng dẫn bằng tiếng Anh.
    - `vie`: Chứa các tệp `.md` hướng dẫn bằng tiếng Việt.
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