# SHA-1 hashing demo
import hashlib

def main():
    message = b"SHA-1 legacy demo"
    h = hashlib.sha1(message).hexdigest()
    print("SHA-1 hash:", h)

if __name__ == "__main__":
    main()
