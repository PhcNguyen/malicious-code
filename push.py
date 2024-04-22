import time
import requests
from lib.system import System
from subprocess import run, DEVNULL


Terminal = System()
Terminal.Init()
Terminal.Clear()
start = time.time()


try:
    response = requests.get('https://github.com')
    if response.status_code == 200:
        Terminal.Console('Ping', 'Connect to github.com successful', 'Orange')
    else:
        Terminal.Console('Ping', f'Error: HTTP status code {response.status_code}', 'Red')
        Terminal.Exit()
except Exception as e:
    Terminal.Console('Ping', e, 'Red')
    Terminal.Exit()

try:
    with open('scripts/.version', 'r') as file:
        __version__ = file.read()
        
except FileNotFoundError:
    Terminal.Console('GitHub', 'File .version not found', 'Red')
    Terminal.Exit()

except Exception as e:
    Terminal.Console('GitHub', f'Error reading .version file: {e}', 'Red')
    Terminal.Exit()

try:
    run(['git', 'add', '.'], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', 'git add .', 'Blue')

    run(['git', 'commit', '-m', __version__], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', f'git commit -m "{__version__}"', 'Blue')

    run(['git', 'push', 'origin', 'main'], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', 'git push origin main', 'Blue')

    end = time.time()
    elapsed_time = end - start
    Terminal.Console('Timer', f'Elapsed time for push: {elapsed_time:.2f} seconds', 'Yellow')

except FileNotFoundError:
    Terminal.Console('GitHub', 'Git command not found', 'Red')
    Terminal.Exit()

except Exception as e:
    Terminal.Console('GitHub', f'Error executing Git command: {e}', 'Red')
    Terminal.Exit()