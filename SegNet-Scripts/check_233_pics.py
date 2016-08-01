import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

"""
for i in range(0,62):
    img = mpimg.imread("gt/"+str(i)+".png")
    img2_fn = 8550+30*(i)
    if img2_fn < 10000:
        img2_fn = "0001TP_00" + str(img2_fn) +"_L"
    else:
        img2_fn = "0001TP_0" + str(img2_fn) + "_L"
    plt.figure()
    plt.imshow(img)
    img2 = mpimg.imread("gt_701/" + img2_fn + ".png")
    plt.figure()
    plt.imshow(img2) 
    print "img1: " + str(i) + " img2: " + img2_fn
    plt.show()
"""
for i in range(62,233):
    img = mpimg.imread("gt/"+str(i)+".png")
    img2_fn = 0+30*(i-62)
    if i == 62:
	img2_fn = "Seq05VD_f00000_L"
    elif img2_fn < 100 and img2_fn > 0 :
	img2_fn = "Seq05VD_f000" + str(img2_fn) + "_L"
    elif img2_fn < 1000 and img2_fn >= 100:
        img2_fn = "Seq05VD_f00" + str(img2_fn) + "_L"
    elif img2_fn >= 1000:
        img2_fn = "Seq05VD_f0" + str(img2_fn) +"_L"
    plt.figure()
    plt.imshow(img)
    img2 = mpimg.imread("gt_701/" + img2_fn + ".png")
    plt.figure()
    plt.imshow(img2) 
    print "img1: " + str(i) + " img2: " + img2_fn
    plt.show()
