using System.Collections.Concurrent;

namespace CipherSafe.Logging;
public class Logger
{
    private readonly bool a = true;
    private readonly string b = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs");
    private static readonly object c = new();
    private readonly ConcurrentDictionary<string, string> d;

    public Logger()
    {
        if (a) Directory.CreateDirectory(b);
        d = a ? new ConcurrentDictionary<string, string>
        {
            ["INFO"] = Path.Combine(b, "info.log"),
            ["WARNING"] = Path.Combine(b, "warning.log"),
            ["ERROR"] = Path.Combine(b, "error.log")
        } : new();
    }

    private void e(string f, string g, Exception? h = null)
    {
        if (!a) return;
        var i = $"{DateTime.Now:yy-MM-dd HH:mm:ss} - {g} - {f}" +
            (h != null ? $" - Exception: {h.Message}" : "");

        if (d.TryGetValue(g, out var j))
        {
            lock (c)
            {
                using var k = new StreamWriter(j, true);
                k.WriteLine(i);
            }
        }
    }

    public void Info(string message) => e(message, "INFO");
    public void Warning(string message) => e(message, "WARNING");
    public void Error(string message, Exception? ex = null) => e(message, "ERROR", ex);
}
