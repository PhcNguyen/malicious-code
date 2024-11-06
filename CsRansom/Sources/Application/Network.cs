namespace CipherSafe.Application;
class NetworkClient
{
    private readonly System.Net.Sockets.TcpClient c = new() { NoDelay = true };
    private System.Net.Sockets.NetworkStream? s;
    private readonly string h = Config.Host;
    private readonly int p = Config.Port;
    public bool Connect() { try { c.Connect(h, p); return (s = c.GetStream()) != null; } catch { return false; } }
    public bool Send(string m) => Send(System.Text.Encoding.UTF8.GetBytes(m));
    public bool Send(byte[] d) => s != null && c.Connected && TrySend(d);
    private bool TrySend(byte[] d) { try { s?.Write(d, 0, d.Length); return true; }  catch { return false; } }
    public bool Disconnect() { try { s?.Close(); c.Close(); return true; } catch { return false; } }
}