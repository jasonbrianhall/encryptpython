import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import getopt
import getpass

# Encrypt the script
def encrypt_script(file_name, password):
    # Read the file
    with open(file_name, 'rb') as f:
        data = f.read()
    # Derive a key from the password
    password = password.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    # Encrypt the data
    encrypted_data = f.encrypt(data)
    # Write the encrypted data to a new file
    with open(file_name, 'wb') as f:
        f.write(encrypted_data)

# Decrypt and run the script
def run_encrypted_script(file_name, password):
    # Read the file
    with open(file_name, 'rb') as f:
        data = f.read()
    # Derive a key from the password
    password = password.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    # Decrypt the data
    decrypted_data = f.decrypt(data)
    # Run the decrypted script
    exec(decrypted_data)

# Main function
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e", ["help", "input="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    encrypt=False
    filename=None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            filename = arg
        elif opt in ("-e", "--encrypt"):
            encrypt=True

    if encrypt==True and not filename==None:
        password = getpass.getpass(prompt='Enter password: ')
        encrypt_script(filename, password)
        sys.exit(0)
    elif not filename==None:
        password = getpass.getpass(prompt='Enter password: ')
        run_encrypted_script(filename, password)
        sys.exit(0)
    else:
        show_help()
        sys.exit(1)



def show_help():
    print("This script takes a filename as input and does something with it.")
    print("Usage: python " + sys.argv[0] + " [-h] [-i <filename>] -e")
    print("-h --help    Show this help message")
    print("-i --input   Provide a filename as input (required)")
    print("-e --encrypt Encrypt File (This overwrites the existing file)")

if __name__ == "__main__":
    main()

