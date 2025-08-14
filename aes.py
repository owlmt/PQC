from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

# Key derivation from password
password = b"mysecretpassword"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# AES-GCM encryption
iv = os.urandom(12)
encryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv),
    backend=default_backend()
).encryptor()

plaintext = b"Confidential AES message"
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# AES-GCM decryption
decryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv, encryptor.tag),
    backend=default_backend()
).decryptor()
decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

print("AES Plaintext:", plaintext)
print("AES Ciphertext:", ciphertext.hex())
print("AES Decrypted:", decrypted_text)
