# RC4 stream cipher demo
from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes

def main():
    key = get_random_bytes(16)
    cipher = ARC4.new(key)
    message = b"RC4 legacy demo"

    ciphertext = cipher.encrypt(message)
    plaintext = ARC4.new(key).decrypt(ciphertext)

    print("RC4 decrypted:", plaintext.decode())

if __name__ == "__main__":
    main()
