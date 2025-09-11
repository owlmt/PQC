# Simulated Diffie–Hellman key exchange using ECC
from Crypto.PublicKey import ECC

def main():
    alice = ECC.generate(curve="P-256")
    bob = ECC.generate(curve="P-256")

    shared1 = alice.pointQ * bob.d
    shared2 = bob.pointQ * alice.d

    print("DH shared secrets equal?", shared1 == shared2)

if __name__ == "__main__":
    main()
