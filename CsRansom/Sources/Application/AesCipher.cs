using CipherSafe.Logging;
using System.Security.Cryptography;
using System.Text;

namespace CipherSafe.Application;
internal class AesCipher
{
    public byte[] key { get; set; }

    public AesCipher(int keySize = 256)
    {
        if (keySize != 128 && keySize != 192 && keySize != 256)
            throw new ArgumentException("Key size must be 128, 192, or 256 bits.");

        using (var rng = RandomNumberGenerator.Create())
        {
            byte[] key = new byte[keySize / 8];
            rng.GetBytes(key);
            this.key = key;
        }

    }

    /// <summary>
    /// Increments the given counter byte array. This is typically used for 
    /// encryption modes like AES CTR, where a counter is incremented 
    /// for each block of data being encrypted.
    /// </summary>
    /// <param name="counter">The byte array representing the counter to increment.</param>
    private static void IncrementCounter(byte[] counter)
    {
        Span<byte> spanCounter = counter; // Create a span from the counter array for efficient manipulation
                                          // Iterate from the last byte to the first
        for (int i = spanCounter.Length - 1; i >= 0; i--)
        {
            // Increment the current byte
            if (++spanCounter[i] != 0) break; // If the increment did not wrap around (i.e., did not become 0), exit the loop
        }
    }

    /// <summary>
    /// Encrypts data using AES in CTR mode.
    /// </summary>
    /// <param name="plaintext">The plaintext data to encrypt.</param>
    /// <param name="iv">The initialization vector (IV) for encryption.</param>
    /// <returns>The encrypted data as a byte array.</returns>
    public byte[] Encrypt(byte[] plaintext, byte[] iv)
    {
        using Aes aes = Aes.Create();
        aes.Key = this.key;
        aes.Mode = CipherMode.ECB;

        using var ms = new MemoryStream();
        ms.Write(iv, 0, iv.Length); // Write IV to the start of the encrypted data

        using var encryptor = aes.CreateEncryptor();
        byte[] counter = new byte[16];
        Array.Copy(iv, counter, iv.Length);

        for (int i = 0; i < plaintext.Length; i += aes.BlockSize / 8)
        {
            byte[] encryptedCounter = new byte[16];
            encryptor.TransformBlock(counter, 0, counter.Length, encryptedCounter, 0);

            int bytesToEncrypt = Math.Min(plaintext.Length - i, aes.BlockSize / 8);
            byte[] block = new byte[aes.BlockSize / 8];
            Array.Copy(plaintext, i, block, 0, bytesToEncrypt);

            for (int j = 0; j < bytesToEncrypt; j++)
                block[j] ^= encryptedCounter[j];

            ms.Write(block, 0, bytesToEncrypt);
            IncrementCounter(counter);
        }

        return ms.ToArray();
    }

    /// <summary>
    /// Decrypts data using AES in CTR mode.
    /// </summary>
    /// <param name="cipherText">The encrypted data to decrypt.</param>
    /// <param name="iv">The initialization vector (IV) used during encryption.</param>
    /// <returns>The decrypted data as a byte array.</returns>
    public byte[] Decrypt(byte[] cipherText, byte[] iv)
    {
        using Aes aes = Aes.Create();
        aes.Key = this.key;
        aes.Mode = CipherMode.ECB;

        using var ms = new MemoryStream(cipherText, iv.Length, cipherText.Length - iv.Length);
        using var encryptor = aes.CreateEncryptor();
        byte[] counter = new byte[16];
        Array.Copy(iv, counter, iv.Length);

        using var resultStream = new MemoryStream();
        byte[] buffer = new byte[16];
        int bytesRead;

        while ((bytesRead = ms.Read(buffer, 0, buffer.Length)) > 0)
        {
            byte[] encryptedCounter = new byte[16];
            encryptor.TransformBlock(counter, 0, counter.Length, encryptedCounter, 0);

            for (int j = 0; j < bytesRead; j++)
                buffer[j] ^= encryptedCounter[j];

            resultStream.Write(buffer, 0, bytesRead);
            IncrementCounter(counter);
        }

        return resultStream.ToArray();
    }

    /// <summary>
    /// Encrypts a file and creates a new encrypted file with a .enc extension.
    /// </summary>
    /// <param name="filePath">The path of the file to encrypt.</param>
    /// <param name="fileSize">The size of the file to encrypt.</param>
    /// <returns>True if the encryption was successful; otherwise, false.</returns>
    public bool EncryptFile(string filePath, long fileSize)
    {
        string directoryName = Path.GetDirectoryName(filePath) ?? string.Empty;
        string newFilePath = Path.Combine(directoryName, $"{Guid.NewGuid()}.enc");

        MemoryStream? memoryStream = null;
        FileStream? sourceFileStream = null;
        FileStream? newFileStream = null;

        try
        {
            memoryStream = new MemoryStream();
            sourceFileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read);

            byte[] iv = new byte[16];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(iv);
            }

