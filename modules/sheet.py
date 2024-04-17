import json
from requests import get, post
try:
    from google.oauth2 import service_account as SACC
    from googleapiclient.discovery import build
except:
    from system import System
    from subprocess import run, DEVNULL
    packages = ['google-auth-httplib2', 'google-auth-oauthlib', 'google-api-python-client']
    brk = '--break-system-packages'

    for package in packages:
        run(['pip', 'install', package, brk], stdout=DEVNULL, stderr=DEVNULL)

    System().Reset()


class GoogleSheet:
    def __init__(self):
        self.id_sheet = '10rs_CfL4W5uKJI-ueX1n1MVZF4DT8uzqyb7wgtp0zfo'
        self._loadservice()
        self._createservice()
    
    def _loadservice(self) -> dict:
        with open('scripts/credentials.json', 'r') as file:
            self.api_sheet = json.load(file)
        
    def _createservice(self):
        try:
            credentials = SACC.Credentials.from_service_account_info(
                self.api_sheet,
                scopes = ['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(e)
    
    def get_all_values(self, sheet: str = 'Sheet1') -> list:
        if not hasattr(self, '_values'):
            result = self.service.spreadsheets().values().get(
                spreadsheetId = self.id_sheet,
                range = sheet
            ).execute()
            self._values = result.get('values', [])
        return self._values
    
    def UpdateValuesInRange(self, values: list, range: str):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.id_sheet,
            range=range,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result
    
    def UpdateValues(self, values, Sheet: str = 'Sheet1'):
        Row = len(self.get_all_values()) + 1
        range_str = f'{Sheet}!A{Row}:F{Row}'
        return self.UpdateValuesInRange(values, range_str)
    
    def UpdateColumn(self, values, Rowid, Sheet: str = 'Sheet1'):
        range = f'{Sheet}!A{Rowid}:A'
        return self.UpdateValuesInRange(values, range)
