from lib.cryptography.padding import pad, unpad
from lib.cryptography.constants import (
    IV, BLOCK, KEY, List,
    r_con, s_box
)
from lib.cryptography.util import (
    Bytes2Matrix, xor_Bytes, add_Round_Key, 
    Sub_Bytes, Shift_Rows, Mix_Columns,
    Matrix2Bytes, inv_Mix_Columns, inv_Shift_Rows, 
    inv_Sub_Bytes, Split_Blocks
)


class AesCipher:
    rounds_by_key_size = {
        16: 10, 24: 12, 32: 14
    }
    def __init__(
        self, 
        master_key: KEY
    ) -> None:
        assert len(master_key) in AesCipher.rounds_by_key_size
        self.n_rounds = AesCipher.rounds_by_key_size[len(master_key)]
        self._key_matrices = self._expand_key(master_key)

    def _expand_key(
        self, 
        master_key: KEY
    ) -> List[List[List[int]]]:
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

    def encrypt_block(
        self, 
        plaintext: BLOCK
    ) -> BLOCK:
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

    def decrypt_block(
        self, 
        ciphertext: BLOCK
    ) -> BLOCK:
       
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

    def encrypt_cbc(
        self, 
        plaintext: bytes, 
        iv: IV
    ) -> bytes:
        assert len(iv) == 16

        plaintext = pad(plaintext)

        blocks = []
        previous = iv
        for plaintext_block in Split_Blocks(plaintext):
            block = self.encrypt_block(xor_Bytes(plaintext_block, previous))
            blocks.append(block)
            previous = block

        return b''.join(blocks)

    def decrypt_cbc(
        self, 
        ciphertext: bytes, 
        iv: IV
    ) -> bytes:
        assert len(iv) == 16

        blocks = []
        previous = iv
        for ciphertext_block in Split_Blocks(ciphertext):
            blocks.append(xor_Bytes(previous, self.decrypt_block(ciphertext_block)))
            previous = ciphertext_block

        return unpad(b''.join(blocks))