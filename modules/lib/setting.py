from modules.system import Console, ConsoleInput, System
import os.path
import json


def get_input(prompt: str) -> str:
    value = ConsoleInput(prompt, 'Green')
    while not value:
        Console('127.0.0.1', f'{prompt} cannot be empty!', 'Red')
        value = ConsoleInput(prompt, 'Green')
    return value

def load_settings(setting: str) -> dict:
    try:
        with open(setting, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        Console('127.0.0.0', str(e), 'Red')
        os.remove(setting)
        System().Reset()

def save_settings(setting: str, data: dict) -> None:
    try:
        with open(setting, 'w') as f:
            f.write(json.dumps(data, indent=4))
        System().Reset()
    except Exception as e:
        Console('127.0.0.0', str(e), 'Red')
        System().Reset()

def Setting() -> None:
    setting = 'scripts/setting.json'
    if os.path.exists(setting):
        data = load_settings(setting)
        data_list = [data['ip'], data['port'], data['id']]
        return data_list
    else:
        Console('127.0.0.1', 'SETTING', 'Red')
        ip = get_input('IP: ')
        port = int(get_input('PORT: '))
        ids = get_input('ID SHEET: ')
        data = {"ip": ip, "port": port, "id": ids}
        save_settings(setting, data)