            memoryStream.Write(iv, 0, iv.Length);

            byte[] fileNameBytes = Encoding.UTF8.GetBytes(Path.GetFileName(filePath));
            memoryStream.Write(BitConverter.GetBytes(fileNameBytes.Length), 0, sizeof(int));
            memoryStream.Write(fileNameBytes, 0, fileNameBytes.Length);

            byte[] buffer = new byte[Math.Min(fileSize, 8192)];
            int bytesRead;

            while (true)
            {
                try
                {
                    bytesRead = sourceFileStream.Read(buffer, 0, buffer.Length);
                    if (bytesRead <= 0) break; // Kết thúc vòng lặp nếu không còn dữ liệu để đọc

                    byte[] encryptedData = Encrypt(buffer.AsSpan(0, bytesRead).ToArray(), iv);
                    memoryStream.Write(encryptedData, 0, encryptedData.Length);
                }
                catch (IOException)
                {
                    return false; // Hoặc tiếp tục tùy vào yêu cầu của bạn
                }
            }

            newFileStream = new FileStream(newFilePath, FileMode.Create, FileAccess.Write);
            memoryStream.Position = 0;
            memoryStream.CopyTo(newFileStream);

            return true;
        }
        catch (Exception)
        {
            return false;
        }
        finally
        {
            memoryStream?.Dispose();
            sourceFileStream?.Dispose();
            newFileStream?.Dispose();

            // Xóa tệp gốc nếu quá trình mã hóa thành công
            if (File.Exists(filePath) && File.Exists(newFilePath))
            {
                File.Delete(filePath);
            }
        }
    }

    /// <summary>
    /// Decrypts an encrypted file and restores it to its original name.
    /// </summary>
    /// <param name="filePath">The path of the encrypted file to decrypt.</param>
    /// <param name="fileSize">The size of the encrypted file.</param>
    /// <returns>True if the decryption was successful; otherwise, false.</returns>
    public bool DecryptFile(string filePath, long fileSize)
    {
        string directoryName = Path.GetDirectoryName(filePath) ?? string.Empty;
        FileStream? sourceFileStream = null;
        FileStream? newFileStream = null;
        string newFilePath = string.Empty;

        try
        {
            if (!File.Exists(filePath) || fileSize <= 16 + sizeof(int))
            {
                Console.WriteLine("Invalid file or file size.");
                return false;
            }

            sourceFileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read);

            byte[] iv = new byte[16];
            if (sourceFileStream.Read(iv, 0, iv.Length) != iv.Length)
            {
                //Console.WriteLine("Error reading IV.");
                return false;
            }

            byte[] fileNameLengthBytes = new byte[sizeof(int)];
            if (sourceFileStream.Read(fileNameLengthBytes, 0, fileNameLengthBytes.Length) != fileNameLengthBytes.Length)
            {
                //Console.WriteLine("Error reading file name length.");
                return false;
            }

            int fileNameLength = BitConverter.ToInt32(fileNameLengthBytes, 0);
            byte[] originalFileNameBytes = new byte[fileNameLength];
            if (sourceFileStream.Read(originalFileNameBytes, 0, fileNameLength) != fileNameLength)
            {
                // Console.WriteLine("Error reading file name.");
                return false;
            }

            string originalFileName = Encoding.UTF8.GetString(originalFileNameBytes);
            foreach (char c in Path.GetInvalidFileNameChars())
            {
                originalFileName = originalFileName.Replace(c, '_');
            }

            newFilePath = Path.Combine(directoryName, originalFileName);
            newFileStream = new FileStream(newFilePath, FileMode.Create, FileAccess.Write);

            long bytesToRead = fileSize - iv.Length - sizeof(int) - fileNameLength;
            byte[] buffer = new byte[Math.Min(8192, bytesToRead)];
            int bytesRead;

            while (bytesToRead > 0 && (bytesRead = sourceFileStream.Read(buffer, 0, buffer.Length)) > 0)
            {
                byte[] decryptedData = Decrypt(buffer.AsSpan(0, bytesRead).ToArray(), iv);
                newFileStream.Write(decryptedData, 0, decryptedData.Length);
                bytesToRead -= bytesRead;
            }

            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            return false;
        }
        finally
        {
            sourceFileStream?.Dispose();
            newFileStream?.Dispose();

            if (File.Exists(filePath) && !string.IsNullOrEmpty(newFilePath) && File.Exists(newFilePath))
            { File.Delete(filePath); }
        }
    }
}