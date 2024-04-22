from subprocess import run, DEVNULL
from lib.system import System

Terminal = System()
Terminal.Clear()
Terminal.Init()

try:
    import google.oauth2  # type: ignore
    import googleapiclient.discovery
    import cryptography
except ImportError as e:
    try:
        packages = ['google-auth-httplib2', 
                    'google-auth-oauthlib', 
                    'google-api-python-client']

        for package in packages:
            run(['pip', 'install', package, '--break-system-packages'], stdout=DEVNULL, stderr=DEVNULL)
            Terminal.Console('Build', f'Installed {package} successfully !', 'Pink')
    except Exception as e:
        Terminal.Console('Build', f'Error installing packages: {e}', 'Red')
        Terminal.Exit()
else:
    Terminal.Console('Build', 'All required packages are already installed.', 'Green')