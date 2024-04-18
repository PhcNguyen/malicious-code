## Ransomware Directory Structure

```
[ Malicious-Code ] [1.0.6]
  ├──[ doc ]
  │    ├── requirements.txt
  │    ├─────────────────────[ eng ]
  │    └─[ vie ]               ├── client.md
  │        ├── encdec.md       ├── server.md
  │        ├── system.md       └── ...
  │        └── ...
  │
  ├──[ modules ]        
  │    ├── __init__.py    
  │    ├── encdec.py
  │    ├── setiing.py
  │    └── system.py
  │
  ├─────────────────────[ scripts ]
  │                       ├── credentials.json
  ├──[ test ]             ├── extensions.yaml
  │    ├── __init__.py    ├── info.txt
  │    ├── server.py      └── setting.json
  │    └── client.py
  │
  ├── .gitignore 
  ├── install-lib.py
  ├── LICENSE
  ├── main.sh
  ├── README.md
  └── update.py
```
---
### Language English

The `Ransomware` project consists of the following directories and files:

- `doc`: This directory contains documentation files.
    - `requirements.txt`: This file contains a list of Python libraries required for the project.
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
- `README.md`: This file contains project introduction information.
---
### Ngôn ngữ Tiếng Việt

Dự án `Ransomware` bao gồm các thư mục và tệp sau:

- `doc`: Thư mục này chứa tài liệu hướng dẫn sử dụng mã nguồn.
    - `requirements.txt`: Tệp này chứa danh sách các thư viện Python cần thiết cho dự án.
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
- `README.md`: Tệp này chứa thông tin giới thiệu dự án.