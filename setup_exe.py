import os ,sys
import subprocess

try:
    import pyinstaller
except ImportError:
    try:
        subprocess.run(['pip', 'install', 'pyinstaller'])
        subprocess.run(['pip', 'install', 'cryptography'])
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except FileNotFoundError:
        print('[Errno 2] No such file or directory: "pip"')
        exit()

file_name = input('Nhap file muon xuat exe: ')

try:
    subprocess.run(['pyinstaller', '--onefile', '--noconsole', file_name])
except FileNotFoundError:
    print('[Errno 2] No such file or directory: "pyinstaller"')


