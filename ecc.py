from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Generate ECC key pairs (ECDH)
private_key_A = ec.generate_private_key(ec.SECP256R1())
private_key_B = ec.generate_private_key(ec.SECP256R1())

# Shared secret derivation
shared_secret_A = private_key_A.exchange(ec.ECDH(), private_key_B.public_key())
shared_secret_B = private_key_B.exchange(ec.ECDH(), private_key_A.public_key())

# Derive AES key from shared secret
def derive_key(shared_secret):
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake data",
    ).derive(shared_secret)

key_A = derive_key(shared_secret_A)
key_B = derive_key(shared_secret_B)

# AES-GCM Encryption with ECC-derived key
iv = os.urandom(12)
encryptor = Cipher(
    algorithms.AES(key_A),
    modes.GCM(iv)
).encryptor()

plaintext = b"Confidential ECC message"
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# AES-GCM Decryption with ECC-derived key
decryptor = Cipher(
    algorithms.AES(key_B),
    modes.GCM(iv, encryptor.tag)
).decryptor()
decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

print("ECC Plaintext:", plaintext)
print("ECC Ciphertext:", ciphertext.hex())
print("ECC Decrypted:", decrypted_text)
