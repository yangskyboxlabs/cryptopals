from data_utils import hamming_distance, transpose

def test_hamming_distance():
    assert hamming_distance(b'this is a test', b'wokka wokka!!!') == 37

def test_transpose():
    data = bytes.fromhex("00 01 02 03 04 05")
    transposed  = transpose(data, 3)

    assert transposed[0] == bytes.fromhex("00 03")
    assert transposed[1] == bytes.fromhex("01 04")
    assert transposed[2] == bytes.fromhex("02 05")