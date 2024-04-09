from subprocess import DEVNULL
from subprocess import run 
try:
  import pyinstaller
except:
  print('Dang cai dat thu vien: pyinstaller')
  print('Vui long cho trong giy lat')
  run(['pip', 'install', 'pyinstaller'], stdout=DEVNULL, stderr=DEVNULL)

status = True
while status:
  try:
    file: str = input('Nhap file muon xuat exe: ')
    run(['pyinstaller', '--onefile', '--noconsole', file])
  except:
    print('file ban nhap khong dung !')
