import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from compute_test_result import select_match
"""
for i in range(0,62):
    img = Image.open("gt/"+str(i)+".png")
    img2_fn = 8550+30*(i)
    if img2_fn < 10000:
        img2_fn = "0001TP_00" + str(img2_fn) +"_L"
    else:
        img2_fn = "0001TP_0" + str(img2_fn) + "_L"

    img2 = Image.open("gt_701/" + img2_fn + ".png")
    print "img1: " + str(i) + " img2: " + img2_fn
    img2 = img2.resize(img.size)
    img_pix = img.load()
    img2_pix = img2.load()

    (width, height) = img.size
    for w in range(0,width):
	for h in range(0, height):
	    gt_701_color = select_match(img2_pix[w,h])
	    if gt_701_color == (128, 0, 192):
		img.putpixel((w,h), (255, 69, 0))
    	    
    img.save("gt_modified/" + str(i) + ".png")
"""


for i in range(62,233):
    img = Image.open("gt/"+str(i)+".png")
    img2_fn = 0+30*(i-62)
    if i == 62:
	img2_fn = "Seq05VD_f00000_L"
    elif img2_fn < 100 and img2_fn > 0 :
	img2_fn = "Seq05VD_f000" + str(img2_fn) + "_L"
    elif img2_fn < 1000 and img2_fn >= 100:
        img2_fn = "Seq05VD_f00" + str(img2_fn) + "_L"
    elif img2_fn >= 1000:
        img2_fn = "Seq05VD_f0" + str(img2_fn) +"_L"
    img2 = Image.open("gt_701/" + img2_fn + ".png")

    print "img1: " + str(i) + " img2: " + img2_fn
    img2 = img2.resize(img.size)
    img_pix = img.load()
    img2_pix = img2.load()

    (width, height) = img.size
    for w in range(0,width):
	for h in range(0, height):
	    gt_701_color = select_match(img2_pix[w,h])
	    if gt_701_color == (128, 0, 192):
		img.putpixel((w,h), (255, 69, 0))
    	    
    img.save("gt_modified/" + str(i) + ".png")


