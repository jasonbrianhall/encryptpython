from PIL import Image
from pro import predictable_random_order

# Encodes data into PNG using 32 bit length
def encode_image(image_filename, outfile, message, pro=False, password=""):

	# Open the PNG image
	im = Image.open(image_filename)

	# Checks if it has an alpha layer and adds it if it doesn't
	has_alpha = im.mode.endswith('A')
	if not has_alpha:
		# Create a new image with an alpha layer
		im.putalpha(255)

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
				if counter>=len(data):
					break
	else:
		prolist=[]
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				r, g, b, a = pixels[i, j]
				newdata={"i": i, "j": j, "red": r, "green": g, "blue": b, "alpha": a}
				prolist.append(newdata)
		predictable_random_order(password, prolist)
		
		counter=0
		for superdata in prolist:
			r=superdata.get("red")
			g=superdata.get("green")
			b=superdata.get("blue")
			a=superdata.get("alpha")
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
			i=superdata.get("i")
			j=superdata.get("j")
			#print(i,j)
			pixels[superdata.get("i"), superdata.get("j")] = (r, g, b, a)
			if counter>=len(data):
				break

			
	temp=outfile.split(".", 1)
	outfile=temp[0]+".png"
	im.save(outfile)
	print(outfile)
	print("Message encoded successfully.")

# Decodes data in PNG using 32 bit length
def decode_image(encoded_image_filename, pro=False, password=""):

	# Open the PNG image
	im = Image.open(encoded_image_filename)
	# Get the pixel data from the image
	pixels = im.load()

	message=""
	if pro==False:
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
	else:
		prolist=[]
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				r, g, b, a = pixels[i, j]
				data={"i": i, "j": j, "red": r, "green": g, "blue": b, "alpha": a}
				prolist.append(data)
		predictable_random_order(password, prolist)
		for data in prolist:
			r=data.get("red")
			g=data.get("green")
			b=data.get("blue")
			a=data.get("alpha")
			r=r%2
			message=message+str(r)
			g=g%2
			message=message+str(g)				
			b=b%2
			message=message+str(b)
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
    
'''# Example usage
message=(chr(0)+chr(1)+chr(196)+chr(255)+'Hello, world to the nth degree!').encode("latin-1")
encode_image('test.png', 'outfile.png', message, pro=True, password="bob")
print(decode_image('outfile.png', pro=True, password="bob"))'''
