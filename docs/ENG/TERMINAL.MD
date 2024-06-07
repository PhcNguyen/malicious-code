## Terminal - Col

1. **Terminal Class**:
 - This class contains methods for interacting with the system. It includes methods for clearing the console, setting the console size, restarting the program, and executing system commands.
```
    1 variable:
        Windows    |     Indicates whether the user is using the Windows operating system or not
    7 functions:
        Init()     |     Initializes the terminal to enable color usage
        Clear()    |     Clears the terminal
        Title()    |     Sets the title of the terminal, only applicable for Windows
        Size()     |     Sets the size of the terminal, only applicable for Windows
        Reset()    |     Restarts the current program
        Command()  |     Executes a shell command on the computer's system
```
 ---
2. **Col Class**:
 - This class provides a method for creating ANSI color codes. It contains predefined ANSI color codes for easy use.
 ---

```python
    # Initialize the system
    from lib.modules import Terminal, Col

    Terminal.Init()

    # Clear the console
    Terminal.Clear()

    # Set console size
    Terminal().Size(80, 24)

    # Print a message to the console
    Terminal.Console("127.0.0.1", "Hello, World!", "Green")

    # Define the color black (RGB)
    Black = Col.start('0;0;0')
    print(f"{Col.Red} I AM RED {Col.White}")
```