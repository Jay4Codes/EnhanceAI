import cv2 
import numpy as np    
import tensorflow as tf
import time
from patchify import patchify, unpatchify
# import matplotlib.pyplot as plt

def patches(img,patch_size):
  patches = patchify(img, (patch_size, patch_size, 3), step=patch_size)
  return patches

def get_model():
    RIDNet=tf.keras.models.load_model(r"C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\image-denoising-py-script\RIDNet.h5")
    return RIDNet

def prediction(img):
    start = time.time()
    model = get_model()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    nsy_img = cv2.resize(img,(1024,1024))
    nsy_img = nsy_img.astype("float32") / 255.0

    img_patches = patches(nsy_img,256)
    nsy=[]
    for i in range(4):
        for j in range(4):
            nsy.append(img_patches[i][j][0])
    nsy = np.array(nsy)
    
    pred_img = model.predict(nsy)
    pred_img = np.reshape(pred_img,(4,4,1,256,256,3))
    pred_img = unpatchify(pred_img, nsy_img.shape)
    end = time.time()
     
    img = cv2.resize(img,(512,512))
    pred_img = cv2.resize(pred_img,(512,512))
    # f = plt.figure(figsize=(12, 6))
    # f.add_subplot(1,2, 1)
    # plt.imshow(img)
    # f.add_subplot(1,2, 2)
    # plt.imshow(pred_img)
    # plt.show(block=True)
    # print('Time taken: ', end-start)

img = cv2.imread(r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\ImageDenoising\NoisyImage\image.jpg')
prediction(img)