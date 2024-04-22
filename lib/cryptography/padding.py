def pad(
        plaintext: bytes
    ) -> bytes:
    """
    Pads the input plaintext to a multiple of 16 bytes.

    Args:
        plaintext (bytes): The original plaintext.

    Returns:
        bytes: The padded plaintext.
    """
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(
        plaintext: bytes
    ) -> bytes:
    """
    Removes padding from the input plaintext.

    Args:
        plaintext (bytes): The padded plaintext.

    Returns:
        bytes: The original plaintext.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message