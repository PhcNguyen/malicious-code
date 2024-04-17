try:
    import google.oauth2 
    import googleapiclient.discovery
    import cryptography
except:
    from subprocess import run, DEVNULL
    packages = ['google-auth-httplib2', 
                'google-auth-oauthlib', 
                'google-api-python-client',
                'cryptography']
    brk = '--break-system-packages'

    for package in packages:
        run(['pip', 'install', package, brk], stdout=DEVNULL, stderr=DEVNULL)
        print(f'{package} success !')