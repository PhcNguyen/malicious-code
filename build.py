from subprocess import run, DEVNULL
from lib.system import System
from time import time
import os.path


start = time()
Terminal = System()
Terminal.Clear()
Terminal.Init()


def _check():
    global start
    end = time()
    elapsed_time = end - start
    Terminal.Console('Timer', f'The program runs for: {elapsed_time:.2f} seconds', 'Yellow')


if os.path.isdir('venv'):
    try:
        run(["python", "-m", "venv", "env"], 
            stdout=DEVNULL, 
            stderr=DEVNULL, 
            check=True
        )
    except:
        Terminal.Console(
            'Build', 
            "Cannot create venv", 
            'Red'
        )
        _check()
        Terminal.Exit()

try:
    import google.oauth2 # type: ignore
    import googleapiclient.discovery
except ImportError as e:
    required_packages: list = [
        'google-auth-httplib2', 
        'google-auth-oauthlib', 
        'google-api-python-client'
    ]
    installed_packages = run(
        ['pip', 'list', '--format=json'], 
        stdout=DEVNULL, 
        stderr=DEVNULL, 
        universal_newlines=True
    )
    if all(package in installed_packages for package in required_packages):
        Terminal.Console(
            'Build', 
            'All required packages are already installed.', 
            'Green'
        )
    else:
        for package in required_packages:
            try:
                result = run(
                    ['pip', 'install', package], 
                    stdout=DEVNULL, 
                    stderr=DEVNULL, 
                    universal_newlines=True
                )
                if result.returncode == 0:
                    Terminal.Console(
                        'Build', 
                        f'Installed {package} successfully!', 
                        'Pink'
                    )
                else:
                    Terminal.Console(
                        'Build', 
                        f'Error installing {package}: {result.stdout}', 
                        'Red'
                    )
                    Terminal.Exit()
                    _check()
            except Exception as e:
                Terminal.Console('Build', e, 'Red')
finally:
    _check()