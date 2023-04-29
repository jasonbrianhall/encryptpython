#!/usr/bin/env python

'''  This code encrypted a python script using AES-256 encryption (this code is FIPS 140-2 compliant); it has two modes, self-contained python script or it can run the encrypted data 

Written by Jason Hall (jasonbrianhall@gmail.com)
'''

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
import steghide
import struct

# Get Encrypted Data
def get_encrypt_script(file_name, password):
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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:16])

    # Generate a random initialization vector (IV)
    iv=""
    for x in range(0,AES.block_size):
        iv = iv+chr(random.randint(0,255))

    length_as_int = struct.pack('I', len(data))
    data=length_as_int+data

    iv=iv.encode()[:16]
    # Pad the data to a multiple of the block size
    padding_length = AES.block_size - (len(data) % AES.block_size)
    offset=chr(padding_length).encode()
    data = data + (chr(padding_length) * padding_length).encode()
    
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt the data and return the IV and encrypted data as a tuple
    ct = cipher.encrypt(data)
    return offset+iv+ct

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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:16])

    # Generate a random initialization vector (IV)
    iv=""
    for x in range(0,AES.block_size):
        iv = iv+chr(random.randint(0,255))
    iv=iv.encode()[:16]
    # Pad the data to a multiple of the block size
    length_as_int = struct.pack('I', len(data))
    data= length_as_int + data

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
def run_encrypted_data(data, password):

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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:16])
    iv=data[1:AES.block_size+1]
    offset=-1*data[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        pt = cipher.decrypt(data[1+AES.block_size:])
    except:
        print("\nDecryption error ... probably wrong password")
        return

    length=pt[0] + pt[1]*256 + pt[2]*256**2 + pt[3]*256**3
    exec(pt[4:length+4])
    #exec(decrypted_data[:offset])


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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:16])
    iv=data[1:AES.block_size+1]
    offset=-1*data[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        pt = cipher.decrypt(data[1+AES.block_size:])
    except:
        print("\nDecryption error ... probably wrong password")
        return

    length=pt[0] + pt[1]*256 + pt[2]*256**2 + pt[3]*256**3
    exec(pt[4:length+4])
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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:AES.block_size])

    # Generate a random initialization vector (IV)
    iv=""
    for x in range(0,AES.block_size):
        iv = iv+chr(random.randint(0,255))

    length_as_int = struct.pack('I', len(data))
    data=length_as_int+data

    iv=iv.encode()[:16]
    # Pad the data to a multiple of the block size
    padding_length = AES.block_size - (len(data) % AES.block_size)
    offset=chr(padding_length).encode()

    data = data + (chr(padding_length) * padding_length).encode()
    
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt the data and return the IV and encrypted data as a tuple
    ct = cipher.encrypt(data)
    ct = offset+iv+ct
    data=b"""#!/usr/bin/env python
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

# Decrypt and run the script
def run_encrypted_script(password):
    # Read the data
    encrypted_data = b\'\'\'""" + base64.b64encode(ct) + b"""\'\'\'
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
    key = base64.urlsafe_b64encode(kdf.derive(password)[:16])
    data=base64.b64decode(encrypted_data)
    iv=data[1:AES.block_size+1]
    offset=-1*data[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        pt = cipher.decrypt(data[1+AES.block_size:])
        length=pt[0] + pt[1]*256 + pt[2]*256**2 + pt[3]*256**3
        exec(pt[4:length+4])
    except ValueError:
        print("\t** Invalid password!!!")
        sys.exit(1)

def main():
    password = getpass.getpass(prompt='Enter password to decrypt script: ')
    run_encrypted_script(password)

if __name__ == "__main__":
    main()
"""

    with open(filename, 'wb') as f:
        f.write(data)



# Main function
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:ecp:P", ["help", "input="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    encrypt=False
    filename=None
    selfencrypted=False
    pngfile=None
    usepro=True
    inputset=False
    pngset=False
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            filename = arg
            inputset=True
        elif opt in ("-e", "--encrypt"):
            encrypt=True
        elif opt in ("-c", "--create"):
            selfencrypted=True
        elif opt in ("-p", "--png"):
            pngfile = arg
            pngset=True
        elif opt in ("-P", "--pro"):
            usepro=False
            
    if inputset==True and pngset==True and encrypt==False:
        print("Can not set -i and -p at the same time without setting -e")
        sys.exit(1)
            
    if encrypt==True and not filename==None:
        if pngfile==None:
            password = getpass.getpass(prompt='Enter password to encrypt the script: ')
            encrypt_script(filename, password)
        else:
            password = getpass.getpass(prompt='Enter password to encrypt the PNG: ')
            data=get_encrypt_script(filename, password)
            if usepro==False:
                steghide.encode_image(pngfile, pngfile, data)
            else:
                steghide.encode_image(pngfile, pngfile, data, pro=True, password=password)
        sys.exit(0)
    elif not filename==None and selfencrypted==False:
        password = getpass.getpass(prompt='Enter password to decrypt/run encrypted script: ')
        run_encrypted_script(filename, password)
        sys.exit(0)
    elif not pngfile==None and selfencrypted==False:
        password = getpass.getpass(prompt='Enter password to decrypt the PNG: ')
        if usepro==False:
            data=steghide.decode_image(pngfile)
        else:
            data=steghide.decode_image(pngfile, pro=True, password=password)
        run_encrypted_data(data, password)
        sys.exit(0)
    elif selfencrypted==True and not filename==None:
        password = getpass.getpass(prompt='Enter password to create encrypted script: ')
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
    print("-p --png     Steganography PNG file where the script is hidden (when decrypting, don't include -i)")
    print("-P --pro     Disable Predictable Random Order (disabling it makes it less secure)")

if __name__ == "__main__":
    main()

