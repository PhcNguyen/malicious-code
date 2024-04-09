from subprocess import run

try:
  import pyinstaller
  file: str = input('Nhap file muon xuat exe: ')
  run(['pyinstaller', '--onefile', '--noconsole', file])
except ModuleNotFoundError:
  try:
    run(['pip', 'install', 'pyinstaller'])
  except:
    print('[Errno 2] No such file or directory: "pyinstaller"')

