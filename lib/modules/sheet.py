from typing import List, Dict, Any
from .service_account import Credentials
from googleapiclient.discovery import build


class GoogleSheet:
    def __init__(self, id: str) -> None:
        self.id_sheet: str = id
        self.service: Any = None
        self.__create_service()
    
    def __create_service(self) -> None:
        try:
            credentials: Credentials = Credentials.from_service_account_file(
                'scripts/credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            return e

    def get_all_values(self, sheet: str = 'Sheet1') -> List[List[str]]:
        result: Dict[str, List[List[str]]] = self.service.spreadsheets().values().get(
            spreadsheetId=self.id_sheet,
            range=sheet
        ).execute()
        self._values: List[List[str]] = result.get('values', [])
        return self._values
    
    def update_values_in_range(self, values: List[List[str]], range_str: str) -> Dict[str, Any]:
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
    
    def update_values(self, values: List[List[str]], sheet: str = 'Sheet1') -> Dict[str, Any]:
        row: int = len(self.get_all_values(sheet)) + 1
        range_str: str = f'{sheet}!A{row}:F{row}'
        return self.update_values_in_range(values, range_str)