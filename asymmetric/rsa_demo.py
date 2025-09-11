# RSA encryption/decryption demo
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def main():
    key = RSA.generate(2048)
    cipher = PKCS1_OAEP.new(key)
    message = b"Secret message with RSA"
    ciphertext = cipher.encrypt(message)
    plaintext = PKCS1_OAEP.new(key).decrypt(ciphertext)
    print("RSA decrypted:", plaintext.decode())

if __name__ == "__main__":
    main()
