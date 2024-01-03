import os

from constants import p, s, key

def swap(a, b):
    return b, a

def func(L):
    global s  
    a = (L >> 16) & 0xFF
    b = L & 0xFF

    S1 = (s[0][a] + s[1][b]) & 0xFFFFFFFF
    S2 = (s[2][a] + s[3][b]) & 0xFFFFFFFF

    result = S1 ^ S2

    return result

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

def encrypt_text(text):
    # Padding the input text and encrypting each block
    if isinstance(text, str):
        text_bytes = text.encode('utf-8')
    elif isinstance(text, bytes):
        text_bytes = text
    else:
        raise ValueError("Unsupported input type. Please provide a string or bytes.")
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
        L1 = func(L)
        R ^= L1
        L, R = swap(L, R)

    L, R = swap(L, R)
    R ^= p[1]
    L ^= p[0]

    decrypted_data = (L << 32) ^ R
    return decrypted_data

def decrypt_text(encrypted_text):
    decrypted_blocks = [decryption(int.from_bytes(encrypted_text[i:i+8], byteorder='big')) for i in range(0, len(encrypted_text), 8)]
    decrypted_data = b''.join([block.to_bytes((block.bit_length() + 7) // 8, byteorder='big') for block in decrypted_blocks])
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]
    return decrypted_data.decode('utf-8')

def encrypt_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = encrypt_text(file_data)

    with open(output_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = decrypt_text(encrypted_data)

    # Convert the decrypted string to bytes
    decrypted_data_bytes = decrypted_data.encode('utf-8')

    with open(output_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data_bytes)


def driver():
    input_file_path = "test.txt"
    encrypted_output_path = "OutputV4/encrypted_file.bin"
    decrypted_output_path = "OutputV4/decrypted_file.txt"

    # Key schedule initialization
    for i in range(18):
        p[i] ^= key[i % 14]

    # Generate subkeys
    k = 0
    data = 0
    for i in range(9):
        temp = encryption(data)
        p[k] = temp >> 32
        k += 1
        p[k] = temp & 0xFFFFFFFF
        k += 1
        data = temp

    # Encrypt file
    encrypt_file(input_file_path, encrypted_output_path)
    print(f"File '{input_file_path}' encrypted and saved to '{encrypted_output_path}'")

    # Decrypt file
    decrypt_file(encrypted_output_path, decrypted_output_path)
    print(f"File '{encrypted_output_path}' decrypted and saved to '{decrypted_output_path}'")

if __name__ == "__main__":
    # Create the OutputV4 directory if it doesn't exist
    output_directory = "OutputV4"
    os.makedirs(output_directory, exist_ok=True)

    driver()
