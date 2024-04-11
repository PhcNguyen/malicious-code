def safe_load(stream):

    yaml_data = {}
    current_list = []
    current_key = None

    for line in stream:
        # Loại bỏ các khoảng trắng ở đầu và cuối dòng
        stripped_line = line.strip()

        # Bỏ qua dòng nếu dòng đó trống
        if not stripped_line:
            continue

        # Nếu dòng bắt đầu bằng '-', thì đây là một phần tử của danh sách
        if stripped_line.startswith('-'):
            # Thêm phần tử vào danh sách hiện tại
            current_list.append(stripped_line[1:].strip())
        else:
            # Nếu danh sách hiện tại không trống, thì thêm nó vào dữ liệu YAML
            # dưới dạng giá trị của khóa hiện tại
            if current_list:
                yaml_data[current_key] = '\n'.join(current_list)
                # Đặt lại danh sách hiện tại
                current_list = []

            # Nếu dòng chứa ':', thì đây là một cặp khóa-giá trị
            if ':' in stripped_line:
                # Tách khóa và giá trị
                current_key, value = map(str.strip, stripped_line.split(':', 1))
                # Nếu giá trị không trống, thì thêm nó vào dữ liệu YAML
                # dưới dạng giá trị của khóa hiện tại
                if value:
                    yaml_data[current_key] = value

    # Nếu danh sách hiện tại không trống sau khi duyệt qua tất cả các dòng,
    # thì thêm nó vào dữ liệu YAML dưới dạng giá trị của khóa hiện tại
    if current_list:
        yaml_data[current_key] = '\n'.join(current_list)

    # Trả về dữ liệu YAML
    return yaml_data



