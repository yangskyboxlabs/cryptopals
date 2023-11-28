from xorcipher import Xor

def test_encrypt_with_equal_len():
    a = bytes.fromhex('1c0111001f010100061a024b53535009181c')
    b = bytes.fromhex('686974207468652062756c6c277320657965')

    cipher = Xor(b)
    r = cipher.encrypt(a)

    assert r == bytes.fromhex('746865206b696420646f6e277420706c6179')

def test_encrypt_single_byte():
    data = bytes.fromhex('00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff')
    cipher = Xor(bytes.fromhex('01'))

    r = cipher.encrypt(data)

    assert r == bytes.fromhex('01 10 23 32 45 54 67 76 89 98 ab ba cd dc ef fe')


def test_encrypt_repeatingkey():
    cipher = Xor(b'ICE')

    stanza = b"Burning 'em, if you ain't quick and nimble\n" \
             b"I go crazy when I hear a cymbal"

    assert cipher.encrypt(stanza) \
        == bytes.fromhex(
                "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
                "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
            )