## Ransomware Directory Structure

```
[ Malicious-Code ] [ 1.0.6 ]
  ├──[ doc ]
  │    ├── requirements.txt
  │    ├─────────────────────[ english ]
  │    └─[ vietnam ]           ├── client.md
  │        ├── encdec.md       ├── server.md
  │        ├── system.md       └── ...
  │        └── ...
  │
  ├──[ lib ]──── system.py
  │    ├────────────────────[ cryptography ]       
  │    └── [ modules ]        ├── fernet.py      
  │          ├── yaml.py      └── encdec.py               
  │          └── sheet.py
  │
  ├─────────────────────[ scripts ]
  │                       ├── extensions.yaml
  ├──[ test-http ]        ├── setting.yaml
  │    ├── client.py      └── ...
  │    └── server.py      
  │
  ├──[ test-socket ]
  │    ├── client.py 
  │    └── server.py
  │
  └── ...
```
---
### Language English

The `Ransomware` project consists of the following directories and files:

- `doc`: This directory contains documentation files.
    - `eng`: Contains English language `.md` files.
    - `vie`: Contains Vietnamese language `.md` files.
- `lib`: This directory contains Python modules.
- `scripts`: This directory contains script files.
- `test`: This directory contains test files.
---
### Ngôn ngữ Tiếng Việt

Dự án `Ransomware` bao gồm các thư mục và tệp sau:

- `doc`: Thư mục này chứa tài liệu hướng dẫn sử dụng mã nguồn.
    - `eng`: Chứa các tệp `.md` hướng dẫn bằng tiếng Anh.
    - `vie`: Chứa các tệp `.md` hướng dẫn bằng tiếng Việt.
- `lib`: Thư mục này chứa các module Python.
- `scripts`: Thư mục này chứa các tệp script.
- `test`: Thư mục này chứa các tệp kiểm thử.