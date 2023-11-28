from itertools import chain, islice, permutations, zip_longest

from data_utils import chunked, hamming_distance

def encrypt(a: memoryview, b: memoryview) -> bytes:
    if len(a) > len(b):
        a = a[0:len(b)]
    elif len(a) < len(b):
        b = b[0:len(a)]
    return bytes(aa ^ bb for (aa, bb) in zip_longest(a, b))


class Xor:
    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, data: memoryview) -> bytes:
        encrypted_chunks = (encrypt(chunk, self._key) for chunk in chunked(data, len(self._key)))
        return bytes(chain.from_iterable(encrypted_chunks))

    def decrypt(self, data: memoryview) -> bytes:
        return self.encrypt(data)


def guess_keysize(data: memoryview, sample_size = 4) -> list[int]:
    """Guess the keysize used to encryt data, and return them in descending order"""
    guesses = []
    for n in range(1, 40):
        chunks = list(islice(chunked(data, n), sample_size))
        edit_distance_sum = 0
        for (a, b) in permutations(range(sample_size), 2):
            edit_distance_sum += hamming_distance(chunks[a], chunks[b])
        guesses.append((n, edit_distance_sum / n))
        # print(f"HD: {hd}  nHD: {hd / n}")
    
    guesses.sort(key=lambda x: x[1])
    return guesses