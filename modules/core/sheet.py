from modules.google import Credentials
from googleapiclient.discovery import build


class SheetApis:
    def __init__(self, id: str) -> None:
        self.id_sheet = id
        self.service = None
        self.create_service()
    
    def create_service(self) -> None:
        try:
            credentials = Credentials.from_service_account_file(
                'scripts/credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print('[SYSTEM] --> ' + str(e))

    def get_all_values(self, sheet: str = 'Sheet1') -> list:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.id_sheet,
            range=sheet
        ).execute()
        self._values = result.get('values', [])
        return self._values
    
    def update_values_in_range(self, values: list, range_str: str) -> dict:
        body= {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.id_sheet,
            range=range_str,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result
    
    def update_values(self, values: list, sheet: str = 'Sheet1') -> dict:
        row: int = len(self.get_all_values(sheet)) + 1
        range_str: str = f'{sheet}!A{row}:F{row}'
        return self.update_values_in_range(values, range_str)