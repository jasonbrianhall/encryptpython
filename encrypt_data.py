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
import steghide
import struct

def get_encrypt_data(file_name, password):
    """Encrypt the contents of a file without executing it"""
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
    iv = ''.join(chr(random.randint(0,255)) for _ in range(AES.block_size))
    iv = iv.encode()[:16]
    
    # Add length information
    length_as_int = struct.pack('I', len(data))
    data = length_as_int + data

    # Pad the data
    padding_length = AES.block_size - (len(data) % AES.block_size)
    offset = chr(padding_length).encode()
    data = data + (chr(padding_length) * padding_length).encode()
    
    # Create cipher and encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(data)
    return offset + iv + ct

def decrypt_data(data, password):
    """Decrypt the data and return it without executing"""
    # Derive key from password
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
    
    # Extract IV and decrypt
    iv = data[1:AES.block_size+1]
    offset = -1 * data[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    try:
        pt = cipher.decrypt(data[1+AES.block_size:])
        # Extract original length
        length = pt[0] + pt[1]*256 + pt[2]*256**2 + pt[3]*256**3
        # Return actual data without executing
        return pt[4:length+4]
    except:
        print("\nDecryption error ... probably wrong password")
        return None

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:ep:P", ["help", "input=", "encrypt", "png="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    filename = None
    pngfile = None
    encrypt = False
    use_pro = True
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            filename = arg
        elif opt in ("-e", "--encrypt"):
            encrypt = True
        elif opt in ("-p", "--png"):
            pngfile = arg
        elif opt in ("-P", "--pro"):
            use_pro = False

    if not filename and not pngfile:
        show_help()
        sys.exit(1)

    if encrypt and filename and pngfile:
        # Encrypt and hide in image
        password = getpass.getpass(prompt='Enter password to encrypt the data: ')
        data = get_encrypt_data(filename, password)
        outfile = f"{os.path.splitext(pngfile)[0]}_encrypted.png" if pngfile.endswith(".png") else pngfile
        steghide.encode_image(pngfile, outfile, data, pro=use_pro, password=password)
        print(f"Data encrypted and hidden in {outfile}")
    
    elif pngfile and not encrypt:
        # Extract and decrypt from image
        password = getpass.getpass(prompt='Enter password to decrypt the data: ')
        data = steghide.decode_image(pngfile, pro=use_pro, password=password)
        if data:
            decrypted = decrypt_data(data, password)
            if decrypted:
                output_file = f"extracted_data_{os.path.splitext(os.path.basename(pngfile))[0]}.bin"
                with open(output_file, 'wb') as f:
                    f.write(decrypted)
                print(f"Decrypted data saved to {output_file}")
    else:
        show_help()
        sys.exit(1)

def show_help():
    print("Steganography Tool - Hide and extract encrypted data in images")
    print(f"Usage: python {sys.argv[0]} [options]")
    print("Options:")
    print("-h --help    Show this help message")
    print("-i --input   Input file containing data to hide")
    print("-p --png     Image file to hide data in or extract from")
    print("-e --encrypt Encrypt and hide data (requires both -i and -p)")
    print("-P --pro     Disable Predictable Random Order (less secure)")
    print("\nExample Usage:")
    print(f"{sys.argv[0]} -i secret.txt -p image.png -e    # Hide encrypted data in image")
    print(f"{sys.argv[0]} -p image_encrypted.png           # Extract and decrypt data")

if __name__ == "__main__":
    main()

