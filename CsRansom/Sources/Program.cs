using CipherSafe.Application;
using CipherSafe.Logging;
using System.Diagnostics;

namespace CipherSafe;
class Program
{
    static async Task Main()
    {
        Logger logger = new Logger();
        var fileExplorer = new FileExplorer();
        Console.WriteLine("Enc: 1. Dec: 2");

        while (true)
        {
            if (int.TryParse(Console.ReadLine(), out int selection))
            {
                if (selection == 1)
                {
                    var stopwatch = Stopwatch.StartNew();
                    fileExplorer.Scan(1024 * 1024, FileExplorer.SortOrder.Descending);
                    stopwatch.Stop();

                    Console.WriteLine($"Scan completed in {stopwatch.Elapsed.TotalSeconds:F2} seconds");
                    Console.WriteLine($"Files found: {fileExplorer.filteredFiles.Count}");
                    if (fileExplorer.filteredFiles.Count == 0) return;

                    Console.WriteLine("Start Encrypt");
                    fileExplorer.EncryptFilesMultiple();

                    Console.WriteLine("key: " + Convert.ToBase64String(fileExplorer.aesCipher.key));
                    logger.Info(Convert.ToBase64String(fileExplorer.aesCipher.key));

                    Console.ReadLine();
                    return;
                }
                else if (selection == 2)
                {
                    var stopwatch = Stopwatch.StartNew();
                    fileExplorer.Scan(1024 * 1024, FileExplorer.SortOrder.Descending, fileType: ".dec");
                    stopwatch.Stop();

                    Console.WriteLine($"Scan completed in {stopwatch.Elapsed.TotalSeconds:F2} seconds");
                    Console.WriteLine($"Files found: {fileExplorer.filteredFiles.Count}");
                    if (fileExplorer.filteredFiles.Count == 0) return;

                    Console.WriteLine("Please enter the key in Base64 format:");
                    string? inputKey = Console.ReadLine();

                    if (inputKey == null)
                    {
                        Console.WriteLine("Invalid key input. Exiting.");

                        Console.ReadLine();
                        return;
                    }

                    byte[] keyBytes;
                    try
                    {
                        keyBytes = Convert.FromBase64String(inputKey);
                    }
                    catch (FormatException)
                    {
                        Console.WriteLine("Invalid base64 input. Exiting.");
                        return;
                    }

                    fileExplorer.aesCipher.key = keyBytes;
                    Console.WriteLine("Start Decrypt");

                    fileExplorer.DecryptFilesMultiple();

                    Console.ReadLine();
                    return;
                }
                else
                {
                    Console.WriteLine("Invalid choice.");
                }
                break;
            }
            else
            {
                Console.WriteLine("Invalid input. Please enter a number.");
                await Task.Delay(5000);
            }
        }
    }
}