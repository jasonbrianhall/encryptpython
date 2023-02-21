from PIL import Image

def encode_image(image_filename, outfile, message):

	# Open the PNG image
	im = Image.open(image_filename)

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
	for i in range(im.size[0]):
		for j in range(im.size[1]):
			r, g, b, a = pixels[i, j]
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
			if counter<len(data):
				a=254&a
				if data[counter]=="1":
					a+=1
				counter+=1		
			#print(r,g,b,a)
			pixels[i, j] = (r, g, b, a)

	im.save(outfile)
	print("Message encoded successfully.")

def decode_image(encoded_image_filename):

	# Open the PNG image
	im = Image.open(encoded_image_filename)
	# Get the pixel data from the image
	pixels = im.load()

	message=""
	for i in range(im.size[0]):
		for j in range(im.size[1]):
			r, g, b, a = pixels[i, j]
			r=r%2
			message=message+str(r)
			g=g%2
			message=message+str(g)				
			b=b%2
			message=message+str(b)
			a=a%2
			message=message+str(a)
			#print(r,b,g,a)

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
    
'''# Example usage
message=(chr(0)+chr(1)+chr(196)+chr(255)+'Hello, world!').encode("latin-1")
encode_image('test.png', 'outfile.png', message)
print(decode_image('outfile.png'))'''
   
        

