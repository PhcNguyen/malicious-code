namespace CipherSafe.Application;
internal class ProgressBar
{
    public static void drawText(int progress, int total)
    {
        Console.CursorLeft = 0;
        Console.Write("["); //start
        Console.CursorLeft = 32;
        Console.Write("]"); //end
        Console.CursorLeft = 1;
        float onechunk = 30.0f / total;

        //draw filled part
        int position = 1;
        for (int i = 0; i < onechunk * progress; i++)
        {
            Console.BackgroundColor = ConsoleColor.Gray;
            Console.CursorLeft = position++;
            Console.Write(" ");
        }

        //draw unfilled part
        for (int i = position; i <= 31; i++)
        {
            Console.BackgroundColor = ConsoleColor.Green;
            Console.CursorLeft = position++;
            Console.Write(" ");
        }

        // Calculate percentage progress
        float percentage = (float)progress / total * 100;

        // Draw totals with fixed width for progress, total, and percentage
        Console.CursorLeft = 35;
        Console.BackgroundColor = ConsoleColor.Black;

        // Ensuring that progress, total, and percentage have fixed width (6 characters)
        Console.Write(progress.ToString().PadLeft(6) + "/" + total.ToString().PadRight(6) + " - " + percentage.ToString("0.00") + "%    ");
    }

    public static void Ciz(int sol, int ust, int deger, int isaret, ConsoleColor color)
    {
        char[] symbol = new char[5] { '\u25A0', '\u2592', '\u2588', '\u2551', '\u2502' };

        int maxBarSize = Console.BufferWidth - 1;
        int barSize = deger;
        decimal f = 1;
        if (barSize + sol > maxBarSize)
        {
            barSize = maxBarSize - (sol + 5);
            f = (decimal)deger / (decimal)barSize;
        }
        Console.CursorVisible = false;
        Console.ForegroundColor = color;
        Console.SetCursorPosition(sol + 5, ust);

        for (int i = 0; i < barSize + 1; i++)
        {
            System.Threading.Thread.Sleep(10);
            Console.Write(symbol[isaret]);
            Console.SetCursorPosition(sol, ust);
            Console.Write("%" + (i * f).ToString("0,0"));
            Console.SetCursorPosition(sol + 5 + i, ust);
        }
        Console.ResetColor();
    }

}