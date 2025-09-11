# ECC signing/verification demo
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def main():
    key = ECC.generate(curve="P-256")
    message = b"ECC signature demo"
    h = SHA256.new(message)

    signer = DSS.new(key, "fips-186-3")
    signature = signer.sign(h)

    verifier = DSS.new(key.public_key(), "fips-186-3")
    try:
        verifier.verify(h, signature)
        print("ECC signature verified")
    except ValueError:
        print("ECC verification failed")

if __name__ == "__main__":
    main()
