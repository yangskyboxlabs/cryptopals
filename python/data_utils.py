from collections.abc import Iterable
import sys

type ChunkedBytes = Iterable[memoryview]
type freqmap = dict[bytes, int]

def chunked(data: memoryview, n: int) -> ChunkedBytes:
    for i in range(0, len(data), n):
        yield data[i:i+n]

def get_frequency_map(s: memoryview) -> dict[bytes, int]:
    map = dict()
    for c in s:
        try:
            map[c] += 1
        except KeyError:
            map[c] = 1
    map = dict((k.to_bytes(1), v) for (k, v) in sorted(map.items(), key=lambda x: x[1], reverse=True))
    return map

def hamming_distance(a: bytes, b: bytes) -> int:
    return sum((aa ^ bb).bit_count() for (aa, bb) in zip(a, b))

def transpose(data: memoryview, n: int) -> ChunkedBytes:
    blocks = list(chunked(data, n))

    # If final block is not same as rest, ignore it
    if len(blocks[-1]) != n:
        blocks.pop()

    transposed_blocks = []
    for i in range(n):
        block = bytes(b[i] for b in blocks)
        transposed_blocks.append(block)

    return transposed_blocks


if __name__ == '__main__':
    for line in sys.stdin:
        line = line.rstrip()
        print(f"IN: {line}")
        ciphertext = bytes.fromhex(line)
        freq_map = get_frequency_map(ciphertext)

        for k, v in freq_map.items():
            print(f"  {k} ({k.hex()}): {v}")