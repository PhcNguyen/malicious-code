import re

def safe_load(stream) -> dict:
    yaml_data = {}
    current_list = []
    current_key = None
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