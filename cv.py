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
