import subprocess

subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', '1.0.6'])
subprocess.run(['git', 'push', 'origin', 'main'])