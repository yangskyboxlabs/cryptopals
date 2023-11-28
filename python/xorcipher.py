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


def guess_keysize(data: memoryview, max_keysize = 40, chunk_samples = 4) -> list[int]:
    """Guess the keysize used to encryt data, and return them in descending order"""
    guesses = []
    for keysize in range(1, max_keysize):
        chunks = list(islice(chunked(data, keysize), chunk_samples))
        edit_distance_sum = 0
        sample_count = 0
        for (a, b) in permutations(range(chunk_samples), 2):
            edit_distance_sum += hamming_distance(chunks[a], chunks[b])
            sample_count += 1
        normalized_edit_distance = edit_distance_sum / keysize / sample_count
        guesses.append((keysize, normalized_edit_distance))
    
    guesses.sort(key=lambda x: x[1])
    return guesses