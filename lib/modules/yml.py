import re
from typing import Any, Dict, List

"""
Parameters:
stream (List[str]): A list of strings representing the YAML data stream.

Returns:
yaml_data (Dict[str, Any]): A dictionary containing the loaded YAML data. Keys are strings representing keys in the YAML document and the corresponding values are the respective data.

Steps:
 - Initialize a dictionary yaml_data to store the YAML data.
 - Initialize a list current_list to store the values of a YAML list.
 - Initialize a string current_key to store the current key of the YAML dictionary.
 - Create a regular expression pattern to parse the syntax of lines in the YAML data stream.
 - Iterate through each line in the data stream:
 - Trim leading and trailing whitespace from the line.
 - If the line is empty, check if it marks the end of a list. If so, store the list in the yaml_data dictionary and reset current_list.
 - If not, parse the syntax of the line and store the data in the yaml_data dictionary.
 - Return the yaml_data dictionary after all YAML data has been loaded.

Note:
- This function assumes that the input YAML data has been validated and not tampered with to avoid security vulnerabilities. It is a basic YAML loading function and does not provide advanced security mechanisms.
- You can add or modify information in this documentation as per your project requirements or criteria.
"""

def safe_load(stream: List[str]) -> Dict[str, Any]:
    yaml_data: Dict[str, Any] = {}
    current_list: List[Any] = []
    current_key: str = None
    pattern = re.compile(r'(-\s*)(.*)|([^:]*):(.*)')

    for line in stream:
        stripped_line = line.strip()
        if not stripped_line:
            if current_list and current_key is not None:  # End of a list
                yaml_data[current_key] = current_list
                current_list = []
            continue

        match = pattern.match(stripped_line)
        if match:
            if match.group(1):  # matched '- value'
                current_list.append(match.group(2))
            else:  # matched 'key: value'
                if current_list and current_key is not None:  # End of a list
                    yaml_data[current_key] = current_list
                    current_list = []

                current_key = match.group(3).strip()
                value = match.group(4).strip() if match.group(4) else None
                if value or value is None:
                    yaml_data[current_key] = value

    if current_list and current_key is not None:  # End of a list
        yaml_data[current_key] = current_list
    return yaml_data