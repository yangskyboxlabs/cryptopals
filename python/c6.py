import base64

from data_utils import transpose
import english
from xorcipher import guess_keysize, Xor

with open("../6.txt", 'rt') as f:
    text = ''.join(f.readlines())
    data = base64.b64decode(text)

# print(data[:40].hex(' '))

key_sizes = guess_keysize(data)[:5]

print("Key size guesses:")
for (keysize, normalized_edit_dist) in key_sizes:
    print(f"{keysize} ({normalized_edit_dist})")

key_sizes = [key_size for (key_size, _) in key_sizes]

print("=========================")
print("Guessing key bytes...")

full_key = b''
# for keysize in (5, 3, 2, 13, 11, 9, 10):
# for keysize in range(20, 50):
for keysize in key_sizes:
    transposed_blocks = transpose(data, keysize)

    has_key = False
    key = bytearray(keysize)
    for block_idx, block in enumerate(transposed_blocks):
        # print(f"block: {block_idx}")
        byte_key = b'\0'
        byte_key_score = 0
        for k in range(255):
            key_guess = k.to_bytes(1)
            cipher = Xor(key_guess)
            text = cipher.decrypt(block)
            score = english.score(text)
            if score > 1:
                has_key = True
                print(f"{keysize=} {block_idx=}: {key_guess} ({english.score(text)}): {text}")
                if score > byte_key_score:
                    byte_key = key_guess
                    byte_key_score = score
        key[block_idx] = int.from_bytes(byte_key)

    if has_key:
        print(f"{keysize=}: KEY {key}")
        full_key = bytes(key)
    else:
        print(f"{keysize=}: NO KEY")

print("=========================")

if full_key:
    print(f"USING KEY: {full_key}")
    print("---------")

    cipher = Xor(full_key)
    plaintext = cipher.decrypt(data)
    print(plaintext)