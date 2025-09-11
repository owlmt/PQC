# AES-128 encryption/decryption demo
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def main():
    key = get_random_bytes(16)  # 128-bit
    cipher = AES.new(key, AES.MODE_EAX)
    message = b"AES-128 legacy demo"
    ciphertext, tag = cipher.encrypt_and_digest(message)

    decipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
    plaintext = decipher.decrypt(ciphertext)
    print("AES-128 decrypted:", plaintext.decode())

if __name__ == "__main__":
    main()
