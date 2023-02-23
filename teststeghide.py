from steghide import encode_image, decode_image


# Todo; move in test file
def testmain():
	# Example usage
	password="bobthemagicalpenguinwholovesbacon"
	message=(chr(0)+chr(1)+chr(196)+chr(255)+'Hello, world to the nth degree!\n\nCowabunga dude\n\n').encode("latin-1")
	print("Message being encoded: ", message)

	print("\nTesting PRO Features")
	encode_image('test.jpg', 'outfile-pro.png', message, pro=True, password=password, sigbits=1)
	print(decode_image('outfile-pro.png', pro=True, password=password, sigbits=1))

	print("\nTesting PRO Features; sigbits=8; really ugly PNG; very visual that their is something wrong")
	encode_image('test.jpg', 'outfile-pro-8bit.png', message, pro=True, password=password, sigbits=8)
	print(decode_image('outfile-pro-8bit.png', pro=True, password=password, sigbits=8))

	# Testing pro=False (insecure mode)
	print("\nTesting Insecure Mode")
	encode_image('test.jpg', 'outfile-insecure.png', message, pro=False, password=password)
	print(decode_image('outfile-insecure.png', pro=False, password=password))

	# Testing JPEG MOde (this *should* fail); only getting 100 bytes
	print("\nTesting JPEG; shouldn't work")
	encode_image('test.jpg', 'outfile.jpg', message, pro=False, password=password, sigbits=1)
	data=decode_image('outfile.jpg', pro=False, password=password, sigbits=1)
	print(data[0:100])

	# Testing TIFF MOde (this *should* work; secure)
	print("\nTesting TIF; should work")
	encode_image('test.jpg', 'outfile.tif', message, pro=True, password=password)
	print(decode_image('outfile.tif', pro=True, password=password))

	# Testing BMP MOde (this *should* work; secure)
	print("\nTesting BMP; should work")
	encode_image('test.jpg', 'outfile.bmp', message, pro=True, password=password)
	print(decode_image('outfile.bmp', pro=True, password=password))

	# Testing WEBP MOde (this *shouldn't* work)
	print("\nTesting WEBP; shouldn't work")
	encode_image('test.jpg', 'outfile.webp', message, pro=False, password=password)
	data=decode_image('outfile.webp', pro=False, password=password)
	print(data[0:100])



if __name__ == "__main__":
    testmain()  

