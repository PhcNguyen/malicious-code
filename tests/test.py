import __init__
from lib.modules.yaml import safe_load

with open('scripts/setting.yaml', 'r') as file:
    data = safe_load(file)['contact']
    print(data)