#!/usr/bin/env python3
"""
ML-KEM KEM using liboqs-python.
API:
  - generate_keypair() -> (sk_bytes, pk_bytes)
  - encapsulate(peer_pk_bytes: bytes, info: bytes = b"") -> (ciphertext: bytes, shared_key: bytes)
  - decapsulate(ciphertext: bytes, sk_bytes: bytes, info: bytes = b"") -> shared_key: bytes
"""

from typing import Tuple
from dataclasses import dataclass
import oqs
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

KEY_LEN = 32  # derive to 32 bytes for AEAD compatibility
KDF_LABEL = b"ML-KEM-HKDF-SHA256"

ALG = "ML-KEM-768"  # options: ML-KEM-512, ML-KEM-768, ML-KEM-1024

def _hkdf(ss: bytes, info: bytes = b"") -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=KEY_LEN, salt=None, info=KDF_LABEL + info)
    return hkdf.derive(ss)

@dataclass
class MLKEM_KEM:
    @staticmethod
    def generate_keypair() -> Tuple[bytes, bytes]:
        with oqs.KeyEncapsulation(ALG) as kem:
            pk, sk = kem.generate_keypair()
            return sk, pk

    @staticmethod
    def encapsulate(peer_pk_bytes: bytes, info: bytes = b"") -> Tuple[bytes, bytes]:
        with oqs.KeyEncapsulation(ALG) as kem:
            ct, ss = kem.encap_secret(peer_pk_bytes)
            # Optional HKDF to unify length across algorithms
            return ct, _hkdf(ss, info)

    @staticmethod
    def decapsulate(ciphertext: bytes, sk_bytes: bytes, info: bytes = b"") -> bytes:
        with oqs.KeyEncapsulation(ALG) as kem:
            ss = kem.decap_secret(ciphertext, sk_bytes)
            return _hkdf(ss, info)


# Example usage compatible with your previous AEAD helpers
if __name__ == "__main__":
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import os

    def aead_encrypt(key: bytes, pt: bytes, aad: bytes = b""):
        nonce = os.urandom(12)
        ct = AESGCM(key).encrypt(nonce, pt, aad)
        return nonce, ct

    def aead_decrypt(key: bytes, nonce: bytes, ct: bytes, aad: bytes = b""):
        return AESGCM(key).decrypt(nonce, ct, aad)

    # Alice static keypair
    alice_sk, alice_pk = MLKEM_KEM.generate_keypair()

    # Bob encapsulates to Alice
    ct, bob_key = MLKEM_KEM.encapsulate(alice_pk, info=b"demo-context")

    # Alice decapsulates
    alice_key = MLKEM_KEM.decapsulate(ct, alice_sk, info=b"demo-context")
    assert bob_key == alice_key

    # Use the shared key
    msg = b"Hello from ML-KEM"
    nonce, c = aead_encrypt(alice_key, msg, aad=b"hdr")
    print("OK, ML-KEM established a 32-byte key and encrypted a message.")
    print("Ciphertext bytes:", len(c))
    print("Plaintext:", aead_decrypt(alice_key, nonce, c, aad=b"hdr"))
