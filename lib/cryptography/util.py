from hashlib import pbkdf2_hmac
from typing import List, Tuple

from lib.cryptography.constants import (
    s_box, inv_s_box,
    SALT, KEY, IV,
    IV_SIZE, XTIME, BLOCK,
    AES_KEY_SIZE, HMAC_KEY_SIZE,
)


def Sub_Bytes(
        s: List[List[int]]
    ) -> None:
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


def inv_Sub_Bytes(
        s: List[List[int]]
    ) -> None:
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]


def Shift_Rows(
        s: List[List[int]]
    ) -> None:
    s[0][1], s[1][1], s[2][1], s[3][1] = (
        s[1][1], s[2][1], s[3][1], s[0][1]
    )
    s[0][2], s[1][2], s[2][2], s[3][2] = (
        s[2][2], s[3][2], s[0][2], s[1][2]
    )
    s[0][3], s[1][3], s[2][3], s[3][3] = (
        s[3][3], s[0][3], s[1][3], s[2][3]
    )


def inv_Shift_Rows(
        s: List[List[int]]
    ) -> None:
    s[0][1], s[1][1], s[2][1], s[3][1] = (
        s[3][1], s[0][1], s[1][1], s[2][1]
    )
    s[0][2], s[1][2], s[2][2], s[3][2] = (
        s[2][2], s[3][2], s[0][2], s[1][2]
    )
    s[0][3], s[1][3], s[2][3], s[3][3] = (
        s[1][3], s[2][3], s[3][3], s[0][3]
    )


def add_Round_Key(
        s: List[List[int]], 
        k: List[List[int]]
    ) -> None:
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def Mix_Single_Column(
        a: List[int]
    ) -> None:
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    a[0] ^= t ^ XTIME(a[0] ^ a[1])
    a[1] ^= t ^ XTIME(a[1] ^ a[2])
    a[2] ^= t ^ XTIME(a[2] ^ a[3])
    a[3] ^= t ^ XTIME(a[3] ^ a[0])


def Mix_Columns(
        s: List[List[int]]
    ) -> None:
    for i in range(4):
        Mix_Single_Column(s[i])


def inv_Mix_Columns(
        s: List[List[int]]
    ) -> None:
    for i in range(4):
        u = XTIME(XTIME(s[i][0] ^ s[i][2]))
        v = XTIME(XTIME(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    Mix_Columns(s)


def Bytes2Matrix(
        text: bytes
    ) -> List[List[int]]:
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]


def Matrix2Bytes(
        matrix: List[List[int]]
    ) -> bytes:
    return bytes(sum(matrix, []))


def xor_Bytes(
        a: bytes, 
        b: bytes
    ) -> bytes:
    return bytes(i^j for i, j in zip(a, b))


def inc_Bytes(a: bytes) -> bytes:
    out = list(a)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)


def Split_Blocks(
        message: bytes, 
        block_size: int = 16, 
        require_padding: bool = True
    ) -> List[BLOCK]:
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]


def GET_KEY_IV(
        password: bytes, 
        salt: SALT
    ) -> Tuple[KEY, KEY, IV]:
    
    stretched = pbkdf2_hmac('sha256', password, salt, 100000, AES_KEY_SIZE + IV_SIZE + HMAC_KEY_SIZE)
    aes_key, stretched = stretched[:AES_KEY_SIZE], stretched[AES_KEY_SIZE:]
    hmac_key, stretched = stretched[:HMAC_KEY_SIZE], stretched[HMAC_KEY_SIZE:]
    iv = stretched[:IV_SIZE]
    return aes_key, hmac_key, iv