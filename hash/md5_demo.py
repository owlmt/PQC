# MD5 hashing demo
import hashlib

def main():
    message = b"MD5 legacy demo"
    h = hashlib.md5(message).hexdigest()
    print("MD5 hash:", h)

if __name__ == "__main__":
    main()
