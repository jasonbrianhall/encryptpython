This program encrypts a python script, creates an encrypted self-executable python script, or embeds a python script inside a PNG that can be executed via this program.  

This code basically creates a self encrypting python script which the user could distribute without revealing the source code; password should be transmitted out of bounds.

It supports steganography via the pillow library for PNG files which encodes data via the least significant bit in the various channels (Red, Green, Blue, Alpha) and uses AES-256 encryption.  Their is an example using the Fermat library but since Fermat isn't FIPS 140-2 compliant, it isn't being maintained.


