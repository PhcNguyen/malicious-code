from lib.cryptography.padding import pad, unpad
from hashlib import pbkdf2_hmac
from lib.cryptography.util import *


def Sub_Bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


def inv_Sub_Bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]


def Shift_Rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_Shift_Rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def add_Round_Key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def Mix_Single_Column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def Mix_Columns(s):
    for i in range(4):
        Mix_Single_Column(s[i])


def inv_Mix_Columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    Mix_Columns(s)


def Bytes2Matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]


def Matrix2Bytes(matrix):
    return bytes(sum(matrix, []))


def xor_Bytes(a, b):
    return bytes(i^j for i, j in zip(a, b))


def inc_Bytes(a):
    out = list(a)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)


def Split_Blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]


class AESCipher:
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}
    def __init__(self, master_key):
        assert len(master_key) in AESCipher.rounds_by_key_size
        self.n_rounds = AESCipher.rounds_by_key_size[len(master_key)]
        self._key_matrices = self._expand_key(master_key)

    def _expand_key(self, master_key):
        key_columns = Bytes2Matrix(master_key)
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            word = list(key_columns[-1])

            if len(key_columns) % iteration_size == 0:
                word.append(word.pop(0))
                word = [s_box[b] for b in word]
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                word = [s_box[b] for b in word]

            word = xor_Bytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

    def encrypt_block(self, plaintext):
        assert len(plaintext) == 16

        plain_state = Bytes2Matrix(plaintext)

        add_Round_Key(plain_state, self._key_matrices[0])

        for i in range(1, self.n_rounds):
            Sub_Bytes(plain_state)
            Shift_Rows(plain_state)
            Mix_Columns(plain_state)
            add_Round_Key(plain_state, self._key_matrices[i])

        Sub_Bytes(plain_state)
        Shift_Rows(plain_state)
        add_Round_Key(plain_state, self._key_matrices[-1])

        return Matrix2Bytes(plain_state)

    def decrypt_block(self, ciphertext):
        assert len(ciphertext) == 16

        cipher_state = Bytes2Matrix(ciphertext)

        add_Round_Key(cipher_state, self._key_matrices[-1])
        inv_Shift_Rows(cipher_state)
        inv_Sub_Bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            add_Round_Key(cipher_state, self._key_matrices[i])
            inv_Mix_Columns(cipher_state)
            inv_Shift_Rows(cipher_state)
            inv_Sub_Bytes(cipher_state)

        add_Round_Key(cipher_state, self._key_matrices[0])

        return Matrix2Bytes(cipher_state)

    def encrypt_cbc(self, plaintext, iv):
        assert len(iv) == 16

        plaintext = pad(plaintext)

        blocks = []
        previous = iv
        for plaintext_block in Split_Blocks(plaintext):
            block = self.encrypt_block(xor_Bytes(plaintext_block, previous))
            blocks.append(block)
            previous = block

        return b''.join(blocks)

    def decrypt_cbc(self, ciphertext, iv):
        assert len(iv) == 16

        blocks = []
        previous = iv
        for ciphertext_block in Split_Blocks(ciphertext):
            blocks.append(xor_Bytes(previous, self.decrypt_block(ciphertext_block)))
            previous = ciphertext_block

        return unpad(b''.join(blocks))


def get_key_iv(password, salt):
    stretched = pbkdf2_hmac('sha256', password, salt, 100000, AES_KEY_SIZE + IV_SIZE + HMAC_KEY_SIZE)
    aes_key, stretched = stretched[:AES_KEY_SIZE], stretched[AES_KEY_SIZE:]
    hmac_key, stretched = stretched[:HMAC_KEY_SIZE], stretched[HMAC_KEY_SIZE:]
    iv = stretched[:IV_SIZE]
    return aes_key, hmac_key, iv