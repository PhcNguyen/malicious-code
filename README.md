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