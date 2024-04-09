try:
  import pyinstaller
  from subprocess import run
  file: str = input('Nhap file muon xuat exe: ')
  run(['pyinstaller', '--onefile', '--noconsole', file])
except ModuleNotFoundError:
  print('[Errno 2] No such file or directory: "pyinstaller"')

