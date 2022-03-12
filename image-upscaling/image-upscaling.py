import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt
import numpy as np

sr = dnn_superres.DnnSuperResImpl_create()

image_upscaling_user_input = 0

image_upscaling_user_input = int(input('Enter upscaling value: '))

image = cv2.imread(r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\image-upscaling\billow926-XnFxe5eN0Q0-unsplash-downsampled.jpg')

if image_upscaling_user_input == 2:
    sr.readModel(r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\image-upscaling\models\EDSR_x2.pb')
    sr.setModel("edsr", 2)
elif image_upscaling_user_input == 3:
    sr.readModel(r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\image-upscaling\models\EDSR_x3.pb')
    sr.setModel("edsr", 3)
elif image_upscaling_user_input == 4:
    sr.readModel(r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\image-upscaling\models\EDSR_x4.pb')    
    sr.setModel("edsr", 4)

# Upscale the image
result = sr.upsample(image)
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
plt.imshow(result)
plt.show()