from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from pro import predictable_random_order

message="Hello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  Hddello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  Hello World from the greatest country in the world!!!  ".encode()

binary_message = ''
for c in message.decode('latin-1'):
	binary_message+=format(ord(c), '08b')

print(binary_message)

# Load PNG image
img = Image.open("test.jpg")

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

'''counter=0
data=[]
for x in dct_r:
	temp={"counter": counter, "data": x}
	data.append(x)
	counter+=1

print(data)
predictable_random_order("bob", data)
print(data)
#predictable_random_order("bob", dct_g)
#predictable_random_order("bob", dct_b)'''

binary_message_pos=0
#print(len(binary_message))

for dct_coeffs in dct_r:
	# round the DCT coefficients to integers
	dct_ints = np.round(dct_coeffs).astype(int)

	# add a string represented by binary if it's a 1 in the string
	#binary_message = '1010'
	if len(dct_coeffs)+binary_message_pos >= len(binary_message):
		temp=len(binary_message)
	else:
		temp=len(dct_coeffs)+binary_message_pos
	tempstring=binary_message[binary_message_pos:temp]
	print(len(tempstring), binary_message_pos)
	
	for i, bit in enumerate(binary_message[binary_message_pos:temp]):
		# zero out the LSB of each coefficient
		print("Before", dct_ints[i])
		dct_ints[i] = dct_ints[i] & ~1

		#print(i,bit, dct_ints[i])
		
		if bit == '1':
			dct_ints[i]+=1
		binary_message_pos+=1
		print("After", dct_ints[i])

		
	# convert the integers back to floating-point values
	dct_coeffs = dct_ints.astype(float)

	#print("bmp", binary_message_pos)


# Apply 2D IDCT to each color channel to obtain image
img_r_reconstructed = idct(idct(dct_r.T, norm='ortho').T, norm='ortho')
img_g_reconstructed = idct(idct(dct_g.T, norm='ortho').T, norm='ortho')
img_b_reconstructed = idct(idct(dct_b.T, norm='ortho').T, norm='ortho')

# Merge color channels into image
img_reconstructed = Image.merge("RGB", (
    Image.fromarray(np.round(img_r_reconstructed).astype(np.uint8)),
    Image.fromarray(np.round(img_g_reconstructed).astype(np.uint8)),
    Image.fromarray(np.round(img_b_reconstructed).astype(np.uint8))
))

# Save reconstructed image to file
img_reconstructed.save("example_reconstructed.jpg")

