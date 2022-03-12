import cv2
from google.colab.patches import cv2_imshow
import numpy as np
import matplotlib.pyplot as plt



x_pixels=500
y_pixels=500
resized=cv2.resize(img,(x_pixels,y_pixels)) 
# This is the code for resizing
cv2_imshow(resized)
grey=cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
# This is for greyscaling
cv2_imshow(grey)
neg=1-resized
cv2_imshow(neg)


img2=np.zeros((500,500,3),dtype=np.uint8)
img2[:]=[100,225,200]
# this is the code for filling color
text_font = cv2.FONT_HERSHEY_COMPLEX_SMALL
text='Kangte'
x_pos_text=200
y_pos_text=250
scale_text=5
color_code=(0,0,255)
cv2_imshow(img2)
text=cv2.putText(img2,text,(x_pos_text,y_pos_text),text_font,scale_text,color_code)
# this is the text u want to put
plt.imshow(text)
plt.show()

y_pos_upper=200
y_pos_down=400
x_pos_left=150
x_pos_right=350
cropped=resized[y_pos_upper:y_pos_down,x_pos_left:x_pos_right]
# this is the code for cropping based on x and y positions
cv2_imshow(cropped)


x_blur=15
y_blur=15
blur=cv2.blur(resized,(x_blur,y_blur))
# this is the code for blur


s_value=100
r_value=0.2
shade_factor=0.1
smooth=cv2.edgePreservingFilter(resized,cv2.RECURS_FILTER,s_value,r_value)
# this is the code for smoothing the image

pencil,colored=cv2.pencilSketch(resized,s_value,r_value,shade_factor=shade_factor)
# this is the code for pencil as well as colored sketch


imghsv=cv2.cvtColor(img3,cv2.COLOR_BGR2HSV).astype('float32')
h,s,v=cv2.split(imghsv)
s1_value=3
h1_value=2
v1_value=2
s=s*s1_value
h=h*h1_value
v=v*v1_value
s=np.clip(s,0,255)
h=np.clip(h,0,255)
v=np.clip(v,0,255)
imghsv=cv2.merge([h,s,v])
saturated=cv2.cvtColor(img3.astype('uint8'),cv2.COLOR_HSV2BGR)
# used for saturation

kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
img_sharpen = cv2.filter2D(img3, -1, kernel)
cv2_imshow(img_sharpen)
# Sharpern the image

img_sepia = np.array(img3, dtype=np.float64) # converting to float to prevent loss
img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
img_sepia = np.array(img_sepia, dtype=np.uint8)
cv2_imshow(img_sepia)
# Sepia filter


hdr = cv2.detailEnhance(img3, sigma_s=12, sigma_r=0.15)

# Hdr filter

inv = cv2.bitwise_not(img3)

# Invert Filter


from scipy.interpolate import UnivariateSpline
def LookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))


increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
blue_channel, green_channel,red_channel  = cv2.split(img3)
red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
sum= cv2.merge((blue_channel, green_channel, red_channel ))

# Summer filter

increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
blue_channel, green_channel,red_channel = cv2.split(img3)
red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
win= cv2.merge((blue_channel, green_channel, red_channel))

#Winter Filter

# Rotate the image
from scipy import ndimage
angle=45
rotated = ndimage.rotate(img3, angle)
cv2_imshow(rotated)

________________________________________________________________

import numpy as np
import cv2

	
#reading the image
input_image = cv2.imread('/content/photo-1535463731090-e34f4b5098c5.jpg')

#resizing the image according to our need
# resize() function takes 2 parameters,
# the image and the dimensions
input_image = cv2.resize(input_image, (480, 480))

# Extracting the height and width of an image
rows, cols = input_image.shape[:2]

# generating vignette mask using Gaussian
# resultant_kernels
X_resultant_kernel = cv2.getGaussianKernel(cols,200)
Y_resultant_kernel = cv2.getGaussianKernel(rows,200)

#generating resultant_kernel matrix
resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T

#creating mask and normalising by using np.linalg
# function
mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
output = np.copy(input_image)

# applying the mask to each channel in the input image
for i in range(3):
	output[:,:,i] = output[:,:,i] * mask
	
#displaying the original image
cv2_imshow(input_image)

#displaying the vignette filter image
cv2_imshow(output)


