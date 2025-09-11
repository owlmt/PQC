# 3DES encryption/decryption demo
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

def main():
    key = DES3.adjust_key_parity(get_random_bytes(24))
    cipher = DES3.new(key, DES3.MODE_ECB)

    message = b"3DES legacy demo"
    padded = message.ljust(24, b"\0")

    ciphertext = cipher.encrypt(padded)
    plaintext = cipher.decrypt(ciphertext).rstrip(b"\0")
    print("3DES decrypted:", plaintext.decode())

if __name__ == "__main__":
    main()
