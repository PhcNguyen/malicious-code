# Encdec Detailed Guide

This Python code includes several functions for file processing.

1. **Fernet Initialization**

    ```python
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    ```

Before calling the `Encrypt` or `Decrypt` functions, you need to initialize a `Fernet` object with a secret key. `Fernet` is a secure symmetric encryption system provided by the `cryptography` library.

2. **File Encryption**

    ```python
    Encrypt(cipher_suite)
    ```

The `Encrypt` function will encrypt all files listed by the `List_Files` function. Each file will be read and encrypted in `chunks`, then written to a temporary file. Finally, the temporary file will replace the original file.

3. **File Decryption**

    ```python
    Decrypt(cipher_suite)
    ```

The Decrypt function will decrypt all files that have been encrypted by the `Encrypt` function, similar to the encryption process but in reverse.

4. **File Listing**

    ```python
    files = List_Files()
    ```

The `List_Files` function will return a list of files based on the file extensions defined in the `scripts/extensions.yaml` file. This function uses `Path.home().rglob('*')` to list all files in the user's home directory.

Note: This code should only be used for learning purposes. Using it to perform illegal activities (such as cyber attacks) can lead to serious legal consequences. Always comply with the law when using and developing open source code.

