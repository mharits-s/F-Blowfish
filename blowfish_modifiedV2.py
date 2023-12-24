from constants import p, s, key

p_new = p.copy()

def swap(a,b):
    temp = a
    a = b
    b = temp
    return a,b

def driver():
        for i in range(0,18):
                p[i] = p[i]^key[i%14]
        k = 0
        data = 0
        for i in range(9):
            temp = encryption(data)
            p[k] = temp >> 32
            k+=1
            p[k] = temp & 0xffffffff
            k+=1
            data = temp
        encrypt_data = input("Masukkan Kalimat: ")
        encrypted_data = encrypt_text(encrypt_data)
        print("Encrypted data : ",encrypted_data.hex())
        decrypted_data = decrypt_text(encrypted_data)
        print("Decrypted data : ",decrypted_data) 

def encryption(data):
        L = data>>32
        R = data & 0xffffffff
        for i in range(16):
                L = p[i]^L
                L1 = func(L)
                R = R^func(L1)
                L,R = swap(L,R)
        L,R = swap(L,R)
        L = L^p[17]
        R = R^p[16]
        encrypted = (L<<32) ^ R
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

def func(L):
    temp = s[0][L >> 24]
    temp = (temp + s[1][L >> 16 & 0xff]) % 2**32
    temp = temp ^ s[2][L >> 8 & 0xff]
    temp = (temp + s[3][L & 0xff]) % 2**32
    return temp

def decryption(data):
    L = data >> 32
    R = data & 0xffffffff
    for i in range(17, 1, -1):
        L = p[i]^L
        L1 = func(L)
        R = R^func(L1)
        L,R = swap(L,R)
    L,R = swap(L,R)
    L = L^p[0]
    R = R^p[1]
    decrypted_data1 = (L<<32) ^ R
    return decrypted_data1

def decrypt_text(encrypted_text):
    # Proses dekripsi untuk setiap blok
    decrypted_blocks = [decryption(int.from_bytes(encrypted_text[i:i+8], byteorder='big')) for i in range(0, len(encrypted_text), 8)]

    # Menggabungkan hasil dekripsi
    decrypted_data = b''.join([block.to_bytes(8, byteorder='big') for block in decrypted_blocks])

    # Menghilangkan padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    # Konversi bytes ke string
    return decrypted_data.decode('utf-8')

driver()