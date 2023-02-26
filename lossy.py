from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct

# Load PNG image
img = Image.open("test.jpg")

# Separate image into color channels
img_r, img_g, img_b = img.split()

# Convert color channels to NumPy arrays
arr_r = np.array(img_r)
arr_g = np.array(img_g)
arr_b = np.array(img_b)

print(len(arr_r))

# Apply 2D DCT to each color channel
dct_r = dct(dct(arr_r.T, norm='ortho').T, norm='ortho')
dct_g = dct(dct(arr_g.T, norm='ortho').T, norm='ortho')
dct_b = dct(dct(arr_b.T, norm='ortho').T, norm='ortho')

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

