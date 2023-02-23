from PIL import Image
from pro import predictable_random_order

# Encodes data into PNG using 32 bit length
def encode_image(image_filename, outfile, message, pro=False, password="", addalpha=False):

	# Open the PNG image
	im = Image.open(image_filename)

	# Checks if it has an alpha layer and adds it if it doesn't
	has_alpha = im.mode.endswith('A')
	if addalpha==True and not has_alpha:
		# Create a new image with an alpha layer
		im.putalpha(255)
		has_alpha=True

	# Convert the message to a binary string
	binary_message = ''
	for c in message.decode('latin-1'):
		binary_message+=format(ord(c), '08b')
	#binary_message = ''.join(format(ord(c), '08b') for c in message.decode('latin-1'))

	# Get the length of the binary message
	message_length = len(message)
	#print("Message Length", message_length)
	# Convert the message length to a binary string
	binary_message_length = format(message_length, '032b').zfill(32)

	# Get the pixel data from the image
	pixels = im.load()

	# Loop through each pixel and each color channel
	message_index = 0

	max_message_bits = (im.size[0] * im.size[1] - 32) * 4

	data=binary_message_length+binary_message
	counter=0
	if pro==False:
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
				else:
					r, g, b    = pixels[i, j]
				
				if counter<len(data):
					r=254&r
					if data[counter]=="1":
						r+=1

					counter+=1
				if counter<len(data):
					g=254&r
					if data[counter]=="1":
						g+=1
					counter+=1
				if counter<len(data):
					b=254&b
					if data[counter]=="1":
						b+=1
					counter+=1
				if has_alpha==True and counter<len(data):
					a=254&a
					if data[counter]=="1":
						a+=1
					counter+=1		
				#print(r,g,b,a)
				if has_alpha:
					pixels[i, j] = (r, g, b, a)
				else:
					pixels[i, j] = (r, g, b)				
				if counter>=len(data):
					break
	else:
		prolist=[]
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
					#newdata={"i": i, "j": j, "red": r, "green": g, "blue": b, "alpha": a}
				else:
					r, g, b    = pixels[i, j]
					#newdata={"i": i, "j": j, "red": r, "green": g, "blue": b}
				newdata={"i": i, "j": j}
				prolist.append(newdata)
		predictable_random_order(password, prolist)
		
		counter=0
		for superdata in prolist:
			i=superdata.get("i")
			j=superdata.get("j")
			if has_alpha:
				r, g, b, a = pixels[i, j]
			else:
				r, g, b = pixels[i,j]
			if counter<len(data):
				r=254&r
				if data[counter]=="1":
					r+=1

				counter+=1
			if counter<len(data):
				g=254&r
				if data[counter]=="1":
					g+=1
				counter+=1
			if counter<len(data):
				b=254&b
				if data[counter]=="1":
					b+=1
				counter+=1
			if has_alpha==True and counter<len(data):
				a=254&a
				if data[counter]=="1":
					a+=1
				counter+=1		
			i=superdata.get("i")
			j=superdata.get("j")
			#print(i,j)
			if has_alpha:
				pixels[superdata.get("i"), superdata.get("j")] = (r, g, b, a)
			else:
				pixels[superdata.get("i"), superdata.get("j")] = (r, g, b)			
			if counter>=len(data):
				break

	if has_alpha:
		temp=outfile.split(".", 1)
		outfile=temp[0]+".png"
	im.save(outfile)
	#print(outfile)
	#print("Message encoded successfully.")

# Decodes data in PNG using 32 bit length
def decode_image(encoded_image_filename, pro=False, password=""):

	# Open the PNG image
	im = Image.open(encoded_image_filename)
	# Get the pixel data from the image
	pixels = im.load()

	# Checks if it has an alpha layer and adds it if it doesn't
	has_alpha = im.mode.endswith('A')

	message=""
	if pro==False:
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
				else:
					r, g, b = pixels[i, j]

				r=r%2
				message=message+str(r)
				g=g%2
				message=message+str(g)				
				b=b%2
				message=message+str(b)
				if has_alpha:
					a=a%2
					message=message+str(a)
				#print(r,b,g,a)
	else:
		prolist=[]
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
				else:
					r, g, b = pixels[i, j]
				data={"i": i, "j": j}
				
				prolist.append(data)
		predictable_random_order(password, prolist)
		# This code could crash with very large messages since it doesn't calculate datalength until after it appends junk data to the message 
		for data in prolist:
			i=data.get("i")
			j=data.get("j")
			if has_alpha:
				r, g, b, a = pixels[i, j]
			else:
				r, g, b    = pixels[i, j]
			r=r%2
			message=message+str(r)
			g=g%2
			message=message+str(g)				
			b=b%2
			message=message+str(b)
			if has_alpha:
				a=a%2
				message=message+str(a)
			
	datalength=message[0:32]
	#print(datalength)
	finaldatalength=int(datalength,2)
	#print(datalength)
	finalmessage=message[32:32+finaldatalength*8]
	#print(datalength, finalmessage)		
	substrings = [finalmessage[i:i+8] for i in range(0, len(finalmessage), 8)]

	binary_message=b""
	for x in substrings:
		intvalue=int(x,2)
		chrvalue=chr(intvalue)
		#print(intvalue, ord(chrvalue))
		binary_message+=chrvalue.encode("latin-1")

	return binary_message    
	
def testmain():
	# Example usage
	password="bobthemagicalpenguinwholovesbacon"
	message=(chr(0)+chr(1)+chr(196)+chr(255)+'Hello, world to the nth degree!\n\nCowabunga dude\n\n').encode("latin-1")
	print("Message being encoded: ", message)

	print("\nTesting PRO Features")
	encode_image('test.jpg', 'outfile.png', message, pro=True, password=password)
	print(decode_image('outfile.png', pro=True, password=password))


	# Testing pro=False (insecure mode)
	print("\nTesting Insecure Mode")
	encode_image('test.jpg', 'outfile.png', message, pro=False, password=password)
	print(decode_image('outfile.png', pro=False, password=password))

	# Testing JPEG MOde (this *should* fail); only getting 100 bytes
	print("\nTesting JPEG; shouldn't work")
	encode_image('test.jpg', 'outfile.jpg', message, pro=False, password=password)
	data=decode_image('outfile.jpg', pro=False, password=password)
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


