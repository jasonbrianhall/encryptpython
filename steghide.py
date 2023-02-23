from PIL import Image
from pro import predictable_random_order

# Encodes data into Image file (supports non-lossy files such as PNG, BMP, and TIF; sigbits should always be 1 but can be changed for testing)
def encode_image(image_filename, outfile, message, pro=False, password="", addalpha=False, sigbits=1):

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
	ander=1
	for x in range(0,sigbits):
		ander*=2
	adder=ander-1
	ander=256-(ander)

	beginingmultiplier=1
	for x in range(0,sigbits-1):
		beginingmultiplier*=2

	if pro==False:
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
				else:
					r, g, b    = pixels[i, j]
				
				if counter<len(data):
					r=ander&r
					multiplier=beginingmultiplier
					for x in range(0,sigbits):
						if counter<len(data):
							if data[counter]=="1":
								r+=1*int(multiplier)
							multiplier/=2
							counter+=1
				if counter<len(data):
					g=ander&g
					multiplier=beginingmultiplier
					for x in range(0,sigbits):
						if counter<len(data):
							if data[counter]=="1":
								g+=1*int(multiplier)
							multiplier/=2
							counter+=1

				if counter<len(data):
					b=ander&b
					multiplier=beginingmultiplier
					for x in range(0,sigbits):
						if counter<len(data):
							if data[counter]=="1":
								b+=1*int(multiplier)
							multiplier/=2
							counter+=1

				if has_alpha==True and counter<len(data):
					if counter<len(data):
						a=ander&a
						multiplier=beginingmultiplier
						for x in range(0,sigbits):
							if counter<len(data):
								if data[counter]=="1":
									a+=1*int(multiplier)
								multiplier/=2
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
				r=ander&r
				multiplier=beginingmultiplier
				for x in range(0,sigbits):
					if counter<len(data):
						if data[counter]=="1":
							r+=1*int(multiplier)
						multiplier/=2
						counter+=1
			if counter<len(data):
				g=ander&g
				multiplier=beginingmultiplier
				for x in range(0,sigbits):
					if counter<len(data):
						if data[counter]=="1":
							g+=1*int(multiplier)
						multiplier/=2
						counter+=1

			if counter<len(data):
				b=ander&b
				multiplier=beginingmultiplier
				for x in range(0,sigbits):
					if counter<len(data):
						if data[counter]=="1":
							b+=1*int(multiplier)
						multiplier/=2
						counter+=1

			if has_alpha==True and counter<len(data):
				if counter<len(data):
					a=ander&a
					multiplier=beginingmultiplier
					for x in range(0,sigbits):
						if counter<len(data):
							if data[counter]=="1":
								a+=1*int(multiplier)
							multiplier/=2
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

	temp=outfile.split(".", 1)
	if has_alpha:
		outfile=temp[0]+".png"
	else:
		if len(temp)>1:
			if not (temp[1].lower()=="bmp" or temp[1].lower()=="tif" or temp[1].lower()=="png"):
				outfile=temp[0]+".png"
		else:
			outfile=temp[0]+".png"
			
	im.save(outfile)
	#print(outfile)
	print("Message encoded successfully; saved as " + outfile)

# Decodes data in PNG using 32 bit length
def decode_image(encoded_image_filename, pro=False, password="", sigbits=1):

	# Open the PNG image
	im = Image.open(encoded_image_filename)
	# Get the pixel data from the image
	pixels = im.load()

	# Checks if it has an alpha layer and adds it if it doesn't
	has_alpha = im.mode.endswith('A')

	ander=1
	for x in range(0,sigbits):
		ander*=2
		
	message=""
	if pro==False:
		for i in range(im.size[0]):
			for j in range(im.size[1]):
				if has_alpha:
					r, g, b, a = pixels[i, j]
				else:
					r, g, b = pixels[i, j]

				r=r%ander
				message += format(r, f'0{sigbits}b')
				g=g%ander
				message += format(g, f'0{sigbits}b')
				b=b%ander
				message += format(b, f'0{sigbits}b')



				if has_alpha:
					a=a%ander
					message += format(a, f'0{sigbits}b')


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
		counter=-32
		finaldatalength=None
		for data in prolist:
			i=data.get("i")
			j=data.get("j")
			if has_alpha:
				r, g, b, a = pixels[i, j]
			else:
				r, g, b    = pixels[i, j]
			r=r%ander
			message += format(r, f'0{sigbits}b')
			counter+=sigbits
			g=g%ander
			message += format(g, f'0{sigbits}b')
			counter+=sigbits
			b=b%ander
			message += format(b, f'0{sigbits}b')
			counter+=sigbits
			if has_alpha:
				a=a%ander
				message += format(r, f'0{sigbits}b', end="")
				counter+=sigbits
			if finaldatalength==None and counter>=0:
				datalength=message[0:32]
				finaldatalength=int(datalength,2)
				#print(finaldatalength)

				
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



