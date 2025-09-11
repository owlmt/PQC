# Blowfish encryption/decryption demo
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes

def main():
    key = get_random_bytes(16)
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)

    message = b"Blowfish legacy demo"
    padded = message.ljust(16, b"\0")

    ciphertext = cipher.encrypt(padded)
    plaintext = cipher.decrypt(ciphertext).rstrip(b"\0")

    print("Blowfish decrypted:", plaintext.decode())

if __name__ == "__main__":
    main()
