#!/usr/bin/env python

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.Cipher import AES
import sys
import getopt
import getpass
import string
import random

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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:AES.block_size])

    # Generate a random initialization vector (IV)
    iv=""
    for x in range(0,AES.block_size):
        iv = iv+random.choice(string.printable)
    iv=iv.encode()
    # Pad the data to a multiple of the block size
    padding_length = AES.block_size - (len(data) % AES.block_size)
    offset=chr(padding_length).encode()

    data = data + (chr(padding_length) * padding_length).encode()
    
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt the data and return the IV and encrypted data as a tuple
    ct = cipher.encrypt(data)
    with open(file_name, 'wb') as f:
        f.write(offset+iv+ct)

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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:AES.block_size])
    iv=data[1:AES.block_size+1]
    offset=-1*data[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(data[1+AES.block_size:])
    exec(pt)
    #exec(decrypted_data[:offset])

def create_encrypted_script(filename, password):
    # Read the file
    with open(filename, 'rb') as f:
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
    data=b"""#!/usr/bin/env python
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import getpass


# Decrypt and run the script
def run_encrypted_script(password):
    # Read the data
    data = b\'\'\'""" + encrypted_data + b"""\'\'\'
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
    try:
        # Decrypt the data
        decrypted_data = f.decrypt(data)
    # Run the decrypted script
        exec(decrypted_data)
    except:
        print("Wrong password!!!")
        sys.exit(1)

def main():
    password = getpass.getpass(prompt='Enter password: ')
    run_encrypted_script(password)

if __name__ == "__main__":
    main()
"""

    with open(filename, 'wb') as f:
        f.write(data)



# Main function
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:ec", ["help", "input="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    encrypt=False
    filename=None
    selfencrypted=False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            filename = arg
        elif opt in ("-e", "--encrypt"):
            encrypt=True
        elif opt in ("-c", "--create"):
            selfencrypted=True

    if encrypt==True and not filename==None:
        password = getpass.getpass(prompt='Enter password: ')
        encrypt_script(filename, password)
        sys.exit(0)
    elif not filename==None and selfencrypted==False:
        password = getpass.getpass(prompt='Enter password: ')
        #try:
        run_encrypted_script(filename, password)
        #except:
            #print("Script isn't encrypted or wrong password!!!")
        #sys.exit(0)
    elif selfencrypted==True and not filename==None:
        password = getpass.getpass(prompt='Enter password: ')
        create_encrypted_script(filename, password)
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
    print("-c --create  Creates a Self Encrypting Python Script")

if __name__ == "__main__":
    main()

