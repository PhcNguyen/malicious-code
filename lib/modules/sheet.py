from typing import List, Dict, Any
from google.oauth2 import service_account# type: ignore
from googleapiclient.discovery import build

class GoogleSheet:
    def __init__(self, id: str) -> None:
        self.id_sheet: str = id
        self.service: Any = None
        self._create_service()
    
    def _create_service(self) -> None:
        try:
            credentials: service_account.Credentials = service_account.Credentials.from_service_account_file(
                'scripts/credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            return e

    def AllValues(self, sheet: str = 'Sheet1') -> List[List[str]]:
        result: Dict[str, List[List[str]]] = self.service.spreadsheets().values().get(
            spreadsheetId=self.id_sheet,
            range=sheet
        ).execute()
        self._values: List[List[str]] = result.get('values', [])
        return self._values
    
    def UpdateValuesInRange(self, values: List[List[str]], range_str: str) -> Dict[str, Any]:
        body: Dict[str, List[List[str]]] = {
            'values': values
        }
        result: Dict[str, Any] = self.service.spreadsheets().values().update(
            spreadsheetId=self.id_sheet,
            range=range_str,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result
    
    def UpdateValues(self, values: List[List[str]], sheet: str = 'Sheet1') -> Dict[str, Any]:
        row: int = len(self.AllValues(sheet)) + 1
        range_str: str = f'{sheet}!A{row}:F{row}'
        return self.UpdateValuesInRange(values, range_str)