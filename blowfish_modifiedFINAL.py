#Import Constants and time
from constants import p, s, key
import time

#Function swap
def swap(a, b):
    return b, a

#Generate Subkeys
def XOR():
    for i in range(18):
        p[i] ^= key[i % 14]

def subkeys():
    k = 0
    data = 0
    for i in range(9):
        temp = encryption(data)
        p[k] = temp >> 32
        k += 1
        p[k] = temp & 0xFFFFFFFF
        k += 1
        data = temp

#Optimized F-Function
def func(L):
    global s  
    a = (L >> 16) & 0xFF
    b = L & 0xFF

    S1 = (s[0][a] + s[1][b]) & 0xFFFFFFFF
    S2 = (s[2][a] + s[3][b]) & 0xFFFFFFFF

    result = S1 ^ S2

    return result

#Function Encryption
def encryption(data):
    L = data >> 32
    R = data & 0xFFFFFFFF

    for i in range(16):
        L ^= p[i]
        L1 = func(L)
        R ^= L1
        L, R = swap(L, R)

    L, R = swap(L, R)
    R ^= p[16]
    L ^= p[17]

    encrypted = (L << 32) ^ R
    return encrypted

#Function Encrypt Text
def encrypt_text(text):
    text_bytes = text.encode('utf-8')
    padding_length = (8 - len(text_bytes) % 8) % 8
    padded_text = text_bytes + bytes([padding_length] * padding_length) 

    encrypted_blocks = [encryption(int.from_bytes(padded_text[i:i+8], byteorder='big')) for i in range(0, len(padded_text), 8)]
    encrypted_data = b''.join([block.to_bytes((block.bit_length() + 7) // 8, byteorder='big') for block in encrypted_blocks])

    return encrypted_data

#Function Decryption
def decryption(data):
    L = data >> 32
    R = data & 0xFFFFFFFF

    for i in range(17, 1, -1):
        L ^= p[i]
        L1 = func(L)
        R ^= L1
        L, R = swap(L, R)

    L, R = swap(L, R)
    R ^= p[1]
    L ^= p[0]

    decrypted_data = (L << 32) ^ R
    return decrypted_data

#Function Decrypt Text
def decrypt_text(encrypted_text):
    decrypted_blocks = [decryption(int.from_bytes(encrypted_text[i:i+8], byteorder='big')) for i in range(0, len(encrypted_text), 8)]
    decrypted_data = b''.join([block.to_bytes((block.bit_length() + 7) // 8, byteorder='big') for block in decrypted_blocks])
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]
    return decrypted_data.decode('utf-8')

#Function Input Output
def driver():
    XOR()
    subkeys()

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

#Main
if __name__ == "__main__":
    driver()
