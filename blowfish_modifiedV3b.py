from constants import p, s, key
import time

def swap(a, b):
    return b, a

def initialize_constants():
    for i in range(18):
        p[i] ^= key[i % 14]

def generate_subkeys():
    k = 0
    data = 0
    for i in range(9):
        temp = encryption(data)
        p[k] = temp >> 32
        k += 1
        p[k] = temp & 0xFFFFFFFF
        k += 1
        data = temp

def func(XL, subkey):
    XR = XL ^ subkey
    a = (XR >> 24) & 0x03  
    b = (XR >> 16) & 0xFF

    S1 = s[a][b]
    S2 = s[(a + 1) % 4][b] 

    result = (S1 ^ S2) << 16 | (S1 + S2) & 0xFFFF

    return result

def encryption(data):
    L = data >> 32
    R = data & 0xFFFFFFFF

    for i in range(16):
        L ^= p[i]
        L1 = func(L, p[i + 1])
        R ^= L1
        L, R = swap(L, R)

    L, R = swap(L, R)
    L ^= p[17]
    R ^= p[16]

    encrypted = (L << 32) ^ R
    return encrypted

def encrypt_text(text):
    text_bytes = text.encode('utf-8')
    padding_length = (8 - len(text_bytes) % 8) % 8
    padded_text = text_bytes + bytes([padding_length] * padding_length) 

    encrypted_blocks = [encryption(int.from_bytes(padded_text[i:i+8], byteorder='big')) for i in range(0, len(padded_text), 8)]
    encrypted_data = b''.join([block.to_bytes((block.bit_length() + 7) // 8, byteorder='big') for block in encrypted_blocks])

    return encrypted_data

def decryption(data):
    L = data >> 32
    R = data & 0xFFFFFFFF

    for i in range(17, 1, -1):
        L ^= p[i]
        L1 = func(L, p[i - 1])
        R ^= L1
        L, R = swap(L, R)

    L, R = swap(L, R)
    L ^= p[0]
    R ^= p[1]

    decrypted_data = (L << 32) ^ R
    return decrypted_data

def decrypt_text(encrypted_text):
    decrypted_blocks = [decryption(int.from_bytes(encrypted_text[i:i+8], byteorder='big')) for i in range(0, len(encrypted_text), 8)]
    decrypted_data = b''.join([block.to_bytes((block.bit_length() + 7) // 8, byteorder='big') for block in decrypted_blocks])
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]
    return decrypted_data.decode('utf-8')

def driver():
    initialize_constants()
    generate_subkeys()

    encrypt_data = input("Masukkan Kalimat: ")
    start_time = time.time()

    encrypted_data = encrypt_text(encrypt_data)
    end_time = time.time()
    encryption_time_ms = (end_time - start_time) * 1000

    print("Encrypted data : ", encrypted_data.hex())
    print("Encryption Time: {:.4f} ms".format(encryption_time_ms))

    start_time = time.time()
    decrypted_data = decrypt_text(encrypted_data)
    end_time = time.time()
    decryption_time_ms = (end_time - start_time) * 1000

    print("Decrypted data : ", decrypted_data)
    print("Decryption Time: {:.4f} ms".format(decryption_time_ms))

if __name__ == "__main__":
    driver()
