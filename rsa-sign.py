from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# 1. Generate RSA key pair
key = RSA.generate(2048)  # 2048-bit RSA key
private_key = key
public_key = key.publickey()

# 2. Message to be signed
message = b"PostQ and CADI automate PQC migration."

# 3. Hash the message
hash_obj = SHA256.new(message)

# 4. Sign the message with the private key
signature = pkcs1_15.new(private_key).sign(hash_obj)
print("Signature (hex):", signature.hex())

# 5. Verify the signature with the public key
try:
    pkcs1_15.new(public_key).verify(hash_obj, signature)
    print("Signature is valid ✅")
except (ValueError, TypeError):
    print("Signature is invalid ❌")
