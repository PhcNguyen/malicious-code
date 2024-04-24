import os
import sqlite3
from typing import Dict, List

def find_paths(directory: str, keyword: str) -> Dict[str, List[str]]:
    """
    Finds files in the specified directory containing the specified keyword.

    Args:
        directory (str): The directory to search in.
        keyword (str): The keyword to search for in file paths.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are file extensions and values are lists of file paths.
    """
    paths_with_keyword: Dict[str, List[str]] = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if keyword in filepath:
                ext = os.path.splitext(filepath)[-1].lower()  # Lấy phần mở rộng của tệp
                if ext not in paths_with_keyword:
                    paths_with_keyword[ext] = []  # Tạo danh sách nếu chưa tồn tại
                paths_with_keyword[ext].append(filepath)

    return paths_with_keyword

chrome_paths = find_paths("/", "chrome")

def read_data_from_tables(db_path, table_names):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for table_name in table_names:
        print(f"Table: {table_name}")
        # Kiểm tra xem bảng tồn tại trong cơ sở dữ liệu không
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        result = cursor.fetchone()
        if result:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("")
        else:
            print(f"Table '{table_name}' does not exist in the database.")

    conn.close()


def HandleSqlite(path_list):
    for path in path_list:
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(tables)
            if tables:
                print(f"Tables in {path}:")
                for table in tables:
                    print(f" - {table[0]}")
                    # Uncomment the line below to read data from each table
                    read_data_from_tables(path, table[0])
        except sqlite3.Error as e:
            print(f"Error occurred while handling {path}: {e}")

# Sử dụng hàm HandleSqlite
HandleSqlite(chrome_paths['.sqlite'])


# Sử dụng hàm HandleSqlite
HandleSqlite(chrome_paths['.sqlite'])


