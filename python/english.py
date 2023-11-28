import string
from itertools import islice

def score(text: memoryview) -> int:
    freq_map = dict()
    printable = bytes(string.printable, 'ascii')

    score = 0
    for c in text:
        if c not in printable:
            return 0

        if bytes.isalnum(c.to_bytes(1)) or (c in b" '.,!\n"):
            score += 1

        try:
            freq_map[c] += 1
        except KeyError:
            freq_map[c] = 1
    freq_map = dict((k.to_bytes(1), v) for (k, v) in sorted(freq_map.items(), key=lambda x: x[1], reverse=True))

    # bonus points if 6 most frequent characters are vowels or space
    for (c, freq) in islice(freq_map.items(), 6):
        if c in b'aeiouAEIOU ':
            score += freq

    return score - len(text)