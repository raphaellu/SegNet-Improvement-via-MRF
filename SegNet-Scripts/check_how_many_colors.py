import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from sets import Set

colors = Set([])
#color_matches = {
#(222, 40, 60,255) : (60, 40, 222)

#}

for i in range (0,1):
    img = Image.open("uncertainty/" + str(i) + ".png")
    img_px = img.load()
    (width, height) = img.size
    for w in range(0, width):
        for h in range(0, height):
            color = img_px[w,h]
	    colors.add(color)

print len(colors)
for i in colors:
    print i
