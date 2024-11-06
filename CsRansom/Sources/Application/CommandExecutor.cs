using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace CipherSafe.Application;
public static class CommandExecutor
{
    // Importing user32.dll functions
    [DllImport("user32.dll")]
    private static extern int FindWindow(string lpClassName, string lpWindowName);

    [DllImport("user32.dll")]
    private static extern bool ShowWindow(int hWnd, int nCmdShow);

    private const int SW_HIDE = 0; // Hide the window
    private const int SW_SHOW = 5; // Show the window

    private static void HideConsoleWindow()
    {
        // Get the console window handle
        int consoleWindow = FindWindow(null, Console.Title);
        if (consoleWindow != 0) // If the handle is valid
        {
            ShowWindow(consoleWindow, SW_HIDE); // Hide the console window
        }
    }

    private static string GetFileName() =>
        Environment.OSVersion.Platform == PlatformID.Win32NT ? "cmd.exe" : "/bin/bash";

    private static string GetArguments(string command) =>
        Environment.OSVersion.Platform == PlatformID.Win32NT ? $"/C {command}" : $"-c \"{command}\"";

    public static string Command(string command)
    {
        HideConsoleWindow(); // Hide the console window when executing commands

        // Initialize the process
        Process process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = GetFileName(),
                Arguments = GetArguments(command),
                RedirectStandardOutput = true, // Redirect standard output
                RedirectStandardError = true,  // Redirect standard error
                UseShellExecute = false,       // Don't use shell to execute
                CreateNoWindow = true          // Do not create a window
            }
        };

        process.Start(); // Start the process
        string result = process.StandardOutput.ReadToEnd(); // Read the output
        string error = process.StandardError.ReadToEnd(); // Read any errors
        process.WaitForExit(); // Wait for the process to exit

        // Check for errors and throw an exception if any
        if (!string.IsNullOrEmpty(error))
        {
            throw new Exception($"Command error: {error}");
        }

        return result.Trim(); // Return the result with trimmed whitespace
    }

    public static string HardwareInfo()
    {
        string biosSerial = string.Empty;
        string cpuId = string.Empty;
        string diskSerial = string.Empty;
        string motherboardSerial = string.Empty;

        if (Environment.OSVersion.Platform == PlatformID.Win32NT)
        {
            // Windows commands
            biosSerial = Command("wmic bios get serialnumber | findstr /C:\"SerialNumber\"");
            cpuId = Command("wmic cpu get processorid | findstr /C:\"ProcessorId\"");
            diskSerial = Command("wmic diskdrive get serialnumber | findstr /C:\"SerialNumber\"");
            motherboardSerial = Command("wmic baseboard get serialnumber | findstr /C:\"SerialNumber\"");
        }
        else if (Environment.OSVersion.Platform == PlatformID.Unix)
        {
            // Linux / macOS commands
            biosSerial = Command("sudo dmidecode -s bios-version"); // BIOS version (requires sudo)
            cpuId = Command("cat /proc/cpuinfo | grep 'model name' | uniq"); // CPU model name
            diskSerial = Command("lsblk -o NAME,SERIAL | grep '^sd'"); // Disk serial numbers
            motherboardSerial = Command("sudo dmidecode -s baseboard-serial-number"); // Motherboard serial (requires sudo)
        }

        // Combine the hardware information into a single string
        var hardwareInfos = new[] { biosSerial, cpuId, diskSerial, motherboardSerial };
        return string.Join('|', hardwareInfos);
    }
}