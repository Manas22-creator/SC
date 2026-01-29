import matplotlib.pyplot as plt 
from PIL import Image 
import numpy as np 
sPicNameIn='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 7/ImagePr7.jpg' 
imageIn = Image.open(sPicNameIn) 
fig1=plt.figure(figsize=(10, 10)) 
fig1.suptitle('Audi R8', fontsize=20) 
imgplot = plt.imshow(imageIn) 
plt.show() 
 
imagewidth, imageheight = imageIn.size 
imageMatrix=np.asarray(imageIn) 
pixelscnt = (imagewidth * imageheight) 
print('Pixels:', pixelscnt) 
print('Size:', imagewidth, ' x', imageheight,) 
print(imageMatrix)
