from lib.system import System
from subprocess import run, DEVNULL

Terminal = System()
Terminal.Init()
Terminal.Clear()

try:
    with open('scripts/.version', 'r') as file:
        __version__ = file.read()
except Exception as e:
    Terminal.Console('GitHub', e, 'Red')
    Terminal.Command('exit')
try:
    run(['git', 'add', '.'], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', 'git add .', 'Red')

    run(['git', 'commit', '-m', __version__], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', f'git commit -m "{__version__}"', 'Red')

    run(['git', 'push', 'origin', 'main'], stdout=DEVNULL, stderr=DEVNULL)
    Terminal.Console('GitHub', 'git push origin main', 'Red')

except Exception as e:
    Terminal.Console('GitHub', e, 'Red')
    Terminal.Command('exit')