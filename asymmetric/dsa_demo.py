# DSA signing/verification demo
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def main():
    key = DSA.generate(1024)
    message = b"DSA signature demo"
    h = SHA256.new(message)

    signer = DSS.new(key, "fips-186-3")
    signature = signer.sign(h)

    verifier = DSS.new(key.publickey(), "fips-186-3")
    try:
        verifier.verify(h, signature)
        print("DSA signature verified")
    except ValueError:
        print("DSA verification failed")

if __name__ == "__main__":
    main()
