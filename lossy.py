from PIL import Image
from pro import predictable_random_order
import numpy as np

import math


def idct(coefficients):
	return np.fft.ifft2(coefficients, norm='ortho').real

def dct(signal):
	return np.fft.fft2(signal, norm='ortho')

def encode_image(image_filename, outfile, message, pro=False, password=""):

	binary_message = ''
	for c in message.decode('latin-1'):
		binary_message+=format(ord(c), '08b')

	img = Image.open(image_filename)

	pixels=img.load()

	for x in range(img.size[0]):
		for y in range(img.size[1]):
			r,g,b=pixels[x,y]
			print("Before", x,y, r,g,b)
			

	r_block = []
	g_block = []
	b_block = []
	for i in range(0, img.size[0]):
		r_row=[]
		g_row=[]
		b_row=[]
		for j in range(0, img.size[1]):
			r,g,b=pixels[i,j]
			r_row.append(r)
			g_row.append(g)
			b_row.append(b)
		r_block.append(r_row)
		g_block.append(g_row)
		b_block.append(b_row)
		

	r_dct_block = dct(r_block)
	g_dct_block = dct(g_block)
	b_dct_block = dct(b_block)

	'''for x in range(len(r_dct_block)):
		for y in range(len(r_dct_block[x])):
			print(x,y, r_dct_block[x][y])'''

	ir_dct_block=idct(r_dct_block)
	ig_dct_block=idct(g_dct_block)
	ib_dct_block=idct(b_dct_block)
	

	#print(r_dct_block)
	
	#print(len(r_dct_block))
	
	
	for i in range(0, img.size[0]):
		for j in range(0, img.size[1]):
			r=int(round(ir_dct_block[i][j]))
			b=int(round(ib_dct_block[i][j]))
			g=int(round(ig_dct_block[i][j]))
			print("After", i, j, r,g,b)
			pixels[i,j] = (r, g, b)

	img.save(outfile)

def decode_image(encoded_image_filename, pro=False, password=""):
	print("Start Decode")
	binary_message = ''

	# Load PNG image
	img = Image.open(encoded_image_filename)

	# Separate image into color channels
	img_r, img_g, img_b = img.split()

	# Convert color channels to NumPy arrays
	arr_r = np.array(img_r)
	arr_g = np.array(img_g)
	arr_b = np.array(img_b)

	# Apply 2D DCT to each color channel
	dct_r = dct(dct(arr_r.T, norm='ortho').T, norm='ortho')
	dct_g = dct(dct(arr_g.T, norm='ortho').T, norm='ortho')
	dct_b = dct(dct(arr_b.T, norm='ortho').T, norm='ortho')

	binary_message_pos=0
	#print(len(binary_message))

	for dct_coeffs in dct_r:
		# round the DCT coefficients to integers
		dct_ints = np.round(dct_coeffs).astype(int)

		# add a string represented by binary if it's a 1 in the string
		#binary_message = '1010'
		#tempstring=binary_message[0:len(dct_coeffs)]
		#print(len(tempstring), binary_message_pos)
		
		for i in range(0,40):
			#print(i, dct_ints[i])
			print(dct_ints[i])

			data=dct_ints[i]%2
			binary_message+=str(data)
			
	#print(binary_message)


