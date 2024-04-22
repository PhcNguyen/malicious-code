# Class GoogleSheet
from google.oauth2 import service_account as SACC # type: ignore
from googleapiclient.discovery import build
from modules.system import Console


class GoogleSheet:
    def __init__(self, id: str) -> None:
        self.id_sheet = id
        self._create_service()
    
    def _create_service(self) -> None:
        try:
            credentials = SACC.Credentials.from_service_account_file(
                'scripts/credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            Console('127.0.0.1', e, 'Red')

    def AllValues(self, sheet='Sheet1') -> list:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.id_sheet,
            range=sheet
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
    
    def UpdateValues(self, values, sheet='Sheet1'):
        row = len(self.AllValues(sheet)) + 1
        range_str = f'{sheet}!A{row}:F{row}'
        return self.UpdateValuesInRange(values, range_str)