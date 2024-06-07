## SheetApis

### `SheetApis` Class:
- `__init__(self, id: str)`: The initialization method takes a Google Sheets ID and initializes the Google Sheets API service.
   
- `__create_service(self)`: This method creates the Google Sheets API service using authentication information from a JSON file and initializes a service.

- `get_all_values(self, sheet: str = 'Sheet1') -> List[List[str]]`: This method retrieves all values from a specific sheet in Google Sheet.
   
- `update_values_in_range(self, values: List[List[str]], range_str: str) -> Dict[str, Any]`: This method updates values within a specified range on Google Sheet with provided new values.
   
- `update_values(self, values: List[List[str]], sheet: str = 'Sheet1') -> Dict[str, Any]`: This method updates values on Google Sheet, increases the number of rows, and uses a new range for the updated values.
---
```python
    # Initialize a SheetApis object with the ID of the Google Sheets
    sheet = SheetApis("your_sheet_id")

    # Get all values from a specific sheet
    all_values = sheet.get_all_values()

    # Update values on Google Sheet
    new_values = [['A1', 'B1', 'C1'], ['A2', 'B2', 'C2']]
    sheet.update_values(new_values)
```
