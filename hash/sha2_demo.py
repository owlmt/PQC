# SHA-256 hashing demo
import hashlib

def main():
    message = b"SHA-2 legacy demo"
    h = hashlib.sha256(message).hexdigest()
    print("SHA-256 hash:", h)

if __name__ == "__main__":
    main()
