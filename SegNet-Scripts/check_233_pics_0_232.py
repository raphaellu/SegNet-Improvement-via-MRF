import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

for i in range(0,233):
    img = mpimg.imread("gt/"+str(i)+".png")
    plt.figure()
    plt.imshow(img)
    img2 = mpimg.imread("predictions/"+str(i)+".png")
    plt.figure()
    plt.imshow(img2) 
    img3 = mpimg.imread("uncertainty/"+str(i)+".png")
    plt.figure()
    plt.imshow(img3) 
    plt.show()
