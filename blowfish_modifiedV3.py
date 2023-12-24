from constants import p, s, key

# Initialize the P-array and four S-boxes with a fixed string
p_new = p.copy()

def swap(a, b):
    temp = a
    a = b
    b = temp
    return a, b

def driver():
    # Encrypt the key and P-array to prepare the sub keys
    generate_subkeys()

    encrypt_data = input("Masukkan Kalimat: ")
    encrypted_data = encrypt_text(encrypt_data)
    print("Encrypted data : ", encrypted_data.hex())

    decrypted_data = decrypt_text(encrypted_data)
    print("Decrypted data : ", decrypted_data)

def generate_subkeys():
    # Encrypt the P-array values using the F function with four S-boxes
    for i in range(0, 18):
        p[i] = p[i] ^ key[i % 14]

    k = 0
    data = 0

    for i in range(9):
        temp = encryption(data)
        p[k] = temp >> 32
        k += 1
        p[k] = temp & 0xffffffff
        k += 1
        data = temp

def encryption(data):
    L = data >> 32
    R = data & 0xffffffff

    for i in range(16):
        L = L ^ p[i]
        L1, R1 = func(L, R)
        L = R
        R = L1 ^ R1

    L, R = swap(L, R)
    L = L ^ p[17]
    R = R ^ p[16]

    encrypted = (L << 32) ^ R
    return encrypted

def encrypt_text(text):
    # Konversi teks ke bytes
    text_bytes = text.encode('utf-8')
    # Padding jika panjang tidak kelipatan 8
    padding_length = (8 - len(text_bytes) % 8) % 8
    padded_text = text_bytes + bytes([padding_length]) * padding_length

    # Proses enkripsi untuk setiap blok
    encrypted_blocks = [encryption(int.from_bytes(padded_text[i:i+8], byteorder='big')) for i in range(0, len(padded_text), 8)]

    # Menggabungkan hasil enkripsi
    encrypted_data = b''.join([block.to_bytes(8, byteorder='big') for block in encrypted_blocks])
    return encrypted_data

def func(L, R):
    # Divide XR into two 16-bit halves: a, and b
    a = R >> 16
    b = R & 0xffff

    # The optimized F function: F(XL) = F(a, b) = (S1 ♁ S2)
    temp = (s[0][a >> 8] ^ s[1][a & 0xff]) ^ s[2][b >> 8] ^ s[3][b & 0xff]

    return temp, L ^ temp

def decryption(data):
    L = data >> 32
    R = data & 0xffffffff

    L = L ^ p[17]
    R = R ^ p[16]

    L, R = swap(L, R)

    for i in range(15, -1, -1):  
        L1, R1 = func(L, R)
        R = L
        L = L1 ^ p[i] 

    decrypted_data1 = (L << 32) ^ R
    return decrypted_data1

def decrypt_text(encrypted_text):
    # Process decryption for each block
    decrypted_blocks = [decryption(int.from_bytes(encrypted_text[i:i + 8], byteorder='big')) for i in
                        range(0, len(encrypted_text), 8)]

    # Combine the decryption results
    decrypted_data = b''.join([block.to_bytes(8, byteorder='big') for block in decrypted_blocks])

    # Remove padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    # Convert bytes to string
    return decrypted_data.decode('utf-8')

driver()
