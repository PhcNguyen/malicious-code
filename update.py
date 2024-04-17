import subprocess

subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', '"1.0.5"'])
subprocess.run(['git', 'push', 'origin', 'main'])