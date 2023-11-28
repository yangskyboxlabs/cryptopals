from xorcipher import Xor

import english

ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

for k in range(255):
    key = k.to_bytes(1)
    cipher = Xor(key)
    text = cipher.decrypt(ciphertext)
    score = english.score(text)
    if score < len(text) * 0.15:
        continue
    print(f"{key} ({english.score(text)}): {text}")
